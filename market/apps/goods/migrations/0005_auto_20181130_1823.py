# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-30 18:23
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0004_auto_20181124_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopspu',
            name='detail',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='详情'),
        ),
    ]
