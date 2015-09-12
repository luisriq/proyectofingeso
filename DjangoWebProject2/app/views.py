"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, Http404
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from datetime import datetime, timedelta, date
from django.views.generic import View
from models import *
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
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            _user = User.objects.create_user(username=form.cleaned_data['email'],
                             password=form.cleaned_data['password2'],
                             first_name=form.cleaned_data['name'])
            fecha = 0
            if not form.cleaned_data['tipo']:
                usuario = Normal(user = _user)
                fecha = usuario.fechaIngreso
                usuario.save()
            else:
                usuario = Artista(user = _user)
                fecha = usuario.fechaIngreso
            	usuario.save()
            user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password2'])
            print "user : ", form.cleaned_data['email'], "pass : ", form.cleaned_data['password2'], "login : ", user
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
            return HttpResponseRedirect("/login")
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
            return HttpResponseRedirect("/login") 
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
                    'lasquesigo':bandasSeguidas
                })
            )
        
#-----------------------------------------------------------

class perfilBandaNp(View):
    
    def get(self, request, bandaid):
        tipoUsuario = verificacion(request)
        if tipoUsuario == 0:
            return HttpResponseRedirect("/login")   
               #banda seleccionada proveniente del modelo, por medio del ntegrante logeado
        artista = Artista.objects.filter(user = request.user)[0]
        banda = Banda.objects.filter(id = bandaid)[0]
        pertenece = IntegrantesBanda.objects.filter(integrante = artista).filter(banda = banda)
        if len(pertenece) == 1:
            return HttpResponseRedirect("/perfilBanda/%s" % bandaid)
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
        normal = getUsuarioUrl(normalid)
        tipoUsuarioUrl = verificacion(normal)
        verLogVsUrl = verificarLogVsUrl(request, normalid)
        if tipoUsuario == 0:
            return HttpResponseRedirect("/login") 
        
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
    def get(self, request, bandaid):
        tipoUsuario = verificacion(request)
        if tipoUsuario == 0:
            return HttpResponseRedirect("/login")
        artista = Artista.objects.filter(user = request.user)[0]
        banda = Banda.objects.filter(id = bandaid)[0]
        pertenece = IntegrantesBanda.objects.filter(integrante = artista).filter(banda = banda)
        if len(pertenece) == 1:
            integrantes = [ib for ib in IntegrantesBanda.objects.filter(banda = banda)]  
            seguidores = len(banda.seguidores.all())
            
            assert isinstance(request, HttpRequest)
            return render(
                request,
                'app/perfilBandaNp.html',
                context_instance = RequestContext(request,
                {
                    'banda':banda,
                    'artista':artista,
                    'tipoUsuario':tipoUsuario,
                    'datosBarra':datosBarra(request),
                    'integrantes':integrantes,
                    'seguidores':seguidores
                })
            )
#------------------------

class perfilArtista(View):
    def get(self, request):
        tipoUsuario = verificacion(request)
        if tipoUsuario == 0:
            return HttpResponseRedirect("/login")
        usuario = request.user
        try:
            artista = Artista.objects.filter(user = usuario)[0]
        except:
            return HttpResponse("Debe redirigirse al home del usuario normal")
        integranteEn = IntegrantesBanda.objects.filter(integrante = artista)
        instrumentos = [ib for ib in Toca.objects.filter(artista = artista)]
        seguidores = len(artista.seguidores.all())
        formimagen = UploadFileForm()
        allInstruments = Instrumento.objects.all()
        
            
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
                'formImagen':formimagen,
            })
        )
#------------------------------------------------------
#    clase perfil Artista No propietario
#------------------------------------------------------
class perfilArtistaNp(View):
    def get(self, request,userid):
        tipoUsuario = verificacion(request)
        usuario = getUsuarioUrl(userid)
        tipoUsuarioUrl = verificacion(usuario)
        verLogVsUrl = verificarLogVsUrl(request, userid)
        if tipoUsuario == 0:
            return HttpResponseRedirect("/login")           
        
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
            integranteEn = [ib.banda for ib in IntegrantesBanda.objects.filter(integrante = artista)]
            
            #instrumentos que toca
            instrumentos = [ib for ib in Toca.objects.filter(artista = artista)]
            
            #numero de seguidores
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
        
#------------------------------
class crearBanda(View):
    def post(self, request):
        tipoUsuario = verificacion(request)
        if tipoUsuario != 1:
            return HttpResponseRedirect("/login")
         
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


def guardarDatosArtista(request):
    try:
        if request.method == 'POST':
            
            print "Loged %s"%request.user.id
            dato = request.POST.get('dato')
            target = request.POST.get('target')
            response_data = {}
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
            print "YEEEES %s"%dato
            print "Target %s"%target
    except :
        return HttpResponse("ERROR")
    return HttpResponse("OK")

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

