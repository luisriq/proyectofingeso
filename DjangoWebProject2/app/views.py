"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, Http404, HttpResponseBadRequest
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from datetime import datetime, timedelta, date
from django.views.generic import View
from models import *
from forms import *
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
import json
import unicodedata
import uuid
import sys, os
import traceback
from django.core import serializers
import re
from random import randint

from django.views.generic.edit import CreateView

class VistaSignUp(View):
    def post(self, request):
        # create a form instance and populate it with data from the request:
        form = RegistroForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            _user = User.objects.create_user(username=form.cleaned_data['email'].lower(),
                             password=form.cleaned_data['password2'],
                             first_name=form.cleaned_data['name'])
            fecha = 0
            if not form.cleaned_data['tipo']:
                usuario = Normal(user = _user, nombre = form.cleaned_data['name'],
                    correo = form.cleaned_data['email'].lower())
                fecha = usuario.fechaIngreso
                usuario.save()
            else:
                usuario = Artista(user = _user, nombre = form.cleaned_data['name'],
                    correo = form.cleaned_data['email'].lower())
                fecha = usuario.fechaIngreso
            	usuario.save()
            user = authenticate(username=form.cleaned_data['email'].lower(), password=form.cleaned_data['password2'])
            print "user : ", form.cleaned_data['email'].lower(), "pass : ", form.cleaned_data['password2'], "login : ", user
            login(request, user)
            
            if form.cleaned_data['tipo']:
                return HttpResponseRedirect("/perfilArtista")
            else:
                return HttpResponseRedirect("/perfilNormal")
            
        else:
            return render(request, 'app/registro.html', {'form': form})
    def get(self, request):
        # if this is a POST request we need to process the form data
        form = RegistroForm()
    
        return render(request, 'app/registro.html', {'form': form})

class VistaLanding(View):
    def get(self, request):
        return render(request, 'app/landing.html')
    

    
class Home(View):
    def get(self, request):
        tipoUsuario = verificacion(request)
        """Renders the home page."""
        assert isinstance(request, HttpRequest)
        urlAvatar = ""
        tipo = ""
        integranteEn = []
        try:
            if len(Artista.objects.filter(user=request.user)) == 1:
                tipo = "Artista :"
                artista = Artista.objects.filter(user = request.user)
                urlAvatar = artista[0].imagenPerfil.url
                integranteEn = [ib for ib in IntegrantesBanda.objects.filter(integrante = artista)]
                return render( 
                    request,
                    'app/mainartista.html',
                    context_instance = RequestContext(request,
                    {
                        'title':'Pagina Principal Artista',
                        
                        'tipo':tipo,
                        
                        'year':datetime.now().year,
                        'urlAvatar':urlAvatar,
                        'datosBarra':datosBarra(request),
                        'bandas':integranteEn
                    })
                )

            elif len(Normal.objects.filter(user=request.user)) == 1:
                normal = Normal.objects.filter(user = request.user)
                urlAvatar = normal[0].imagenPerfil.url
                tipo = "Normal :"
                bandas = Banda.objects.all()
                return render( 
                    request,
                    'app/mainnormal.html',
                    context_instance = RequestContext(request,
                    {
                        'title':'Pagina Principal Normal',
                        
                        'tipo':tipo,
                        
                        'year':datetime.now().year,
                        'urlAvatar':urlAvatar,
                        'bandas':bandas
                        #'datosBarra':datosBarra(request),
                        #'bandas':integranteEn
                    })
                )
        except:
            print "no logeado"
        return HttpResponseRedirect("/login/")
        tipo = ""
            

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        context_instance = RequestContext(request,
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        })
    )

#----------------------------------------
#   peril normal
#----------------------------------------
class perfilNormal(View):
    
    def get(self, request):
        tipoUsuario = verificacion(request)
        if tipoUsuario == 0:
            return HttpResponseRedirect("/login/") 
        normal = request.user
        try:
            normal = Normal.objects.filter(user = normal)[0]
        except:
            return HttpResponse("Debe redirigirse al home del usuario Artista")
 
        else:  
            
            #artistas a los que sigue el usuario normal de la url
            artistasSeguidos = Artista.objects.filter(seguidores = normal)
        
            #bandas a las que sigue el usuario normal de la url
            bandasSeguidas = Banda.objects.filter(seguidores = normal)
            
            title = 'perfil '+normal.nombre
            #llamada al template
            assert isinstance(request, HttpRequest)
            return render(
                request,
                'app/perfilNormal.html',
                context_instance = RequestContext(request,
                {
                    'usuario':normal,
                    'tipoUsuario':tipoUsuario,
                    'datosBarra':datosBarra(request),
                    'losquesigo':artistasSeguidos,
                    'lasquesigo':bandasSeguidas,
                    'title':title
                })
            )
        
