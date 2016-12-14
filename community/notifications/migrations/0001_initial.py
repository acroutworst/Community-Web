# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-11 23:07
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
            name='Notification',
            fields=[
                ('notification_id', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=100)),
                ('date', models.DateTimeField(verbose_name='notification date')),
                ('status', models.CharField(choices=[('UNSEEN', 'unseen'), ('SEEN', 'seen')], default='UNSEEN', max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Notification',
                'verbose_name_plural': 'Notifications',
            },
        ),
        migrations.AlterUniqueTogether(
            name='notification',
            unique_together=set([('user', 'notification_id')]),
        ),
    ]
