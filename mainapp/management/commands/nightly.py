from django.core.management.base import BaseCommand, CommandError
from django.utils.dateformat import format
from mainapp.models import LatestModel
from json import dumps
from mainapp.utils import MODEL_DIR
from zipfile import ZipFile

class Command(BaseCommand):
    help = 'Updates the nightly dump'

    def handle(self, *args, **options):
        INFO_FILENAME = 'info.json'
        NIGHTLY_FILENAME = '3dmr-nightly.zip'

        info_file = open(INFO_FILENAME, 'w')
        zip_file = ZipFile(NIGHTLY_FILENAME, 'w')

        models = LatestModel.objects.all()

        info_file.write('{\n')

        first = True
        for model in models.iterator():
            model_id = model.model_id

            if not first:
                info_file.write(',')
            first = False

            output = dumps({
                'author': model.author.username,
                'revision': model.revision,
                'title': model.title,
                'description': model.description,
                'upload_date': format(model.upload_date, 'U'),
                'latitude': model.latitude,
                'longitude': model.longitude,
                'license': model.license,
                'categories': model.categories.all().values_list('name', flat=True)[::1],
                'tags': model.tags,
                'rotation': model.rotation,
                'scale': model.scale,
                'translation': [
                    model.translation_x,
                    model.translation_y,
                    model.translation_z
                ]
            })

            info_file.write(f'"{model_id}": {output}\n')
            zip_file.write(f'{MODEL_DIR}/{model_id}/{model.revision}.zip', f'models/{model_id}.zip')

        info_file.write('}')
        info_file.close()
        zip_file.write(INFO_FILENAME)
        zip_file.close()
