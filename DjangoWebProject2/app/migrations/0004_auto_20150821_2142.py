# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_banda_seguidores'),
    ]

    operations = [
        migrations.CreateModel(
            name='Toca',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nivel', models.IntegerField()),
                ('artista', models.ForeignKey(related_name='tocador', to='app.Artista', null=True)),
                ('instrumento', models.ForeignKey(related_name='tocacion', to='app.Instrumento', null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='banda',
            name='integrantes',
        ),
    ]
