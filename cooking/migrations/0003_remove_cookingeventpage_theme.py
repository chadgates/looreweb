# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-15 13:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cooking', '0002_cookingeventindexpage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cookingeventpage',
            name='theme',
        ),
    ]
