# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-15 00:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('events', '0001_initial'),
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='groups.Group'),
        ),
        migrations.AddField(
            model_name='event',
            name='image',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='current_event_image', to='events.EventImage'),
        ),
        migrations.AlterUniqueTogether(
            name='eventimage',
            unique_together=set([('event', 'id')]),
        ),
        migrations.AlterUniqueTogether(
            name='eventattendee',
            unique_together=set([('user', 'event')]),
        ),
    ]
