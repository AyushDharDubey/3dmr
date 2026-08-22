from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def populate_uploader_field(apps, schema_editor):
    """
    Existing revisions were always uploaded by their author.
    """

    db_alias = schema_editor.connection.alias
    Model = apps.get_model("mainapp", "Model")
    Model.objects.using(db_alias).update(uploader=models.F("author"))


def reverse_populate_uploader_field(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    Model = apps.get_model("mainapp", "Model")
    Model.objects.using(db_alias).update(uploader=None)


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0007_update_osm_oauth2_provider'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='model',
            name='uploader',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='uploaded_models', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RunPython(populate_uploader_field, reverse_populate_uploader_field),
    ]
