# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_auto_20150914_1449'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitud',
            name='ocupacion',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
