# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banda',
            name='imagenPortada',
            field=models.ImageField(default=b'pic_folder/None/no-portada.jpg', upload_to=b'app/static/app/images'),
        ),
    ]
