# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_banda_biografia'),
    ]

    operations = [
        migrations.AddField(
            model_name='artista',
            name='cuentaTwitter',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='banda',
            name='cuentaTwitter',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='banda',
            name='imagenPerfil',
            field=models.ImageField(default=b'pic_folder/None/no-img.jpg', upload_to=b'app/static/app/images'),
        ),
        migrations.AlterField(
            model_name='banda',
            name='imagenPortada',
            field=models.ImageField(default=b'pic_folder/None/no-img.jpg', upload_to=b'app/static/app/images'),
        ),
        migrations.AlterField(
            model_name='instrumento',
            name='imagen',
            field=models.ImageField(default=b'pic_folder/None/no-img.jpg', upload_to=b'app/static/app/images'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='imagenPerfil',
            field=models.ImageField(default=b'pic_folder/None/no-img.jpg', upload_to=b'app/static/app/images'),
        ),
    ]
