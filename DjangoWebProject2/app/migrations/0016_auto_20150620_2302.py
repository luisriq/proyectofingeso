# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_evento_bandas'),
    ]

    operations = [
        migrations.CreateModel(
            name='Asiste',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pagado', models.BooleanField()),
                ('evento', models.ForeignKey(to='app.Evento', null=True)),
                ('normal', models.ForeignKey(to='app.Normal', null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='integrantesbanda',
            name='banda',
            field=models.ForeignKey(related_name='integrante', to='app.Banda', null=True),
        ),
        migrations.AddField(
            model_name='evento',
            name='evento',
            field=models.ManyToManyField(to='app.Normal', through='app.Asiste'),
        ),
    ]
