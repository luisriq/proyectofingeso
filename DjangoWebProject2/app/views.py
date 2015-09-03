"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, Http404
from django.template import RequestContext
from datetime import datetime, timedelta, date
from django.views.generic import View
from models import *
import time
from forms import *
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
import json


from django.views.generic.edit import CreateView

class VistaSignUp(View):
    def post(self, request):
        # create a form instance and populate it with data from the request:
        form = RegistroForm(request.POST)
        # check whether it's valid:
        print "lkansdlkansdlkansds"
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            _user = User.objects.create_user(username=form.cleaned_data['email'],
                             password=form.cleaned_data['password2'],
                             first_name=form.cleaned_data['name'])
            fecha = 0
            if not form.cleaned_data['tipo']:
                usuario = Normal(user = _user, correo=form.cleaned_data['email'], 
                             nombre = form.cleaned_data['name'], 
                             contrasena = form.cleaned_data['password2'], )
                fecha = usuario.fechaIngreso
                usuario.save()
            else:
                usuario = Artista(user = _user, correo=form.cleaned_data['email'], 
                             nombre = form.cleaned_data['name'], 
                             contrasena = form.cleaned_data['password2'], )
                fecha = usuario.fechaIngreso
            	usuario.save()
            print "EXITO!!!!"
            return render( 
                request,
                'app/usuarioCreado.html',
                context_instance = RequestContext(request,
                {
                    'title':'Home Page',
                    'year':datetime.now().year,
                    'nombre':form.cleaned_data['name'],
                    'email':form.cleaned_data['email'],
                    'creado':fecha,
                })
        	)
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
            elif len(Normal.objects.filter(user=request.user)) == 1:
                normal = Normal.objects.filter(user = request.user)
                urlAvatar = normal[0].imagenPerfil.url
                tipo = "Normal :"
        except:
            print "Usuario no logeado"
            return HttpResponseRedirect("/login")
            tipo = ""
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
#-----------------------------------------------------------

class perfilBandaNp(View):
    
    def get(self, request, bandaid):
        tipoUsuario = verificacion(request)
        if tipoUsuario == 0:
            return HttpResponse("FORBIDEN 404 ERROR ACCESO DENEGADO HAY QUE LOGEARSE")    
               #banda seleccionada proveniente del modelo, por medio del ntegrante logeado
        #banda = IntegrantesBanda.objects.filter(integrante =)[0].banda
        #lista de los integrantes de la banda (modelo)
        #ide = banda.id
        #if ide == bandaid:
        #    return HttpResponseRedirect("/perfilBanda")
        banda = Banda.objects.filter(id = bandaid)[0]
        integrantes = [ib for ib in IntegrantesBanda.objects.filter(banda = banda)]  
        seguidores = len(banda.seguidores.all())
        
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/perfilBandaNp.html',
            context_instance = RequestContext(request,
            {
                'banda':banda,
                'tipoUsuario':tipoUsuario,
                'datosBarra':datosBarra(request),
                'integrantes':integrantes,
                'seguidores':seguidores
            })
        )
#-----------------------------------------------------------
#    clase perfil normal no propietario
#-----------------------------------------------------------
class perfilNormalNp(View):
    
    def get(self, request, normalid):
        tipoUsuario = verificacion(request)
        verLogVsUrl = verificarLogVsUrl(request, normalid)
        print "tipo : ", tipoUsuario, " vs : ", verLogVsUrl, " @ : ", request.user
        if tipoUsuario == 0:
            return HttpResponse("FORBIDEN 404 ERROR ACCESO DENEGADO HAY QUE LOGEARSE") 
        
        elif verLogVsUrl and tipoUsuario == 1:
            return HttpResponseRedirect("/perfilArtistaNp/%s" % normalid)
            
        elif verLogVsUrl and tipoUsuario == 2:
            return HttpResponseRedirect("/perfilNormal/%s" % normalid)
                #falta hacer esta template
        else:
            #usuario del perfil normal
            normal = Normal.objects.filter(id = normalid)[0]  
            
            #artistas a los que sigue el usuario normal de la url
            artistasSeguidos = Artista.objects.filter(seguidores = normal)
        
            #bandas a las que sigue el usuario normal de la url
            bandasSeguidas = Banda.objects.filter(seguidores = normal)
            
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
                    'lasquesigo':bandasSeguidas
                })
            )
        
        
        
        
        
#-----------------------------------------------------------
   

class perfilBanda(View):
    def get(self, request):
        if not request.user.is_authenticated() :
            return HttpResponse("FORBIDEN 404 ERROR ACCESO DENEGADO HAY QUE LOGEARSE")
        usuario = request.user
        artista = Artista.objects.filter(user = usuario)
        #if(len(artista)==0):
        #    return HttpResponse("Solo artista")
        artista = artista[0]
        integranteEn = IntegrantesBanda.objects.filter(integrante = artista)
        #holi
        instrumentos = [ib.instrumento for ib in Toca.objects.filter(artista = artista)]
        seguidores = len(artista.seguidores.all())
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/perfilArtista.html',
            context_instance = RequestContext(request,
            {
                'year':datetime.now().year,
                'integranteEn':integranteEn,
                'datosBarra':datosBarra(request),
                'instrumentos':instrumentos,
                'seguidores':seguidores,
                'artista':artista
            })
        )
