# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_auto_20150912_1732'),
    ]

    operations = [
        migrations.AddField(
            model_name='cancion',
            name='duracion',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
