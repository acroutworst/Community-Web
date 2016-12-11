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
        ('communities', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_created=True, verbose_name='date created')),
                ('description', models.CharField(blank=True, max_length=300, null=True)),
                ('title', models.CharField(max_length=50)),
                ('active', models.BooleanField(default=True)),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='communities.Community')),
                ('create_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GroupMembers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('join_date', models.DateTimeField(auto_created=True, verbose_name='date joined')),
                ('position', models.CharField(blank=True, max_length=30, null=True)),
                ('last_activity', models.CharField(blank=True, max_length=300, null=True)),
                ('active', models.BooleanField(default=True)),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='communities.Community')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='groups.Group')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='group',
            name='current_leader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leader', to='groups.GroupMembers'),
        ),
        migrations.AlterUniqueTogether(
            name='groupmembers',
            unique_together=set([('user', 'community', 'group')]),
        ),
        migrations.AlterUniqueTogether(
            name='group',
            unique_together=set([('community', 'id')]),
        ),
    ]
