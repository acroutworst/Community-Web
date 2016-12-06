# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-05 10:05
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100)),
                ('date', models.DateTimeField(verbose_name='notification date')),
                ('status', models.CharField(choices=[('UNSEEN', 'unseen'), ('SEEN', 'seen')], default='UNSEEN', max_length=10)),
                ('object_id', models.PositiveIntegerField(null=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Notifications',
                'verbose_name': 'Notification',
            },
        ),
        migrations.AlterUniqueTogether(
            name='notification',
            unique_together=set([('user', 'id')]),
        ),
    ]
