from django.test import TestCase
from mainapp.models import Model
from .mixins import AuthTestMixin
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from mainapp.utils import MODEL_DIR
import os


class TestUpload(AuthTestMixin, TestCase):
    def test_upload_get(self):
        response = self.client.get(reverse('upload'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Upload Model')

    def test_upload_post(self):
        with open('mainapp/tests/models/test_model.zip', 'rb') as f:
            file_content = f.read()

        model_file = SimpleUploadedFile(
            name='test_model.zip',
            content=file_content,
            content_type='application/zip'
        )

        response = self.client.post(reverse('upload'), {
            'title': 'Test Model',
            'description': 'This is a test model',
            'latitude': '2.48',
            'longitude': '48.84',
            'categories': 'tc1, tc2',
            'tags': '',
            'translation': '0.0 0.0 0.0',
            'rotation': 0,
            'scale': 1.0,
            'license': 0,
            'model_file': model_file,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Model.objects.count(), 1)
        self.assertEqual(Model.objects.first().title, 'Test Model')
        self.assertEqual(Model.objects.first().description, 'This is a test model')
        self.assertEqual(Model.objects.first().categories.count(), 2)
        self.assertSetEqual(
            set(Model.objects.first().categories.values_list('name', flat=True)),
            {'tc1', 'tc2'}
        )
        self.assertEqual(Model.objects.first().translation_x, 0.0)
        self.assertEqual(Model.objects.first().translation_y, 0.0)
        self.assertEqual(Model.objects.first().translation_z, 0.0)
        self.assertEqual(Model.objects.first().rotation, 0)
        self.assertEqual(Model.objects.first().scale, 1.0)
        self.assertEqual(Model.objects.first().license, 0)
        self.assertEqual(Model.objects.first().revision, 1)
        self.assertEqual(Model.objects.first().author, self.user)
        self.assertEqual(Model.objects.first().location.latitude, 2.48)
        self.assertEqual(Model.objects.first().location.longitude, 48.84)

        filepath = '{}/{}/{}.zip'.format(MODEL_DIR, response.url.split('/')[2], '1')
        assert os.path.exists(filepath)
        os.remove(filepath)
        os.rmdir('{}/{}'.format(MODEL_DIR, response.url.split('/')[2]))
        