# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_remove_banda_integrante'),
    ]

    operations = [
        migrations.CreateModel(
            name='IntegrantesBanda',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fechaIngreso', models.DateField()),
                ('ocupacion', models.CharField(max_length=200)),
                ('banda', models.ForeignKey(related_name='integrante1', to='app.Banda', null=True)),
                ('integrante', models.ForeignKey(related_name='pertenece1', to='app.Artista', null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='integrante',
            name='artistaIntegrante',
        ),
        migrations.RemoveField(
            model_name='integrante',
            name='bandaPertenece',
        ),
        migrations.DeleteModel(
            name='Integrante',
        ),
        migrations.AddField(
            model_name='banda',
            name='integrantes',
            field=models.ManyToManyField(to='app.Artista', through='app.IntegrantesBanda'),
        ),
    ]
