"""modelrepository URL Configuration"""

from django.urls import include, path
from django.contrib import admin
from django.conf import settings

urlpatterns = [
    path('', include('mainapp.urls')),
    path('', include('social_django.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        path('admin/', admin.site.urls),
    ]
