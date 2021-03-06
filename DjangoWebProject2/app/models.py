"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import User
import uuid
# Crear modelos aqui.


class Usuario(models.Model):
	user = models.OneToOneField(User, null=True, related_name="profile")
	nombre = models.CharField(max_length=200)
	correo = models.EmailField(unique=True)
	fechaIngreso =  models.DateTimeField(auto_now_add=True)
	usuarioActivo = models.BooleanField(default=True)
	imagenPerfil = models.ImageField(upload_to = 'app/static/app/images', default = 'pic_folder/None/no-img.jpg')
	def __unicode__(self):
		return self.nombre + " / " + self.correo

class Artista(Usuario):
	biografia	 = models.TextField()
	seguidores = models.ManyToManyField("Normal", blank=True)
	cuentaTwitter = models.CharField(max_length=200, null = True)
	
class Administrador(Usuario):	
	pass
	
class Reporte(models.Model):
	justificacion = models.CharField(max_length=200)
	administrador = models.ForeignKey(Administrador, related_name = 'reportado', null=True)
	def __unicode__(self):
		return self.justificacion

class Genero(models.Model):
	nombre = models.CharField(max_length=200)
	def __unicode__(self):
		return self.nombre
	
class Banda(models.Model):
	nombre = models.CharField(max_length=200)
	biografia = models.TextField()
	#integrantes = models.ManyToManyField(Artista, through = 'IntegrantesBanda')
	genero = models.ForeignKey(Genero, related_name = 'tocado_por')
	imagenPerfil = models.ImageField(upload_to = 'app/static/app/images', default = 'pic_folder/None/no-img.jpg')
	imagenPortada = models.ImageField(upload_to = 'app/static/app/images', default = 'pic_folder/None/no-portada.jpg')
	seguidores = models.ManyToManyField("Normal", blank=True)
	cuentaTwitter = models.CharField(max_length=200, null = True)
	fechaCreacion = models.DateField(null = True)
	def __unicode__(self):
		return self.nombre
		
class IntegrantesBanda(models.Model):
	integrante = models.ForeignKey(Artista, related_name = 'perteneciente', null=True)
	banda = models.ForeignKey(Banda, related_name = 'integrante', null=True)
	esLider = models.BooleanField(default=False)
	fechaIngreso = models.DateField()
	ocupacion = models.CharField(max_length=200)
	def __unicode__(self):
		return self.integrante.nombre + "----" + self.banda.nombre


class Notificacion(models.Model):
	texto = models.CharField(max_length=200)
	fecha = models.DateTimeField(auto_now_add=True)
	usuario = models.ForeignKey(Usuario, related_name = 'notificado', null=True)
	def __unicode__(self):
		return self.texto

class Mensaje(models.Model):
	texto = models.CharField(max_length=200)
	fecha = models.DateTimeField(auto_now_add=True)
	usuarioE = models.ForeignKey(Usuario, related_name = 'enviado', null=True)
	usuarioR = models.ForeignKey(Usuario, related_name = 'recibido', null=True)
	def __unicode__(self):
		return self.texto

class Disco(models.Model):
	nombre = models.CharField(max_length=200)
	banda = models.ForeignKey(Banda, related_name = 'pertenece', null=True)
	lanzamiento = models.DateField()
	def __unicode__(self):
		return self.nombre
	

class Cancion(models.Model):
	nombre = models.CharField(max_length=200)
	autor = models.CharField(max_length=200)
	disco = models.ForeignKey(Disco, related_name = 'pertenece', null=True)
	duracion = models.CharField(max_length=200 , null=True)
	def __unicode__(self):
		return self.nombre
		
class Instrumento(models.Model):
	tipo = models.CharField(max_length=200)
	imagen = models.CharField(max_length=200)
	#imagen = models.ImageField(upload_to = 'app/static/app/images', default = 'pic_folder/None/no-img.jpg')
	#artista = models.ForeignKey(Artista, related_name = 'instrumentos', null=True, blank=True)
	def __unicode__(self):
		return self.tipo
	
class Toca(models.Model):
	instrumento = models.ForeignKey(Instrumento, related_name = 'tocacion', null=True)
	artista = models.ForeignKey(Artista, related_name = 'tocador', null=True)
	nivel = models.IntegerField()
	def __unicode__(self):
		return self.instrumento.tipo + "----" + self.artista.nombre
	
	
class Normal(Usuario):
	tiempoCastigo = models.IntegerField(default=0)
	descripcion = models.TextField(blank=True)
	genero = models.ManyToManyField(Genero, related_name = 'prefiere')
		
class Evento(models.Model):
	titulo = models.CharField(max_length=200)
	fecha = models.DateField()
	lugar = models.CharField(max_length=200)
	asistentes = models.IntegerField()
	precioEntrada = models.IntegerField()
	bandas = models.ForeignKey(Banda, related_name = 'organiza')
	evento = models.ManyToManyField(Normal, through = 'Asiste')
	
class Asiste(models.Model):
	pagado = models.BooleanField()
	evento = models.ForeignKey(Evento, null=True)
	normal = models.ForeignKey(Normal, null=True)
	def __unicode__(self):
		return self.evento.titulo + "---" + self.normal.nombre
		
class Noticia(models.Model):
	contenido = models.CharField(max_length=200)
	nombre = models.CharField(max_length=200)
	fuente = models.CharField(max_length=200)
	banda = models.ForeignKey(Banda, related_name = 'trata_de')
	def _unicode_(self):
		return self.contenido
		
class Material(models.Model):
	nombre = models.CharField(max_length=200)
	color = models.CharField(max_length=200, default = 'red')
	enlace = models.CharField(max_length=200)
	descripcion = models.CharField(max_length=200)
	tipo = models.CharField(max_length=200)
	privado = models.BooleanField()
	banda = models.ForeignKey(Banda, related_name = 'publica')
	def __unicode__(self):
		return self.nombre
		
class Calificacion(models.Model):
	valor = models.IntegerField()
	fecha = models.DateField()
	normal = models.ForeignKey(Normal, related_name = 'califica')
	banda = models.ForeignKey(Banda, related_name = 'calificado')
	def _unicode_(self):
		return self.normal.nombre + "---" + self.banda.nombre + " = " + self.valor

class MensajeBanda(models.Model):
	texto = models.CharField(max_length=200)
	fecha = models.DateTimeField(auto_now_add=True)
	bandaE = models.ForeignKey(Banda, related_name = 'enviado', null=True)
	bandaR = models.ForeignKey(Banda, related_name = 'recibido', null=True)
	def __unicode__(self):
		return self.texto
		
class Comentario(models.Model):
	texto = models.CharField(max_length=200)
	fecha = models.DateTimeField(auto_now_add=True)
	usuario = models.ForeignKey(Usuario, related_name = 'comentado', null=True)
	material = models.ForeignKey(Material, related_name = 'comenta', null=True)
	def __unicode__(self):
		return self.texto
		
class Solicitud(models.Model):
	banda = models.ForeignKey(Banda, related_name = 'invita', null=True)
	artista = models.ForeignKey(Artista, related_name='invitado', null=True)
	# direccion, True=pedir, False=invitar
	direccion = models.BooleanField()
	guid = models.CharField(max_length=36, null=True)
	ocupacion = models.CharField(max_length=200, null=True)
	
	def __unicode__(self):
		return self.banda.nombre + " " + self.artista.nombre