# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20150618_1532'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mensaje',
            name='usuario',
        ),
        migrations.AddField(
            model_name='mensaje',
            name='usuarioE',
            field=models.ForeignKey(related_name='enviado', to='app.Usuario', null=True),
        ),
        migrations.AddField(
            model_name='mensaje',
            name='usuarioR',
            field=models.ForeignKey(related_name='recibido', to='app.Usuario', null=True),
        ),
    ]
