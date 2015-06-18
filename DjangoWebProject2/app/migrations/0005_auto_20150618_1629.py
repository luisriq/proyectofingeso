# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20150618_1605'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notificacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('texto', models.CharField(max_length=200)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(related_name='notificado', to='app.Usuario', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='comentario',
            name='usuario',
            field=models.ForeignKey(related_name='comentado', to='app.Usuario', null=True),
        ),
        migrations.AlterField(
            model_name='reporte',
            name='administrador',
            field=models.ForeignKey(related_name='reportado', to='app.Administrador', null=True),
        ),
    ]
