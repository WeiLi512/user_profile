# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2019-08-23 03:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20190823_0314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='avatars/'),
        ),
    ]
