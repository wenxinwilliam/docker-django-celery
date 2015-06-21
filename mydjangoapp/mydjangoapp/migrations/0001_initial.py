# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('type', models.CharField(max_length=20, choices=[('fibonacci', 'fibonacci'), ('power', 'power'), ('sleepwake', 'sleepwake'), ('syncsleepwake', 'syncsleepwake')])),
                ('status', models.CharField(max_length=20, choices=[('pending', 'pending'), ('started', 'started'), ('finished', 'finished'), ('failed', 'failed')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('argument', models.PositiveIntegerField()),
                ('result', models.IntegerField(null=True)),
            ],
        ),
    ]
