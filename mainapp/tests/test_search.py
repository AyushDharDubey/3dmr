import json
from django.test import TestCase, Client
from django.urls import reverse
from social_django.models import UserSocialAuth
from .mixins import AuthTestMixin
from mainapp.models import Model, Category, User, Location

class SearchFullTests(AuthTestMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.admin_user = User.objects.create_superuser(username='admin', email='', password='adminpassword')
        UserSocialAuth.objects.create(
            user=self.admin_user,
            provider='test-provider',
            uid='2234567890',
            extra_data={
                'avatar': 'http://example.com/avatar.jpg'
            }
        )
        self.admin_user.save()

        self.model1 = Model.objects.create(
            model_id=1,
            revision=1,
            title='Model 1',
            author=self.user,
            is_hidden=False,
            location=Location.objects.create(latitude=48.8566, longitude=2.3522),
            tags={'color': 'red', 'size': 'large'},
            license=0,
        )
        self.model1.categories.set([Category.objects.create(name='category1')])

        self.model2 = Model.objects.create(
            model_id=2,
            revision=1,
            title='Model 2',
            author=self.admin_user,
            is_hidden=True,
            location=Location.objects.create(latitude=2.3522, longitude=48.8566),
            tags={'color': 'blue', 'size': 'small'},
            license=1,
        )
        self.model2.categories.set([Category.objects.create(name='category2')])

        self.model3 = Model.objects.create(
            model_id=3,
            revision=1,
            title='Model 3',
            author=self.user,
            is_hidden=False,
            location=Location.objects.create(latitude=2.3522, longitude=48.8566),
            tags={'color': 'blue', 'size': 'small'},
            license=1,
        )
        self.model3.categories.set([Category.objects.create(name='category3')])

    def test_search_full_author_filter(self):
        payload = {
            'author': 'testuser',
            'format': ['id', 'title']
        }
        response = self.client.post(
            reverse('search_full'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.content)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0][1], 'Model 1')  # Check title
        self.assertEqual(results[1][1], 'Model 3')

    def test_search_full_location_filter(self):
        # Test filtering by location
        payload = {
            'lat': 48.8566,
            'lon': 2.3522,
            'range': 1000,  # Range in meters
            'format': ['id', 'title']
        }
        response = self.client.post(
            reverse('search_full'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.content)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][1], 'Model 1')  # Check title

    def test_search_full_title_filter(self):
        payload = {
            'title': 'Model',
            'format': ['id', 'title']
        }
        response = self.client.post(
            reverse('search_full'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.content)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0][1], 'Model 1')  # Check title
        self.assertEqual(results[1][1], 'Model 3')

    def test_search_full_tags_filter(self):
        # Test filtering by tags
        payload = {
            'tags': {'color': 'red'},
            'format': ['id', 'title']
        }
        response = self.client.post(
            reverse('search_full'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.content)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][1], 'Model 1')  # Check title

    def test_search_full_categories_filter(self):
        # Test filtering by categories
        payload = {
            'categories': ['category1'],
            'format': ['id', 'title']
        }
        response = self.client.post(
            reverse('search_full'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.content)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][1], 'Model 1')  # Check title

    def test_search_full_pagination(self):
        # Test pagination
        payload = {
            'page': 1,
            'format': ['id', 'title']
        }
        response = self.client.post(
            reverse('search_full'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.content)
        self.assertEqual(len(results), 2)  # Both models should be returned

    def test_search_full_invalid_format(self):
        # Test invalid format specifier
        payload = {
            'format': ['invalid']
        }
        response = self.client.post(
            reverse('search_full'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(), 'Invalid format specifier')

    def test_search_full_admin_access(self):
        # Test admin access to hidden models
        self.client.login(username='admin', password='adminpassword')
        payload = {
            'format': ['id', 'title']
        }
        response = self.client.post(
            reverse('search_full'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.content)
        self.assertEqual(len(results), 2)  # Admin can see hidden models