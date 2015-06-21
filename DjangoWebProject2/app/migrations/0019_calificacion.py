# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_auto_20150621_1015'),
    ]

    operations = [
        migrations.CreateModel(
            name='Calificacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('valor', models.IntegerField()),
                ('fecha', models.DateField()),
                ('banda', models.ForeignKey(related_name='calificado', to='app.Banda')),
                ('normal', models.ForeignKey(related_name='califica', to='app.Normal')),
            ],
        ),
    ]
