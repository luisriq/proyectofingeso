"""
Definition of models.
"""

from django.db import models

# Create your models here.


class Usuario(models.Model):
	nombre = models.CharField(max_length=200)
	correo = models.EmailField(unique=True)
	contrasena =  models.CharField(max_length=200)
	fechaIngreso =  models.DateTimeField(auto_now_add=True)
	imagenPerfil =  models.CharField(max_length=200, blank=True)
	usuarioActivo = models.BooleanField(default=True)
	
	def __unicode__(self):
		return self.correo
		
class Normal(Usuario):
	tiempoCastigo = models.IntegerField(default=0)
	descripcion = models.TextField(blank=True)

class Artista(Usuario):
	biografia = models.TextField()
	imagenCabecera = models.CharField(max_length=200)
	
class Administrador(Usuario):	
	pass
	
class Reporte(models.Model):
	justificacion = models.CharField(max_length=200)
	administrador = models.ForeignKey(Administrador, related_name = 'reportado', null=True)
	def __unicode__(self):
		return self.justificacion
	
class Banda(models.Model):
	nombre = models.CharField(max_length=200)
	def __unicode__(self):
		return self.nombre

class Comentario(models.Model):
	texto = models.CharField(max_length=200)
	fecha = models.DateTimeField(auto_now_add=True)
	usuario = models.ForeignKey(Usuario, related_name = 'comentado', null=True)
	def __unicode__(self):
		return self.texto

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

class Cancion(models.Model):
	nombre = models.CharField(max_length=200)
	autor = models.CharField(max_length=200)
		
class Instrumento(models.Model):
	nombre = models.CharField(max_length=200)
	tipo = models.CharField(max_length=200)
	imagen = models.CharField(max_length=200)
	artista = models.ForeignKey(Artista, related_name = 'instrumentos', null=True)
	cancion = models.ManyToManyField(Cancion)

	
