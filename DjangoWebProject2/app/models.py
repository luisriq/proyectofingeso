"""
Definition of models.
"""

from django.db import models

# Create your models here.

class Musico(models.Model):
	nombre = models.CharField(max_length=200)
	correo = models.CharField(max_length=200)
	sexo = models.BooleanField(default=True)
	banda = models.ManyToManyField('Banda', null=True)
	def __unicode__(self):
		return self.nombre

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
	
class Banda(models.Model):
	nombre = models.CharField(max_length=200)
	def __unicode__(self):
		return self.nombre
		
