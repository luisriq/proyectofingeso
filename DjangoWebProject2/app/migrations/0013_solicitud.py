# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20150904_0738'),
    ]

    operations = [
        migrations.CreateModel(
            name='solicitud',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('direccion', models.CharField(max_length=3)),
                ('guid', models.CharField(max_length=36)),
                ('artista', models.ForeignKey(related_name='invitado', to='app.Artista', null=True)),
                ('banda', models.ForeignKey(related_name='invita', to='app.Banda', null=True)),
            ],
        ),
    ]
