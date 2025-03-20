from django.apps import AppConfig
from django.db.models.signals import pre_migrate
from django.db import connection

def enable_hstore(sender, **kwargs):
    print("Enabling hstore extension...")
    with connection.cursor() as cursor:
        try:
            cursor.execute("CREATE EXTENSION IF NOT EXISTS hstore;")
            print("hstore extension enabled.")
        except Exception as e:
            print("Failed to enable hstore extension:", e)

class MainappConfig(AppConfig):
    name = 'mainapp'

    def ready(self):
        pre_migrate.connect(enable_hstore, sender=self)
