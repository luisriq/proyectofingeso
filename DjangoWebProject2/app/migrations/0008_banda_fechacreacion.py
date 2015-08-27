# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20150827_0746'),
    ]

    operations = [
        migrations.AddField(
            model_name='banda',
            name='fechaCreacion',
            field=models.DateField(null=True),
        ),
    ]