#-----------------------------------------------------------

class perfilBandaNp(View):
    def get(self, request, bandaid):
        tipoUsuario = verificacion(request)
        pertenece = 0
        try:
            banda = Banda.objects.filter(id = bandaid)[0]
        except:
            return HttpResponseRedirect("/error404") 
        discos =  Disco.objects.filter(banda = banda)
        material =  Material.objects.filter(banda = banda)
        
        if tipoUsuario == 0:
            return HttpResponseRedirect("/login/") 
        elif tipoUsuario == 1:
            usuario = Artista.objects.filter(user = request.user)[0]
            pertenece = IntegrantesBanda.objects.filter(integrante = usuario, banda = banda)
            if len(pertenece) == 1:
                return HttpResponseRedirect("/perfilBanda/%s" % bandaid)
            else:
                integrantes = [ib for ib in IntegrantesBanda.objects.filter(banda = banda)]  
                seguidores = len(banda.seguidores.all())
                try:
                    solicitado = len(Solicitud.objects.filter(banda=banda, artista=usuario))==1
                except:
                    solicitado = False
                title = 'perfil de la banda' + banda.nombre
                print "solicitado",solicitado
                return render(
                    request,
                    'app/perfilBandaNp.html',
                    context_instance = RequestContext(request,
                    {
                        'banda':banda,
                        'discos':discos,
                        'material':material,
                        'tipoUsuario':tipoUsuario,
                        'datosBarra':datosBarra(request),
                        'integrantes':integrantes,
                        'solicitado':solicitado,
                        'seguidores':seguidores,
                        'title':title
                    })
                )
        else:
            integrantes = [ib for ib in IntegrantesBanda.objects.filter(banda = banda)]  
            seguidores = len(banda.seguidores.all())
            title = 'perfil de la banda ' + banda.nombre
            assert isinstance(request, HttpRequest)
            return render(
                request,
                'app/perfilBandaNp.html',
                context_instance = RequestContext(request,
                {
                    'banda':banda,
                    'discos':discos,
                    'material':material,
                    'tipoUsuario':tipoUsuario,
                    'datosBarra':datosBarra(request),
                    'integrantes':integrantes,
                    'seguidores':seguidores,
                    'title':title
                })
            )
#-----------------------------------------------------------
#    clase perfil normal no propietario
#-----------------------------------------------------------
class perfilNormalNp(View):
    
    def get(self, request, normalid):
        tipoUsuario = verificacion(request)
        try:
            normal = getUsuarioUrl(normalid)
        except:
            return HttpResponseRedirect("/error404") 
        
        tipoUsuarioUrl = verificacion(normal)
        verLogVsUrl = verificarLogVsUrl(request, normalid)
        if tipoUsuario == 0:
            return HttpResponseRedirect("/login/") 
        
        elif verLogVsUrl and tipoUsuario == 1:
            return HttpResponseRedirect("/perfilArtistaNp/%s" % normalid)
            
        elif verLogVsUrl and tipoUsuario == 2:
            return HttpResponseRedirect("/perfilNormal/%s" % normalid)
                #falta hacer esta template
                
        elif (not verLogVsUrl) and tipoUsuarioUrl == 1:
            return HttpResponseRedirect("/perfilArtistaNp/%s" % normalid)
                
        else:  
            
            #artistas a los que sigue el usuario normal de la url
            artistasSeguidos = Artista.objects.filter(seguidores = normal)
        
            #bandas a las que sigue el usuario normal de la url
            bandasSeguidas = Banda.objects.filter(seguidores = normal)
            
            title = 'perfil ' + normal.nombre
            
            #llamada al template
            assert isinstance(request, HttpRequest)
            return render(
                request,
                'app/perfilNormalNp.html',
                context_instance = RequestContext(request,
                {
                    'usuario':normal,
                    'tipoUsuario':tipoUsuario,
                    'datosBarra':datosBarra(request),
                    'losquesigo':artistasSeguidos,
                    'lasquesigo':bandasSeguidas,
                    'title':title
                })
            )
        
      
        
