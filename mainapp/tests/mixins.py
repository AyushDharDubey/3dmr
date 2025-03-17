from django.contrib.auth.models import User
from social_django.models import UserSocialAuth


class AuthTestMixin:
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        UserSocialAuth.objects.create(
            user=self.user,
            provider='test-provider',
            uid='1234567890',
            extra_data={
                'avatar': 'http://example.com/avatar.jpg'
            }
        )
        self.user.save()
        self.client.login(username='testuser', password='testpassword')
