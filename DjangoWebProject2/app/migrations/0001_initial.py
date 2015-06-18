# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banda',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('texto', models.CharField(max_length=200)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Mensaje',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('texto', models.CharField(max_length=200)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reporte',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('justificacion', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=200)),
                ('correo', models.EmailField(unique=True, max_length=254)),
                ('contrasena', models.CharField(max_length=200)),
                ('fechaIngreso', models.DateTimeField(auto_now_add=True)),
                ('imagenPerfil', models.CharField(max_length=200, blank=True)),
                ('usuarioActivo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Administrador',
            fields=[
                ('usuario_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='app.Usuario')),
            ],
            bases=('app.usuario',),
        ),
        migrations.CreateModel(
            name='Artista',
            fields=[
                ('usuario_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='app.Usuario')),
                ('biografia', models.TextField()),
                ('imagenCabecera', models.CharField(max_length=200)),
            ],
            bases=('app.usuario',),
        ),
        migrations.CreateModel(
            name='Normal',
            fields=[
                ('usuario_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='app.Usuario')),
                ('tiempoCastigo', models.IntegerField(default=0)),
                ('descripcion', models.TextField(blank=True)),
            ],
            bases=('app.usuario',),
        ),
        migrations.AddField(
            model_name='mensaje',
            name='Usuario',
            field=models.ForeignKey(to='app.Usuario'),
        ),
        migrations.AddField(
            model_name='reporte',
            name='Administrador',
            field=models.ForeignKey(to='app.Administrador'),
        ),
    ]