#-----------------------------------------------------------
   

class perfilBanda(View):
    def get(self, request, bandaid):
        tipoUsuario = verificacion(request)
        if tipoUsuario == 0:
            return HttpResponseRedirect("/login/")
        artista = Artista.objects.filter(user = request.user)[0]
        banda = Banda.objects.filter(id = bandaid)[0]
        discos =  Disco.objects.filter(banda = banda)
        material =  Material.objects.filter(banda = banda)
        pertenece = IntegrantesBanda.objects.filter(integrante = artista).filter(banda = banda)
        generos = Genero.objects.all()
        if len(pertenece) == 1:
            integrantes = [ib for ib in IntegrantesBanda.objects.filter(banda = banda)]  
            seguidores = len(banda.seguidores.all())
            solicitantes = Solicitud.objects.filter(banda = banda)
            print solicitantes
            if(len(solicitantes)==0):
                solicitantes = None
            
            title = 'perfil de la banda ' + banda.nombre
            assert isinstance(request, HttpRequest)
            return render(
                request,
                'app/perfilBanda.html',
                context_instance = RequestContext(request,
                {
                    'banda':banda,
                    'discos':discos,
                    'material':material,
                    'artista':artista,
                    'generos':generos,
                    'esLider':pertenece[0].esLider,
                    'tipoUsuario':tipoUsuario,
                    'datosBarra':datosBarra(request),
                    'integrantes':integrantes,
                    'solicitantes':solicitantes,
                    'seguidores':seguidores,
                    'title':title

                })
            )
#------------------------
class infoDisco(View):
    def get(self, request, dId):
        disco =  Disco.objects.filter(id = dId)[0]
        canciones =   Cancion.objects.filter(disco = disco)
        return render(
            request,
            'app/disco.html',
            context_instance = RequestContext(request,
            {
                'disco':disco,
                'canciones':canciones
            })
        )
#------------------------
class infoDiscoE(View):
    def get(self, request, dId):
        disco =  Disco.objects.filter(id = dId)[0]
        canciones =   Cancion.objects.filter(disco = disco)
        return render(
            request,
            'app/discoE.html',
            context_instance = RequestContext(request,
            {
                'disco':disco,
                'canciones':canciones
            })
        )

#------------------------
class addDisco(View):
    def get(self, request, bId):
        banda = Banda.objects.filter(id = bId)[0]
        return render(
            request,
            'app/add_disco.html',
            context_instance = RequestContext(request,
            {
                'banda':banda,
                'year':datetime.now().year
            })
        )
        

        
#-------------------------
class error404(View):
    def get(self, request, loquesea):
        tipoUsuario = verificacion(request)
        title = 'Error 404'
            
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/404.html',
            context_instance = RequestContext(request,
            {
                'tipoUsuario': tipoUsuario,
                'datosBarra':datosBarra(request),
                'title':title
            })
        )
#------------------------

class perfilArtista(View):
    def get(self, request):
        tipoUsuario = verificacion(request)
        if tipoUsuario == 0:
            return HttpResponseRedirect("/login/")
        usuario = request.user
        try:
            artista = Artista.objects.filter(user = usuario)[0]
        except:
            return HttpResponse("Debe redirigirse al home del usuario normal")
        integranteEn = IntegrantesBanda.objects.filter(integrante = artista)
        instrumentos = [ib for ib in Toca.objects.filter(artista = artista)]
        seguidores = len(artista.seguidores.all())
        #formimagen =  ImageUploadForm()
        allInstruments = Instrumento.objects.all()
        
        title = 'perfil ' + artista.nombre
        
            
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/perfilArtista.html',
            context_instance = RequestContext(request,
            {
                'year':datetime.now().year,
                'integranteEn':integranteEn,
                'tipoUsuario': tipoUsuario,
                'allInstruments':allInstruments,
                'datosBarra':datosBarra(request),
                'instrumentos':instrumentos,
                'seguidores':seguidores,
                'artista':artista,
                'title':title
                #'formImagen':formimagen,
            })
        )
class config(View):
    def get(self, request):
        tipoUsuario = verificacion(request)
        if tipoUsuario == 0:
            return HttpResponseRedirect("/login/")
        usuario = request.user
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/cambiarcontrasena.html',
            context_instance = RequestContext(request,
            {
                'year':datetime.now().year,
                'tipoUsuario': tipoUsuario,
                'datosBarra':datosBarra(request),
                #'formImagen':formimagen,
            })
        )
