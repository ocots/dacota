from django.apps import AppConfig


class TernaryAzeotropeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ternary_azeotrope"

    def ready(self) -> None:
        from . import signals
