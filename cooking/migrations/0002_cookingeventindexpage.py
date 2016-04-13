# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-10 21:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0028_merge'),
        ('cooking', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CookingEventIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'verbose_name': 'Cooking Events index',
            },
            bases=('wagtailcore.page',),
        ),
    ]
