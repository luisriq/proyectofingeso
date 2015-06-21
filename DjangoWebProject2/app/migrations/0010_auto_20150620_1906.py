# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20150620_1902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='integrantesbanda',
            name='banda',
            field=models.ForeignKey(related_name='iintegrante', to='app.Banda', null=True),
        ),
        migrations.AlterField(
            model_name='integrantesbanda',
            name='integrante',
            field=models.ForeignKey(related_name='perteneciente', to='app.Artista', null=True),
        ),
    ]
