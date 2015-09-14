# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_cancion_duracion'),
    ]

    operations = [
        migrations.AddField(
            model_name='material',
            name='color',
            field=models.CharField(default=b'red', max_length=200),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='direccion',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='guid',
            field=models.CharField(max_length=36, null=True),
        ),
    ]
