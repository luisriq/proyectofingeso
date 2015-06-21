# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_auto_20150620_2302'),
    ]

    operations = [
        migrations.CreateModel(
            name='Noticia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contenido', models.CharField(max_length=200)),
                ('banda', models.ForeignKey(related_name='trata_de', to='app.Banda')),
            ],
        ),
        migrations.AlterField(
            model_name='evento',
            name='bandas',
            field=models.ForeignKey(related_name='organiza', to='app.Banda'),
        ),
    ]