#------------------------

class perfilArtista(View):
    def get(self, request):
        tipoUsuario = verificacion(request)
        if tipoUsuario == 0:
            return HttpResponse("FORBIDEN 404 ERROR ACCESO DENEGADO HAY QUE LOGEARSE") 
        usuario = request.user
        try:
            artista = Artista.objects.filter(user = usuario)[0]
        except:
            return HttpResponse("Debe redirigirse al home del usuario normal")
        integranteEn = IntegrantesBanda.objects.filter(integrante = artista)
        instrumentos = [ib.instrumento for ib in Toca.objects.filter(artista = artista)]
        seguidores = len(artista.seguidores.all())
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/perfilArtista.html',
            context_instance = RequestContext(request,
            {
                'year':datetime.now().year,
                'integranteEn':integranteEn,
                'tipoUsuario': tipoUsuario,
                'datosBarra':datosBarra(request),
                'instrumentos':instrumentos,
                'seguidores':seguidores,
                'artista':artista
            })
        )
#------------------------------------------------------
#    clase perfil Artista No propietario
#------------------------------------------------------
class perfilArtistaNp(View):
    def get(self, request,userid):
        tipoUsuario = verificacion(request)
        if tipoUsuario == 0:
            return HttpResponse("FORBIDEN 404 ERROR ACCESO DENEGADO HAY QUE LOGEARSE")           
        
        try:
            # si en la url se tiene la key de un normal se redirecciona en el except
            artista = Artista.objects.filter(id = userid)[0]
            # si el usuario logueado es el mismo al que se esta viendo
            usuarioLog = Usuario.objects.filter(user = request.user)[0]
            if usuarioLog.id == artista.id:
                return HttpResponseRedirect("/perfilArtista")
                
            integranteEn = [ib.banda for ib in IntegrantesBanda.objects.filter(integrante = artista)]
            instrumentos = [ib for ib in Toca.objects.filter(artista = artista)]
            seguidores = len(artista.seguidores.all())
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
                    'integranteEn':integranteEn
                })
            )
        except:
            return HttpResponseRedirect("/perfilNormalNp/%s" % userid)
        
#------------------------------
class crearBanda(View):
    def post(self, request):
        tipoUsuario = verificacion(request)
        if tipoUsuario != 1:
            return HttpResponse("FORBIDEN 404 ERROR ACCESO DENEGADO HAY QUE LOGEARSE") 
         
        # create a form instance and populate it with data from the request:
        form = CrearBandaForm(request.POST)
        # check whether it's valid:
        print "lkansdlkansdlkansds"
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
        return render(
            request, 
            'app/crearBanda.html', 
            context_instance = RequestContext(request,
            {
                'tipoUsuario':tipoUsuario,
                'datosBarra':datosBarra(request),
                'form': form
            })
        )

#------------------------------
 
 #------------------------------------------------------       
class busqueda(View):
    def get(self, request):
        
        if request.is_ajax():
                   artistas = Artista.objects.filter(nombre__startswith= request.GET['nombre'] ).values('id', 'nombre', 'imagenPerfil')
                   #return HttpResponse( json.dumps( list(artistas)), content_type='application/json' ) 
        else:
                   return HttpResponse("['nombre':0]");
        
#----------------------------------------------
class editarPerfilArtistA(View):
    def get(self, request):
        
        if  request.user.is_authenticated():
            
                   return HttpResponse( request.GET["target"] + " - " +request.GET["data"]) 
                   #return HttpResponse( json.dumps( list(artistas)), content_type='application/json' ) 
        else:
                   return HttpResponse("a la mierda ");
        
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
        return render(
        request,
        'app/%s.html'%template,
        context_instance = RequestContext(request,
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
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
                admin = Administrador.objects.filter(user = request.user)[0]
                
                tipo = 3
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
    
def datosBarra(request): #TODO: Solo tira 3 bandas
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


def guardarDatosArtista(request):
    return "yes"

    
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        print form
        if form.is_valid():
            handle_uploaded_file(request.FILES['file_'])
            u = Usuario.objects.filter(user = request.user)[0]
            u.imagenPerfil = 'pic_folder/%s'%request.FILES['file_']
            u.save()
            return HttpResponseRedirect('/upload')
    else:
        form = UploadFileForm()
    return render(
        request,
        'app/upload.html',
        context_instance = RequestContext(request,
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,'form': form,
        })
    )

def handle_uploaded_file(f):
    with open('pic_folder/%s'%f, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