#------------------------------------------------------
#    clase perfil Artista No propietario
#------------------------------------------------------
class perfilArtistaNp(View):
    def get(self, request,userid):
        tipoUsuario = verificacion(request)
        try:
            usuario = getUsuarioUrl(userid)
        except:
            return HttpResponseRedirect("/error404") 
        
        tipoUsuarioUrl = verificacion(usuario)
        verLogVsUrl = verificarLogVsUrl(request, userid)
        if tipoUsuario == 0:
            return HttpResponseRedirect("/login/")           
        
        elif verLogVsUrl and tipoUsuario == 1:
            return HttpResponseRedirect("/perfilArtista")
            #falta termina este template
            
        elif verLogVsUrl and tipoUsuario == 2:
            return HttpResponseRedirect("/perfilNormal")
            
        elif (not verLogVsUrl) and tipoUsuarioUrl == 2:
            return HttpResponseRedirect("/perfilNormalNp/%s" % userid)
            
        else:
            #usuario del perfil artista
            artista = Artista.objects.filter(id = userid)[0]
            
            #bandas a las que pertenece
            integranteEn = [ib for ib in IntegrantesBanda.objects.filter(integrante = artista)]
            
            #instrumentos que toca
            instrumentos = [ib for ib in Toca.objects.filter(artista = artista)]
            
            #numero de seguidores
            seguidores = len(artista.seguidores.all())
            
            title = 'perfil ' + artista.nombre
            
            assert isinstance(request, HttpRequest)
            return render(
                request,
                'app/perfilArtistaNp.html',
                context_instance = RequestContext(request,
                {
                    'year':datetime.now().year,
                    'instrumentos':instrumentos,
                    'seguidores':seguidores,
                    'datosBarra':datosBarra(request),
                    'artista':artista,
                    'tipoUsuario':tipoUsuario,
                    'integranteEn':integranteEn,
                    'title':title
                })
            )

#----------------------------------

def search(request):

    # si no es una peticion ajax, devolvemos error 400
    if not request.is_ajax() or request.method != "POST":
        return HttpResponseBadRequest()
    
    q = request.POST['q']
    banda = Banda.objects.filter(id=request.POST.get('bid'))
    
    artistas = Artista.objects.filter(nombre__icontains=q).exclude(user=request.user)
    integrantes = [i.integrante for i in IntegrantesBanda.objects.filter(banda = banda)]
    
    for a in integrantes:
        artistas = artistas.exclude(id = a.id)
    
    artistas = artistas.values('id', 'nombre', 'imagenPerfil')
    print artistas

    artista_fields = (
        'nombre',
    )
    data = json.dumps( list(artistas))

    # eso es todo por hoy ^^
    return HttpResponse(data, content_type="application/json")
    
#-----------------------------

#def elimina_tildes(request):
#   return ''.join((c for c in unicodedata.normalize('NFD', request) if unicodedata.category(c) != 'Mn'))
 
#-----------------------------

#def remove_accents(input_str):
#    nfkd_form = unicodedata.normalize('NFKD', input_str)
#    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])    
#------------------------------
class crearBanda(View):
    def post(self, request):
        tipoUsuario = verificacion(request)
        if tipoUsuario != 1:
            return HttpResponseRedirect("/login/")
         
        # create a form instance and populate it with data from the request:
        form = CrearBandaForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            gen = Genero.objects.filter(nombre=form.cleaned_data['genero'])[0]
            fecha = date(year=int(form.cleaned_data['year']), month=int(form.cleaned_data['mes']), day=1)
            b = Banda(nombre = form.cleaned_data['nombre'],
                      genero=gen, 
                      fechaCreacion = fecha)
            b.save()
            usuario = request.user
            artista = Artista.objects.filter(user = usuario)[0]
            
            integr = IntegrantesBanda(integrante = artista, banda = b, esLider=True, fechaIngreso=fecha, ocupacion="Lider")
            integr.save()
            return HttpResponseRedirect("/perfilBandaNp/%s" % b.id)
            
        else:
            return render(request, 'app/crearBanda.html', {'form': form})
            
    def get(self, request):
        # if this is a POST request we need to process the form data
        #Traer todos los generos 
        tipoUsuario = verificacion(request)

        form = CrearBandaForm()
        title = 'Creacion de banda'
        return render(
            request, 
            'app/crearBanda.html', 
            context_instance = RequestContext(request,
            {
                'tipoUsuario':tipoUsuario,
                'datosBarra':datosBarra(request),
                'form': form,
                'title':title
            })
        )


 #------------------------------------------------------       
