"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import User
# Crear modelos aqui.


class Usuario(models.Model):
	user = models.OneToOneField(User, null=True)
	nombre = models.CharField(max_length=200)
	correo = models.EmailField(unique=True)
	contrasena =  models.CharField(max_length=200)
	fechaIngreso =  models.DateTimeField(auto_now_add=True)
	imagenPerfil =  models.CharField(max_length=200, blank=True)
	usuarioActivo = models.BooleanField(default=True)
	
	def __unicode__(self):
		return self.nombre + " / " + self.correo

class Artista(Usuario):
	biografia = models.TextField()
	imagenCabecera = models.CharField(max_length=200)
	seguidores = models.ManyToManyField("Normal", null=True, blank=True)
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
	integrantes = models.ManyToManyField(Artista, through = 'IntegrantesBanda')
	genero = models.ForeignKey(Genero, related_name = 'tocado_por')
	def __unicode__(self):
		return self.nombre
		
class IntegrantesBanda(models.Model):
	integrante = models.ForeignKey(Artista, related_name = 'perteneciente', null=True)
	banda = models.ForeignKey(Banda, related_name = 'integrante', null=True)
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

class Cancion(models.Model):
	nombre = models.CharField(max_length=200)
	autor = models.CharField(max_length=200)
		
class Instrumento(models.Model):
	nombre = models.CharField(max_length=200)
	tipo = models.CharField(max_length=200)
	imagen = models.CharField(max_length=200)
	artista = models.ForeignKey(Artista, related_name = 'instrumentos', null=True)
	cancion = models.ManyToManyField(Cancion)
		
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
	enlace = models.CharField(max_length=200)
	descripcion = models.CharField(max_length=200)
	tipo = models.CharField(max_length=200)
	privado = models.BooleanField()
	banda = models.ForeignKey(Banda, related_name = 'publica')
	def _unicode_(self):
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