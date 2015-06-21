# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_cancion_instrumento'),
    ]

    operations = [
        migrations.CreateModel(
            name='Integrante',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('artistaIntegrante', models.ForeignKey(related_name='pertenece1', to='app.Artista', null=True)),
                ('bandaPertenece', models.ForeignKey(related_name='integrante1', to='app.Banda', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='banda',
            name='integrante',
            field=models.ManyToManyField(related_name='Integrante', through='app.Integrante', to='app.Artista'),
        ),
    ]