class busqueda(View):
    def get(self, request):
        
        if request.is_ajax():
                   artistas = Artista.objects.filter(nombre__startswith = request.GET['nombre'] ).exclude(user=usuario).values('id', 'nombre', 'imagenPerfil')
                   return HttpResponse( json.dumps( list(artistas)), content_type='application/json' ) 
        else:
                   return HttpResponse("['nombre':0]");
        

#----------------------------------------------
def about(request):
    raise Http404("Pagina no existe 404 dead link")
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        context_instance = RequestContext(request,
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        })
    )
class NoImplementado(View):
    def get(self, request, template):
        tipoUsuario = verificacion(request)
        sinBarra = False
        title = 'No implementado/'+template
        assert isinstance(request, HttpRequest)
        return render(
        request,
        'app/%s.html'%template,
        context_instance = RequestContext(request,
        {
            'title':'No implementado',
            'message':'Your application description page.',
            'datosBarra':datosBarra(request),
            'tipoUsuario':tipoUsuario,
            'sinBarra':sinBarra,
            'year':datetime.now().year,
            'title':title
        }))
#----------------------------------------------------
#    funcion para verificar si esta login el usuaario  
#---------------------------------------------------- 
def verificacion(request):
    if request.user.is_authenticated():
        try:
            artista = Artista.objects.filter(user = request.user)[0]
            tipo = 1
        except:
            try:
                normal = Normal.objects.filter(user = request.user)[0]
                tipo = 2
            except:
                try:
                    admin = Administrador.objects.filter(user = request.user)[0]
                    tipo = 3
                except:
                    tipo = 0
    else:
        tipo = 0
    return tipo

#-----------------------------------------------------
#    funcion para verificar si el usuario logeado es 
#    el mismo de la url
#-----------------------------------------------------   
def verificarLogVsUrl(request, id):
    usuario = Usuario.objects.filter(user = request.user)[0]
    print "user : ", type(usuario.id), "id : ", type(id)
    if usuario.id == int(id):
        return True
    return False

#-----------------------------------------------------
#    devuelve el usuario logeado
#-----------------------------------------------------   
def getUsuariolog(request):
    if len(Normal.objects.filter(user = request.user)) == 1:
        usuario = Normal.objects.filter(user = request.user)[0]
    elif len(Artista.objects.filter(user = request.user)) == 1:
        usuario = Artista.objects.filter(user = request.user)[0]
    return usuario
#-----------------------------------------------------
#    devuelve el usuario url
#-----------------------------------------------------   
def getUsuarioUrl(urlId):
    if len(Normal.objects.filter(id = urlId)) == 1:
        usuario = Normal.objects.filter(id = urlId)[0]
    elif len(Artista.objects.filter(id = urlId)) == 1:
        usuario = Artista.objects.filter(id = urlId)[0]
    return usuario

#-----------------------------------------------------
#    funcion para saber si una palabra es muy larga
#    dentro de un texto
#-----------------------------------------------------  
def largoPalabra(texto, largo):
    palabras = texto.split(" ")
    lista = []
    for palabra in palabras:
        lista.append(palabra.strip("\n"))
    for palabra in lista:
        if len(palabra) >= largo:
            return False
    return True

      

    
    # sdfsdf
def datosBarra(request): #TODO: Solo tira 3 bandas
    tipoUsuario = verificacion(request) 
    if tipoUsuario == 1:
        bandasParticipo = []
        bandasLider = []
        artis = Artista.objects.filter(user = request.user)[0]
        integranteEn = IntegrantesBanda.objects.filter(integrante = artis)
        for inte in integranteEn:
            if(inte.esLider):
                bandasLider.append(inte.banda)
            else:
                bandasParticipo.append(inte.banda)
        return {"participo":bandasParticipo, "lider":bandasLider}  
    elif tipoUsuario == 2:
        return "ooh"

