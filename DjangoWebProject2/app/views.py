"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template import RequestContext
from datetime import datetime
from django.views.generic import View
from models import *
from forms import UserForm, RegistroForm
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
                'bandas':integranteEn
            })
        )

class Musicos(View):
    def get(self, request):
        assert isinstance(request, HttpRequest)
        musicos = Musico.objects.all()
        if ('visitass' in request.session):
            pass
        else:
            request.session['visitass'] = 0
        request.session['visitass'] = request.session['visitass'] + 1
        return render(
            request,
            'app/musicos.html',
            context_instance = RequestContext(request,
            {
                'title':'Musicos',
                'message':'Informacion de los musicos.',
                'year':datetime.now().year,
                'musicos':musicos,
                'visitas':request.session['visitass'],
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
        if not request.user.is_authenticated():
            return HttpResponse("FORBIDEN 404 ERROR ACCESO DENEGADO HAY QUE LOGEARSE")
        usuario = request.user
        a = Artista.objects.filter(user = usuario)[0]
        
        #banda seleccionada proveniente del modelo, por medio del ntegrante logeado
        banda = IntegrantesBanda.objects.filter(integrante = a)[0].banda
        #lista de los integrantes de la banda (modelo)
        ide = banda.id
        if ide == bandaid:
            return HttpResponseRedirect("/perfilBanda")
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
                'integrantes':integrantes,
                'seguidores':seguidores
            })
        )
#-----------------------------------------------------------
class perfilNormalNp(View):
    
    def get(self, request, normalid):
        if not request.user.is_authenticated():
            return HttpResponse("FORBIDEN 404 ERROR ACCESO DENEGADO HAY QUE LOGEARSE")
        usuario = request.user
        
        #usuario al que se esta viendo}
        try:
            usuarioLog = Normal.objects.filter(id = normalid)[0]
        except:
            #url = "/perfilArtistaNp/",normalid
            return HttpResponseRedirect("/perfilArtistaNp/%s" % normalid)
        
        print usuarioLog
        #if ide == bandaid:
        #    return HttpResponseRedirect("/perfilBanda")
        
        #artistas a los que sigue el usuario normal
        artistasSeguidos = Artista.objects.filter(seguidores = usuarioLog)
        
        #bandas a las que sigue el usuario normal
        bandasSeguidas = Banda.objects.filter(seguidores = usuarioLog)
        
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/perfilNormalNp.html',
            context_instance = RequestContext(request,
            {
                'usuario':usuarioLog,
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
                'instrumentos':instrumentos,
                'seguidores':seguidores,
                'artista':artista
            })
        )
#------------------------

class perfilArtista(View):
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
                'instrumentos':instrumentos,
                'seguidores':seguidores,
                'artista':artista
            })
        )
#------------------------
class perfilArtistaNp(View):
    def get(self, request,userid):
        if not request.user.is_authenticated() :
            return HttpResponse("FORBIDEN 404 ERROR ACCESO DENEGADO HAY QUE LOGEARSE")
        usuario = request.user
        usuarioLog = Artista.objects.filter(user = usuario)
        #if(len(usuarioLog)==0):
        #    return HttpResponse("Solo artista")
        try:
            artista = Artista.objects.filter(id = userid)[0]
        except:
            return HttpResponseRedirect("/perfilNormalNp/%s" % userid)
       
        
        
        ##este es el username
        if usuarioLog[0].id == artista.id:
            return HttpResponseRedirect("/perfilArtista")
        integranteEn = [ib.banda for ib in IntegrantesBanda.objects.filter(integrante = artista)]
        instrumentos = [ib for ib in Toca.objects.filter(artista = artista)]
        #instrumentos = Instrumento.objects.filter(artista = artista)
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
                'artista':artista,
                'integranteEn':integranteEn
            })
        )
 
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
