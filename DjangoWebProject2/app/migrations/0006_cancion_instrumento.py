# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20150618_1629'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cancion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=200)),
                ('autor', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Instrumento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=200)),
                ('tipo', models.CharField(max_length=200)),
                ('imagen', models.CharField(max_length=200)),
                ('artista', models.ForeignKey(related_name='instrumentos', to='app.Artista', null=True)),
                ('cancion', models.ManyToManyField(to='app.Cancion')),
            ],
        ),
    ]
