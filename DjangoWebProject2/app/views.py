"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.views.generic import View
from models import Usuario
from forms import UserForm
from django.contrib.auth.models import User

from django.views.generic.edit import CreateView

class VistaSignUp(View):
    def get(self, request):
        if request.GET.get('email','') != '':
            usuario = Usuario(correo=request.GET.get('email',''), nombre = request.GET.get('nombre',''), contrasena = request.GET.get('pas',''), )
            usuario.save()
            return render( 
                request,
                'app/usuarioCreado.html',
                context_instance = RequestContext(request,
                {
                    'title':'Home Page',
                    'year':datetime.now().year,
                    'nombre':usuario.nombre,
                    'email':usuario.correo,
                    'creado':usuario.fechaIngreso,
                })
        	)
        return render(request, 'app/registro.html') 

class Home(View):
    def get(self, request):
        """Renders the home page."""
        assert isinstance(request, HttpRequest)
        return render( 
            request,
            'app/index.html',
            context_instance = RequestContext(request,
            {
                'title':'Home Page',
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
