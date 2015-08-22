# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='banda',
            name='imagenPerfil',
            field=models.ImageField(default=b'pic_folder/None/no-img.jpg', upload_to=b'static/app/images'),
        ),
        migrations.AddField(
            model_name='banda',
            name='imagenPortada',
            field=models.ImageField(default=b'pic_folder/None/no-img.jpg', upload_to=b'static/app/images'),
        ),
        migrations.AlterField(
            model_name='artista',
            name='seguidores',
            field=models.ManyToManyField(to='app.Normal', blank=True),
        ),
        migrations.AlterField(
            model_name='instrumento',
            name='cancion',
            field=models.ManyToManyField(to='app.Cancion', blank=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='user',
            field=models.OneToOneField(related_name='profile', null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
