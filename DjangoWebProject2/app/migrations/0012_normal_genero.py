# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_genero'),
    ]

    operations = [
        migrations.AddField(
            model_name='normal',
            name='genero',
            field=models.ManyToManyField(to='app.Genero'),
        ),
    ]
