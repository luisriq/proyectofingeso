# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_evento'),
    ]

    operations = [
        migrations.AddField(
            model_name='evento',
            name='bandas',
            field=models.ForeignKey(related_name='toca_en', default=1, to='app.Banda'),
            preserve_default=False,
        ),
    ]
