# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-10 00:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djcelery', '0003_auto_20160809_1855'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskmeta',
            name='status',
            field=models.CharField(choices=[('PENDING', 'PENDING'), ('FAILURE', 'FAILURE'), ('RECEIVED', 'RECEIVED'), ('REVOKED', 'REVOKED'), ('SUCCESS', 'SUCCESS'), ('RETRY', 'RETRY'), ('STARTED', 'STARTED')], default='PENDING', max_length=50, verbose_name='state'),
        ),
    ]
