"""
Definition of models.
"""

from django.db import models

# Create your models here.

class Musico(models.Model):
	nombre = models.CharField(max_length=200)
	correo = models.CharField(max_length=200)
	sexo = models.BooleanField(default=True)
class Banda(models.Model):
	nombre = models.CharField(max_length=200)