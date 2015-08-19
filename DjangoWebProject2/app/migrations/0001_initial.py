# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Asiste',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pagado', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Banda',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Calificacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('valor', models.IntegerField()),
                ('fecha', models.DateField()),
                ('banda', models.ForeignKey(related_name='calificado', to='app.Banda')),
            ],
        ),
        migrations.CreateModel(
            name='Cancion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=200)),
                ('autor', models.CharField(max_length=200)),
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
            name='Evento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=200)),
                ('fecha', models.DateField()),
                ('lugar', models.CharField(max_length=200)),
                ('asistentes', models.IntegerField()),
                ('precioEntrada', models.IntegerField()),
                ('bandas', models.ForeignKey(related_name='organiza', to='app.Banda')),
            ],
        ),
        migrations.CreateModel(
            name='Genero',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Instrumento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=200)),
                ('tipo', models.CharField(max_length=200)),
                ('imagen', models.CharField(max_length=200)),
                ('cancion', models.ManyToManyField(to='app.Cancion', null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='IntegrantesBanda',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fechaIngreso', models.DateField()),
                ('ocupacion', models.CharField(max_length=200)),
                ('banda', models.ForeignKey(related_name='integrante', to='app.Banda', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=200)),
                ('enlace', models.CharField(max_length=200)),
                ('descripcion', models.CharField(max_length=200)),
                ('tipo', models.CharField(max_length=200)),
                ('privado', models.BooleanField()),
                ('banda', models.ForeignKey(related_name='publica', to='app.Banda')),
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
            name='MensajeBanda',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('texto', models.CharField(max_length=200)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('bandaE', models.ForeignKey(related_name='enviado', to='app.Banda', null=True)),
                ('bandaR', models.ForeignKey(related_name='recibido', to='app.Banda', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Noticia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contenido', models.CharField(max_length=200)),
                ('nombre', models.CharField(max_length=200)),
                ('fuente', models.CharField(max_length=200)),
                ('banda', models.ForeignKey(related_name='trata_de', to='app.Banda')),
            ],
        ),
        migrations.CreateModel(
            name='Notificacion',
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
                ('usuarioActivo', models.BooleanField(default=True)),
                ('imagenPerfil', models.ImageField(default=b'pic_folder/None/no-img.jpg', upload_to=b'static/app/images')),
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
                ('genero', models.ManyToManyField(related_name='prefiere', to='app.Genero')),
            ],
            bases=('app.usuario',),
        ),
        migrations.AddField(
            model_name='usuario',
            name='user',
            field=models.OneToOneField(null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='notificacion',
            name='usuario',
            field=models.ForeignKey(related_name='notificado', to='app.Usuario', null=True),
        ),
        migrations.AddField(
            model_name='mensaje',
            name='usuarioE',
            field=models.ForeignKey(related_name='enviado', to='app.Usuario', null=True),
        ),
        migrations.AddField(
            model_name='mensaje',
            name='usuarioR',
            field=models.ForeignKey(related_name='recibido', to='app.Usuario', null=True),
        ),
        migrations.AddField(
            model_name='comentario',
            name='material',
            field=models.ForeignKey(related_name='comenta', to='app.Material', null=True),
        ),
        migrations.AddField(
            model_name='comentario',
            name='usuario',
            field=models.ForeignKey(related_name='comentado', to='app.Usuario', null=True),
        ),
        migrations.AddField(
            model_name='banda',
            name='genero',
            field=models.ForeignKey(related_name='tocado_por', to='app.Genero'),
        ),
        migrations.AddField(
            model_name='asiste',
            name='evento',
            field=models.ForeignKey(to='app.Evento', null=True),
        ),
        migrations.AddField(
            model_name='reporte',
            name='administrador',
            field=models.ForeignKey(related_name='reportado', to='app.Administrador', null=True),
        ),
        migrations.AddField(
            model_name='integrantesbanda',
            name='integrante',
            field=models.ForeignKey(related_name='perteneciente', to='app.Artista', null=True),
        ),
        migrations.AddField(
            model_name='instrumento',
            name='artista',
            field=models.ForeignKey(related_name='instrumentos', blank=True, to='app.Artista', null=True),
        ),
        migrations.AddField(
            model_name='evento',
            name='evento',
            field=models.ManyToManyField(to='app.Normal', through='app.Asiste'),
        ),
        migrations.AddField(
            model_name='calificacion',
            name='normal',
            field=models.ForeignKey(related_name='califica', to='app.Normal'),
        ),
        migrations.AddField(
            model_name='banda',
            name='integrantes',
            field=models.ManyToManyField(to='app.Artista', through='app.IntegrantesBanda'),
        ),
        migrations.AddField(
            model_name='asiste',
            name='normal',
            field=models.ForeignKey(to='app.Normal', null=True),
        ),
        migrations.AddField(
            model_name='artista',
            name='seguidores',
            field=models.ManyToManyField(to='app.Normal', null=True, blank=True),
        ),
    ]
