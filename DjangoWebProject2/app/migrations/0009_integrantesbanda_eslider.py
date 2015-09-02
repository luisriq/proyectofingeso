# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_banda_fechacreacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='integrantesbanda',
            name='esLider',
            field=models.BooleanField(default=False),
        ),
    ]
