# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20150821_1153'),
    ]

    operations = [
        migrations.AddField(
            model_name='banda',
            name='seguidores',
            field=models.ManyToManyField(to='app.Normal', blank=True),
        ),
    ]
