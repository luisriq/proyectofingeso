# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_mensajebanda'),
    ]

    operations = [
        migrations.AddField(
            model_name='comentario',
            name='material',
            field=models.ForeignKey(related_name='comenta', to='app.Material', null=True),
        ),
    ]
