# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20150821_2233'),
    ]

    operations = [
        migrations.AddField(
            model_name='banda',
            name='biografia',
            field=models.TextField(default=1234),
            preserve_default=False,
        ),
    ]
