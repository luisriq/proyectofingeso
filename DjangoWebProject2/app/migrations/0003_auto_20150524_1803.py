# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_usuario_rut'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='edad',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='rut',
        ),
        migrations.AlterField(
            model_name='usuario',
            name='nombre',
            field=models.CharField(max_length=20),
        ),
    ]
