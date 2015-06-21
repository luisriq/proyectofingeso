# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_auto_20150620_2134'),
    ]

    operations = [
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=200)),
                ('fecha', models.DateField()),
                ('lugar', models.CharField(max_length=200)),
                ('asistentes', models.IntegerField()),
                ('precioEntrada', models.IntegerField()),
            ],
        ),
    ]
