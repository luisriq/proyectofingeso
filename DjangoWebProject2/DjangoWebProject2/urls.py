"""
Definition of urls for DjangoWebProject2.
"""

from datetime import datetime
from django.conf.urls import patterns, url, include
from app.forms import BootstrapAuthenticationForm
from django.contrib import admin
from app.views import *
from PIL import Image
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns, static
from django.contrib.auth.decorators import login_required
# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', Home.as_view(), name='home'),
    url(r'^contact$', 'app.views.contact', name='contact'),
    #url(r'^error404', error404.as_view(), name='404'),
    url(r'^about', 'app.views.about', name='about'),
    #url(r'^login', VistaSignUp.as_view(), name='login'),
    url(r'^registro', VistaSignUp.as_view(), name='signup'),
    url(r'^perfilArtistaNp/(?P<userid>\w{1,50})$', perfilArtistaNp.as_view(), name='perfilArtistaNp'),
    url(r'^perfilArtista', perfilArtista.as_view(), name='perfilArtista'),
    url(r'^perfilNormalNp/(?P<normalid>\w{1,50})$', perfilNormalNp.as_view(), name='perfilNormalNp'),
    url(r'^perfilNormal', perfilNormal.as_view(), name='perfilNormal'),
    url(r'^perfilBandaNp/(?P<bandaid>\w{1,50})$', perfilBandaNp.as_view(), name='perfilBandaNp'),
    url(r'^noImplementado/(?P<template>\w{1,50})$', NoImplementado.as_view(), name='noImplementado'),
    url(r'^perfilBanda/(?P<bandaid>\w{1,50})$', perfilBanda.as_view(), name='perfilBanda'),
    url(r'^infoDisco/(?P<dId>\w{1,50})$', infoDisco.as_view(), name='infoDisco'),
    url(r'^infoDiscoE/(?P<dId>\w{1,50})$', infoDiscoE.as_view(), name='infoDiscoE'),
    url(r'^addDisco/(?P<bId>\w{1,50})$', addDisco.as_view(), name='addDisco'),
    url(r'^crearBanda', crearBanda.as_view(), name='crearBanda'),
    url(r'^config', config.as_view(), name='config'),
    url(r'^busqueda$', busqueda.as_view(), name='busqueda'),
    url(r'^guardarDatosArtista$', guardarDatosArtista, name='updatePA'),
    url(r'^guardarDatosBanda$', guardarDatosBanda, name='updateB'),
    url(r'^guardarDatosNormal$', guardarDatosNormal, name='updatePN'),
    url(r'^guardarDatosPersonales$', guardarDatosPersonales, name='updateP'), 
    url(r'^agregarMaterial$', agregarMaterial, name='addM'),   
    url(r'^crearDisco$', crearDisco, name='addD'),
    url(r'^crearCancion$', crearCancion, name='addC'),
    url(r'^upload$', upload_file, name='upload'),
    url(r'^search', search),#buscador
    url(r'^autoPoblado', poblacionBd),
    url(r'^login/$',
        'django.contrib.auth.views.login',
        {
            'template_name': 'app/login.html',
            'authentication_form': BootstrapAuthenticationForm,
            'extra_context':
            {
                'title':'Log in',
                'year':datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        'django.contrib.auth.views.logout',
        {
            'next_page': '/login/',
        },
        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?P<loquesea>\w{1,300})$', error404.as_view(), name='error'),
    
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
