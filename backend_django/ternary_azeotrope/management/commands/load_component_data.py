from csv import DictReader

from django.core.management import BaseCommand
from ternary_azeotrope.models import BinaryRelation, Component

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the component data from the CSV file, first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty database with tables.
Note that you will have to create the superuser again,
to do so run `python manage.py createsuperuser` (it's best to give the same username and password as the one given) and follow the prompts.
Then run `python manage.py load_component_data` to load the component data from the CSV file. """


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from component_data.csv"

    def handle(self, *args, **options):
        if Component.objects.exists():
            print("Some component data are already loaded...exiting.")
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        print("Loading component data...")
        for row in DictReader(open("./component_data.csv")):
            component = Component()
            component.name = row["name"]
            component.a = row["a"]
            component.b = row["b"]
            component.c = row["c"]
            component.save()

        print("Loading binary relation data...")
        for row in DictReader(open("./binary_relation_data.csv")):
            relation = BinaryRelation()
            relation.component1 = Component.objects.get(name=row["component1"])
            relation.component2 = Component.objects.get(name=row["component2"])
            relation.a12 = row["a12"]
            relation.a21 = row["a21"]
            relation.alpha = row["alpha"]
            relation.save()
