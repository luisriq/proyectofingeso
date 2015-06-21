# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_normal_genero'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='genero',
            name='banda',
        ),
        migrations.AddField(
            model_name='banda',
            name='genero',
            field=models.ForeignKey(related_name='tocado_por', default=1, to='app.Genero'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='normal',
            name='genero',
            field=models.ManyToManyField(related_name='prefiere', to='app.Genero'),
        ),
    ]
