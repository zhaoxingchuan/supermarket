# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-24 10:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0002_auto_20181123_1756'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopcategory',
            name='oreder',
            field=models.SmallIntegerField(default=0, verbose_name='排序'),
        ),
    ]