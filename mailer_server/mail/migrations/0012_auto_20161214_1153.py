# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-14 09:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0011_auto_20161018_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mail',
            name='mail_from',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='mail',
            name='reply_to',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]