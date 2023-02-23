from django.contrib.sessions.models import Session
from django.db.models import Q
from django.test import Client, TestCase
from django.urls import reverse

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

        self.client1 = Client()
        self.client2 = Client()
        r1 = self.client1.get("")
        r2 = self.client2.get("")
        self.session_id1 = self.client1.session.session_key
        self.session_id2 = self.client2.session.session_key
        self.compounds = [self.acetone, self.benzene, self.chloroforme]
        self.session1 = Session.objects.get(pk=self.session_id1)
        self.session2 = Session.objects.get(pk=self.session_id2)

    def test_edit_component(self):
        # two client adding the same components
        self.client1.post(
            reverse("add_component"),
            {
                "name": "compound1",
                "a": 0,
                "b": 0,
                "c": 0,
            },
        )

        self.client2.post(
            reverse("add_component"),
            {
                "name": "compound1",
                "a": 0,
                "b": 0,
                "c": 0,
            },
        )

        c1 = Component.objects.get(name="compound1")
        self.assertEqual(
            list(utils.compounds_of_session(self.session_id2)),
            self.compounds + [c1],
        )

        self.assertEqual(c1.sessions.count(), 2)

        # client 2 will edit compound 1 that was also added by client 2 so a new instance will be created for the edited compound
        self.client2.post(
            reverse("edit_component"),
            {
                "id": c1.id,
                "name": "compound2",
                "a": 1,
                "b": 0,
                "c": 0,
            },
        )

        # a new instance is created
        self.assertEqual(
            Component.objects.filter(name="compound2").exists(), True
        )

        # the previous compound still  exists
        self.assertEqual(
            Component.objects.filter(name="compound1").exists(), True
        )

        # session 2 no longer assigned to c1
        self.assertEqual(list(c1.sessions.all()), [self.session1])

        # c2 assigned to session 2
        c2 = Component.objects.get(name="compound2")
        self.assertEqual(list(c2.sessions.all()), [self.session2])
        self.assertEqual(
            list(utils.compounds_of_session(self.session_id2)),
            self.compounds + [c2],
        )

    def test_edit_relation(self):
        pass
