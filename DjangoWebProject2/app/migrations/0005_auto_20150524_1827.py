# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_musico_banda'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='musico',
            name='banda',
        ),
        migrations.AddField(
            model_name='musico',
            name='banda',
            field=models.ManyToManyField(to='app.Banda', null=True),
        ),
    ]
