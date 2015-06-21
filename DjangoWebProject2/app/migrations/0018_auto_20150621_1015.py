# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_auto_20150621_1008'),
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=200)),
                ('enlace', models.CharField(max_length=200)),
                ('descripcion', models.CharField(max_length=200)),
                ('tipo', models.CharField(max_length=200)),
                ('privado', models.BooleanField()),
                ('banda', models.ForeignKey(related_name='publica', to='app.Banda')),
            ],
        ),
        migrations.AddField(
            model_name='noticia',
            name='fuente',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='noticia',
            name='nombre',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
