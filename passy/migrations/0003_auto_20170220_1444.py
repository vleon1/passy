# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-20 12:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passy', '0002_auto_20170217_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storedpassword',
            name='site',
            field=models.CharField(max_length=200),
        ),
    ]