#---------------------------
def guardarDatosNormal(request):
    try:
        if request.method == 'POST':
            dato = request.POST.get('dato')
            target = request.POST.get('target')
            if target == "nombre":
                u = Normal.objects.filter(user = request.user)[0]
                if u.nombre == dato:
                    return HttpResponse("w,El nombre ingresado era el mismo")
                else:
                    u.nombre = dato
                    request.user.first_name = dato
                    u.nombre = dato
                    request.user.save()
                    u.save()
            elif target == "descripcion":
                u = Normal.objects.filter(user = request.user)[0]
                if u.descripcion == dato:
                    return HttpResponse("w,La descripcion no ha cambiado")
                else:
                    u.descripcion = dato
                    u.save()
    except:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print(traceback.format_exc())
        return HttpResponse("ERROR")
    return HttpResponse("OK")

#---------------------------
def guardarDatosArtista(request):
    try:
        if request.method == 'POST':
            
            print "Loged %s"%request.user.id
            print "Target %s"%request.POST.get('target')
            dato = request.POST.get('dato')
            target = request.POST.get('target')
            if target == "nombre":
                u = Usuario.objects.filter(user = request.user)[0]
                u.nombre = dato
                request.user.first_name = dato
                request.user.save()
                u.save()
            elif target == "biografia":
                u = Artista.objects.filter(user = request.user)[0]
                u.biografia = dato
                u.save()
                print "saved"
            elif target == "cuentaTwitter":
                u = Artista.objects.filter(user = request.user)[0]
                u.cuentaTwitter = dato
                u.save()
                print "cuentaTwitter saved"
            elif target == "instrumento":
                a = Artista.objects.filter(user = request.user)[0]
                i = Instrumento.objects.filter(id = dato)[0]
                existe = Toca.objects.filter(instrumento=i,artista=a)
                print existe
                if(len(existe)!=0):
                    return HttpResponse("ERROR")
                toca = Toca(instrumento=i,artista=a,nivel=1)
                toca.save()
            elif target == "iNivel": 
                print request.POST.get('idToca')
                t = Toca.objects.filter( id =  request.POST.get('idToca'))[0] 
                t.nivel = dato
                t.save()
                print "nivel cambiado"
            elif target == "delToca": 
                print request.POST.get('idToca')
                t = Toca.objects.filter( id =  request.POST.get('idToca'))
                if len(t)==0:
                    print t
                    return HttpResponse("ERROR")
                t[0].delete()
                print "instrumento eliminado"
            elif target == "passwordUpdate": 
                print dato
                user = User.objects.get(username=request.user.username)
                if(user.check_password(request.POST.get('olddato'))):
                    user.set_password(dato)
                    user.save()
                else:
                    return HttpResponse("ERROR")
            print "YEEEES %s"%dato
            print "Target %s"%target
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print(traceback.format_exc())
        return HttpResponse("ERROR")
    return HttpResponse("OK")

