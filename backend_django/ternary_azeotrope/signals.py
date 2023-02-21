from django.contrib.sessions.models import Session
from django.db.models.signals import post_delete, pre_delete
from django.dispatch import receiver

from .helpers import utils


@receiver(pre_delete, sender=Session)
def pre_delete_session(sender, instance, **kwargs):
    print(f"deleting session {instance.pk} and clearing its data ...")

    instance = Session.objects.prefetch_related("components", "relations").get(
        pk=instance.pk
    )
    utils.clear_session_data(
        session_key=instance.pk,
        compounds=instance.components.all(),
        relations=instance.relations.all(),
    )


@receiver(post_delete, sender=Session)
def post_delete_session(sender, **kwargs):
    print("You have just deleted a Session!!!")
