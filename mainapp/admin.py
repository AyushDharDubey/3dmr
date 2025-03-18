from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Profile)
admin.site.register(models.Category)
admin.site.register(models.Location)
admin.site.register(models.Model)
admin.site.register(models.LatestModel)
admin.site.register(models.ModelCategories)
admin.site.register(models.Change)
admin.site.register(models.Comment)
admin.site.register(models.Ban)