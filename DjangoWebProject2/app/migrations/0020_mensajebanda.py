# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_calificacion'),
    ]

    operations = [
        migrations.CreateModel(
            name='MensajeBanda',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('texto', models.CharField(max_length=200)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('bandaE', models.ForeignKey(related_name='enviado', to='app.Banda', null=True)),
                ('bandaR', models.ForeignKey(related_name='recibido', to='app.Banda', null=True)),
            ],
        ),
    ]
