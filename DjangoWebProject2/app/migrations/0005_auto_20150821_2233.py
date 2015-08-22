# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20150821_2142'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artista',
            name='imagenCabecera',
        ),
        migrations.RemoveField(
            model_name='instrumento',
            name='artista',
        ),
        migrations.RemoveField(
            model_name='instrumento',
            name='nombre',
        ),
        migrations.AlterField(
            model_name='instrumento',
            name='imagen',
            field=models.ImageField(default=b'pic_folder/None/no-img.jpg', upload_to=b'static/app/images'),
        ),
    ]