def guardarDatosBanda(request):
    try:
        if request.method == 'POST':
            for key, value in request.POST.iteritems():
                print "%s:%s"%(key,value)
            print "Loged %s"%request.user.id
            print "Target %s"%request.POST.get('target')
            bandId = request.POST.get('bid')            
            dato = request.POST.get('dato')
            target = request.POST.get('target')
            banda=Banda.objects.filter(id = bandId)[0]
            integrante = IntegrantesBanda.objects.filter(banda=banda,integrante = Artista.objects.filter(user=request.user)[0])
            if target == "solicitarBanda": 
                print "idbanda:",dato    
                a = Artista.objects.filter(id = request.POST.get('artista'))[0]
                
                print "b", banda.nombre,"a",a.nombre
                if(len(Solicitud.objects.filter(artista = a, banda = banda))==0):
                    s = Solicitud(ocupacion = dato ,artista = a, banda = banda, direccion = False)
                    s.save()
                    return HttpResponse("OK,%d"%s.id)
                else:
                    return HttpResponse("ERROR")
            elif(len(integrante)==1):
                if target == "nombre":
                    if integrante[0].esLider:
                        if banda.nombre==dato:
                            return HttpResponse("w,El nombre ingresado era el mismo")
                        else:
                            banda.nombre = dato
                            banda.save()
                    else:
                        return HttpResponse("e,No tienes permiso para cambiar el nombre")
                elif target == "retirarse":
                    artista = Artista.objects.filter(user = request.user)[0]
                    integrante = IntegrantesBanda.objects.filter(integrante = artista).filter(banda = banda)[0]
                    integrante.delete()
                    liderBanda(banda)
                elif target == "biografia":
                    if integrante[0].esLider:
                        if banda.biografia==dato:
                            return HttpResponse("w,El texto ingresado era el mismo")
                        else:
                            banda.biografia = dato
                            banda.save()
                    else:
                        return HttpResponse("e,No tienes permiso para cambiar la biograf&iacute;a")
                elif target == "genero":
                    if integrante[0].esLider:
                        genero = Genero.objects.filter(id = dato)[0]
                        if banda.genero==genero:
                            return HttpResponse("w,El genero ingresado era el mismo")
                        else:
                            banda.genero = genero
                            banda.save()
                    else:
                        return HttpResponse("e,No tienes permiso para cambiar la biograf&iacute;a")
                elif target == "cuentaTwitter":
                    if integrante[0].esLider:
                        if banda.cuentaTwitter==dato:
                            return HttpResponse("w,El texto ingresado era el mismo")
                        else:
                            banda.cuentaTwitter = dato
                            banda.save()
                    else:
                        return HttpResponse("e,No tienes permiso para cambiar la biograf&iacute;a")
                elif target=='material-delete':
                    m = Material.objects.filter(id = dato,banda=banda)
                    if(len(m)>0):
                        m[0].delete()
                        return HttpResponse("OK")
                    else:
                        return HttpResponse("e,No tienes permiso o el material ya no existe")
                elif target=='disco-delete':
                    d = Disco.objects.filter(id = dato,banda=banda)
                    if(len(d)>0):
                        d[0].delete()
                        return HttpResponse("OK")
                    else:
                        return HttpResponse("e,No tienes permiso o el disco ya no existe")
                elif target=='cancion-delete':
                    c = Cancion.objects.filter(id = dato)
                    print dato
                    if(len(c)>0):
                        c[0].delete()
                        return HttpResponse("k,Eliminado con exito")
                    else:
                        return HttpResponse("e,No tienes permiso o la canci&oacute;n ya no existe")
                elif target == "aceptarSolicitud": 
                    if integrante[0].esLider:
                        print "id",dato
                        s = Solicitud.objects.filter(id=dato)[0]
                        accion = request.POST.get('accion')
                        print "accion %s"%accion
                        if(accion == "aceptar"):
                            integr = IntegrantesBanda(integrante = s.artista, banda = s.banda, esLider=False, ocupacion=s.ocupacion, fechaIngreso=datetime.now())
                            integr.save()
                            print "AcEPTAR"
                        s.delete()
                    else:
                        return HttpResponse("e,No tienes permiso para aceptar solicitudes")
            elif target == "solicitar": 
                    print "idbanda:",dato    
                    a = Artista.objects.filter(user = request.user)[0]
                    
                    print "b", banda.nombre,"a",a.nombre
                    if(len(Solicitud.objects.filter(artista = a, banda = banda))==0):
                        s = Solicitud(ocupacion = dato ,artista = a, banda = banda, direccion = True)
                        s.save()
                    else:
                        return HttpResponse("ERROR")
            else:
                return HttpResponse("e,No tienes permiso para esta operaci&oacute;n")
       
    except :
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print(traceback.format_exc())
        return HttpResponse("ERROR")
    return HttpResponse("OK")
    
#----------------------------
def agregarMaterial(request):
    try:
        if request.method == 'POST':
            print "Loged as %s"%request.user.id
            bandId = request.POST.get('bid')
            tipo = request.POST.get('tipo')
            nombre = request.POST.get('nombre')
            color = request.POST.get('color')
            enlace = request.POST.get('enlace')
            descripcion = request.POST.get('descripcion')
            banda =Banda.objects.filter(id = bandId)[0]
            integrante = IntegrantesBanda.objects.filter(banda=banda,integrante = Artista.objects.filter(user=request.user)[0])
            if(len(integrante)==1):
                m = Material(nombre = nombre,color=color,enlace=enlace,descripcion=descripcion,tipo=tipo,privado=True,banda=banda)
                m.save()
                return HttpResponse("k,%d"%m.id)
            else:
                return HttpResponse("e,El usuario no tiene permisos para agregar material en esta banda")
    except :
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print(traceback.format_exc())
        return HttpResponse("ERROR")
    return HttpResponse("OK")
#--------
    
def liderBanda(Banda):
    lider = tieneLider(Banda)
    if lider == 0:
        Banda.delete()
    elif lider == 2:
        integrantes = IntegrantesBanda.objects.filter(banda = Banda)
        lider = integrantes[randint(0, len(integrantes)-1)]
        lider.esLider = True
        lider.save()
        
    
