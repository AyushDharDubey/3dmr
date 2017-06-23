# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-22 19:23
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Change',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typeof', models.IntegerField()),
                ('datetime', models.DateTimeField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=1024)),
                ('datetime', models.DateTimeField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_id', models.IntegerField()),
                ('revision', models.IntegerField()),
                ('description', models.CharField(max_length=512)),
                ('upload_date', models.DateField()),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('license', models.IntegerField()),
                ('categories', models.ManyToManyField(to='mainapp.Category')),
            ],
        ),
        migrations.CreateModel(
            name='ModelTagValueTagKey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Model')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('description', models.CharField(max_length=2048)),
                ('rendered_description', models.CharField(max_length=4096)),
                ('avatar_url', models.CharField(max_length=256)),
                ('admin', models.BooleanField()),
                ('banned', models.BooleanField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TagKey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='TagValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
            ],
        ),
        migrations.AddField(
            model_name='modeltagvaluetagkey',
            name='tag_key',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.TagKey'),
        ),
        migrations.AddField(
            model_name='modeltagvaluetagkey',
            name='tag_value',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.TagValue'),
        ),
        migrations.AddField(
            model_name='comment',
            name='model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Model'),
        ),
        migrations.AddField(
            model_name='change',
            name='model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Model'),
        ),
    ]
