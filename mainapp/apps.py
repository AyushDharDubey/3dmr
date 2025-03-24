import logging

from django.apps import AppConfig
from django.db.models.signals import pre_migrate
from django.db import connection

logger = logging.getLogger(__name__)

def enable_hstore(sender, **kwargs):
    logger.info("Enabling hstore extension...")
    with connection.cursor() as cursor:
        try:
            cursor.execute("CREATE EXTENSION IF NOT EXISTS hstore;")
            logger.info("hstore extension enabled successfully.")
        except Exception as e:
            logging.error("Failed to enable hstore extension.", exc_info=True)
            raise RuntimeError("hstore installation failed.") from e

class MainappConfig(AppConfig):
    name = 'mainapp'

    def ready(self):
        pre_migrate.connect(enable_hstore, sender=self)
