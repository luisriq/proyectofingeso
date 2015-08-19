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
        tipo = ""
        try:
            if len(Artista.objects.filter(user=request.user)) == 1:
                tipo = "Artista :"
            elif len(Normal.objects.filter(user=request.user)) == 1:
                tipo = "Normal :"
        except:
            tipo = ""
        return render( 
            request,
            'app/mainartista.html',
            context_instance = RequestContext(request,
            {
                'title':'Pagina Principal Artista',
                
                'tipo':tipo,
                
                'year':datetime.now().year,
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
class perfilBanda(View):
    
    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponse("FORBIDEN 404 ERROR ACCESO DENEGADO HAY QUE LOGEARSE")
        usuario = request.user
        a = Artista.objects.filter(user = usuario)[0]

        bandaSelec = IntegrantesBanda.objects.filter(integrante = a)[0].banda
        integrantes = [ib.integrante for ib in IntegrantesBanda.objects.filter(banda = bandaSelec)]
        #Ver cada una de las bandas a las que pertenece
        #Las habilidades estan raras
        habilidades = IntegrantesBanda.objects.filter(integrante = a)[0].ocupacion
        banda = bandaSelec
        #No hemos puesto los seguidores, tabun
        seguidores = 1
        
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/perfilBanda.html',
            context_instance = RequestContext(request,
            {
                'habilidades':habilidades,
                'seguidores':seguidores,
                'Banda':banda,
                
            })
        )
#-----------------------------------------------------------
   

class perfilArtista(View):
    
    
    
    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponse("FORBIDEN 404 ERROR ACCESO DENEGADO HAY QUE LOGEARSE")
        usuario = request.user
        a = Artista.objects.filter(user = usuario)[0]

        integranteEn = IntegrantesBanda.objects.filter(integrante = a)
        #Ver cada una de las bandas a las que pertenece
        #Las habilidades estan raras
        habilidades = IntegrantesBanda.objects.filter(integrante = a)[0].ocupacion
        informacion = a.biografia
        nombre = a.nombre
        #No hemos puesto los seguidores, tabun
        seguidores = 1
        
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/perfilArtista.html',
            context_instance = RequestContext(request,
            {
                'year':datetime.now().year,
                'integranteEn':integranteEn,
                'habilidades':habilidades,
                'seguidores':seguidores
                
            })
        )

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