def tieneLider(Banda):
    integrantes = IntegrantesBanda.objects.filter(banda = Banda)
    if len(integrantes) == 0:
        return 0
    for integrante in integrantes:
        if integrante.esLider:
            return 1
    return 2

    #--------
def crearDisco(request):
    try:
        if request.method == 'POST':
            print "Loged as %s"%request.user.id
            bandId = request.POST.get('bid')
            nombre = request.POST.get('nombre')
            lanzamiento = request.POST.get('lanzamiento')
            cancion = request.POST.get('cancion')
            canciones=''
            if cancion != ']':
                canciones = json.loads(cancion)
            if nombre!='' and lanzamiento != '':
                banda = Banda.objects.filter(id = bandId)[0]
                d = Disco(nombre=nombre,lanzamiento=lanzamiento+"-01-01",banda=banda)
                d.save()
                for c in canciones :
                    C=Cancion(nombre=c['nombre'],autor=c['autor'],duracion=c['duracion']+" m",disco=d)
                    C.save()
                return HttpResponse("k,%d"%d.id)
            else:
                return HttpResponse("e,Los campos no deben estar vac&iacute;os")
    except :
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print(traceback.format_exc())
        return HttpResponse("ERROR")
    return HttpResponse("OK")
def crearCancion(request):
    try:
        if request.method == 'POST':
            print "Loged as %s"%request.user.id
            bandId = request.POST.get('bid')
            banda = Banda.objects.filter(id = bandId)[0]
            did = request.POST.get('did')
            disco = Disco.objects.filter(id=did)[0]
            cancion = request.POST.get('cancion')
            canciones=''
            print cancion
            if cancion != ']':
                canciones = json.loads(cancion)
                for c in canciones :
                    C=Cancion(nombre=c['nombre'],autor=c['autor'],duracion=c['duracion']+" m",disco=disco)
                    C.save()
                if len(c)==1:
                    return HttpResponse("k,Cancion agregada con exito")
                else:
                    return HttpResponse("k,Canciones agregadas con exito")
            else:
                return HttpResponse("e,Los campos no deben estar vac&iacute;os")
           
    except :
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print(traceback.format_exc())
        return HttpResponse("ERROR")
    return HttpResponse("OK")
    
def guardarDatosPersonales(request):
    try:
        if request.method == 'POST':
            print "Loged %s"%request.user.id
            target = request.POST.get('target')
            if(target=="email"):
                dato = request.POST.get('dato')
                u = User.objects.filter(username= dato)
                if(len(u) > 0):
                    print u[0]==request.user
                    if u[0]==request.user:
                        return HttpResponse("w,No se cambi&oacute; el correo ya que no era distinto")
                    else :
                        return HttpResponse("e,Ese correo no est&aacute; disponible")
                else:
                    #cambiar el email
                    user = User.objects.filter( id = request.user.id)[0]
                    usuario = Usuario.objects.filter(user = user)[0]
                    usuario.correo = dato
                    user.username = dato
                    user.save()
                    usuario.save()
            elif target == "pass": 
                user = User.objects.get(username=request.user.username)
                dato = request.POST.get('dato')                
                if(user.check_password(request.POST.get('olddato'))):
                    user.set_password(dato)
                    user.save()
                else:
                     return HttpResponse("e,Error de autenticaci&oacute;n")   
    except :
        return HttpResponse("ERROR")
    return HttpResponse("OK")
    #---------
def upload_file(request):
    target = request.POST.get('target')
    if request.method == 'POST':
        try:
            path = handle_uploaded_file(request.FILES['image'])
            if(target == 'banda'):
                banda = Banda.objects.filter(id=request.POST.get('bid'))[0]
                banda.imagenPerfil = path
                banda.save()
            elif(target == "bandaPortada"):
                banda = Banda.objects.filter(id=request.POST.get('bid'))[0]
                banda.imagenPortada = path
                banda.save()
            else:
                print request.FILES['image']
                u = Usuario.objects.filter(user = request.user)[0]
                u.imagenPerfil = path  
                u.save()
            return HttpResponse(path)
        except:
            print "error en el request.FILES['image']"
            return HttpResponse("Error al subir archivo")
    return HttpResponse("procesado")

def handle_uploaded_file(f):
    guid = uuid.uuid4()
    path = 'pic_folder/%s_%s'%(str(guid),f)
    with open('pic_folder/%s_%s'%(str(guid),f), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return path

