# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-02-02 16:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20180125_1330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(default='image/default.png', upload_to='image/user/%Y/%m'),
        ),
    ]
