from datetime import datetime
from time import sleep

from django.contrib.sessions.models import Session
from django.db.models import Q
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from backend_django import settings

from ..helpers import utils
from ..models import BinaryRelation, Component


class TestSessions(TestCase):
    def setUp(self):
        self.acetone = Component.objects.create(
            name="acetone",
            a=7.11714,
            b=1210.595,
            c=229.664,
        )
        self.chloroforme = Component.objects.create(
            name="chloroforme",
            a=6.95465,
            b=1170.966,
            c=226.232,
        )
        self.benzene = Component.objects.create(
            name="benzene",
            a=6.87087,
            b=1196.760,
            c=219.161,
        )

        self.acetone_chloroforme = BinaryRelation.objects.create(
            component1=self.acetone,
            component2=self.chloroforme,
            a12=-643.277,
            a21=228.457,
            alpha=0.3043,
        )
        self.acetone_benzene = BinaryRelation.objects.create(
            component1=self.acetone,
            component2=self.benzene,
            a12=-193.34,
            a21=569.931,
            alpha=0.3007,
        )

    def test_session_creation(self):
        client = Client()
        # direct the client to index page to create the session
        response, creation_date = client.get(""), datetime.now().strftime(
            "%d/%m/%Y, %H:%M"
        )
        client_id = client.session.session_key

        # test creation of session
        self.assertEqual(client.session["created_in"], creation_date)
        self.assertEqual(
            client.session.get_expiry_age(), settings.SESSION_EXPIRY_DURATION
        )
        self.assertEqual(Session.objects.filter(pk=client_id).exists(), True)
        self.assertEqual(Session.objects.all().count(), 1)
        session = Session.objects.get(pk=client_id)

        # test that nothing is added when a session is created
        self.assertEqual(session.relations.all().count(), 0)
        self.assertEqual(session.components.all().count(), 0)

        # test that predifined elements in database are available to client
        self.assertEqual(
            list(utils.compounds_of_session(client_id)),
            [self.acetone, self.benzene, self.chloroforme],
        )

        self.assertEqual(
            list(utils.relations_of_session(client_id)),
            [self.acetone_chloroforme, self.acetone_benzene],
        )

        # test that session is not deleted when reloading page
        response = client.get("")

        ## session id shouold stay the same if no other session is created
        self.assertEqual(client.session.session_key, client_id)
        self.assertEqual(client.session["created_in"], creation_date)

    def test_session_addElement(self):
        # creating two sessions
        client1 = Client()
        client2 = Client()
        r1 = client1.get("")
        r2 = client2.get("")

        client1_id, client2_id = (
            client1.session.session_key,
            client2.session.session_key,
        )

        self.assertEqual(Session.objects.all().count(), 2)

        response = client1.post(
            reverse("add_component"),
            {
                "name": "compound1",
                "a": 0,
                "b": 0,
                "c": 0,
            },
        )

        self.assertEqual(response.url, reverse("index"))

        # test that new compound was added to database for session1 but not for session2
        self.assertEqual(
            Component.objects.filter(name="compound1").exists(), True
        )
        self.assertEqual(Component.objects.all().count(), 4)

        added_c1 = Component.objects.get(name="compound1", a=0, b=0, c=0)
        self.assertEqual(
            list(utils.compounds_of_session(client1_id)),
            [self.acetone, self.benzene, self.chloroforme, added_c1],
        )

        self.assertEqual(
            list(utils.compounds_of_session(client2_id)),
            [self.acetone, self.benzene, self.chloroforme],
        )

        session1 = Session.objects.get(pk=client1_id)
        session2 = Session.objects.get(pk=client2_id)

        self.assertEqual(session1.components.all().count(), 1)
        self.assertEqual(session2.components.all().count(), 0)

        response = client2.post(
            reverse("add_component"),
            {
                "name": "compound2",
                "a": 0,
                "b": 0,
                "c": 0,
            },
        )

        self.assertEqual(session1.components.all().count(), 1)
        self.assertEqual(session2.components.all().count(), 1)

    def test_delete_session(self):
        client1 = Client()
        response = client1.get("")
        client1_id = client1.session.session_key
        session1 = Session.objects.get(pk=client1_id)
        response = client1.post(
            reverse("add_component"),
            {
                "name": "compound1",
                "a": 0,
                "b": 0,
                "c": 0,
            },
        )
        response = client1.post(
            reverse("add_component"),
            {
                "name": "compound2",
                "a": 0,
                "b": 0,
                "c": 0,
            },
        )

        self.assertEqual(session1.components.all().count(), 2)
        self.assertEqual(Session.objects.all().count(), 1)
        c1 = Component.objects.get(name="compound1")
        c2 = Component.objects.get(name="compound2")
        self.assertEqual(
            list(utils.compounds_of_session(client1_id)),
            [self.acetone, self.benzene, self.chloroforme, c1, c2],
        )

        client2 = Client()
        response = client2.get("")
        client2_id = client2.session.session_key
        session2 = Session.objects.get(pk=client2_id)
        session2.components.add(c1)
        self.assertEqual(c1.sessions.count(), 2)
        self.assertEqual(Session.objects.all().count(), 2)

        # deleting session1 will delete c2 since it was only by session1 and
        # will keep c2 instance because it was also added by session2, but c1 won't stay associated with session1
        session1.delete()
        self.assertEqual(Session.objects.all().count(), 1)
        self.assertEqual(
            list(Component.objects.all()),
            [self.acetone, self.chloroforme, self.benzene, c1],
        )
        self.assertEqual(
            Component.objects.filter(name="compound1").exists(), True
        )
        self.assertEqual(
            Component.objects.filter(name="compound2").exists(), False
        )

        self.assertEqual(c1.sessions.count(), 1)
        self.assertEqual(c1.sessions.all()[0], session2)

        # deleting session 2 will remove c2
        session2.delete()
        self.assertEqual(Session.objects.all().count(), 0)
        self.assertEqual(
            Component.objects.filter(name="compound1").exists(), False
        )
        self.assertEqual(Component.objects.all().count(), 3)

    def test_expiration_session(self):
        client = Client()
        response = client.get("")
        client1_id = client.session.session_key
        session1 = Session.objects.get(pk=client1_id)

        c = Component(name="test", a=0, b=0, c=0)
        c.save()
        session1.components.add(c)

        # set expiry of 10 seconds for test
        exp_duration = 2
        session1.expire_date = timezone.now() + timezone.timedelta(
            seconds=exp_duration
        )
        session1.save()

        self.assertEqual(Session.objects.all().count(), 1)
        self.assertEqual(Component.objects.all().count(), 4)

        # print(
        #    "wait 5 seconds for session to expire in order to test its deletion"
        # )
        sleep(exp_duration)

        # session should be expired by now let's create a new session
        # and see if the expired session was cleared
        new_client = Client()
        response = new_client.get("")
        self.assertEqual(Component.objects.filter(name="test").exists(), False)
        self.assertEqual(Session.objects.filter(pk=client1_id).exists(), False)
