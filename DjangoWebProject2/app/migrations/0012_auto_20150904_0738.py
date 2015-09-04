# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20150903_1112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instrumento',
            name='imagen',
            field=models.CharField(max_length=200),
        ),
    ]
