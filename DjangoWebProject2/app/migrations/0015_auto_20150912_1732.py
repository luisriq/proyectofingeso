# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_remove_usuario_contrasena'),
    ]

    operations = [
        migrations.CreateModel(
            name='Disco',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=200)),
                ('lanzamiento', models.DateField()),
                ('banda', models.ForeignKey(related_name='pertenece', to='app.Banda', null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='instrumento',
            name='cancion',
        ),
        migrations.AddField(
            model_name='cancion',
            name='disco',
            field=models.ForeignKey(related_name='pertenece', to='app.Disco', null=True),
        ),
    ]
