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
class Banda(models.Model):
	nombre = models.CharField(max_length=200)
	def __unicode__(self):
		return self.nombre
class Usuario(models.Model):
	nombre = models.CharField(max_length=20)
	def __unicode__(self):
		return self.nombre