"""
Definition of urls for DjangoWebProject2.
"""

from datetime import datetime
from django.conf.urls import patterns, url, include
from app.forms import BootstrapAuthenticationForm
from django.contrib import admin
from app.views import *
from django.contrib.auth.decorators import login_required
# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', Home.as_view(), name='home'),
    url(r'^contact$', 'app.views.contact', name='contact'),
    url(r'^about', 'app.views.about', name='about'),
    url(r'^musicos', login_required(Musicos.as_view()), name='musicos'),
    url(r'^registro', VistaSignUp.as_view(), name='registro'),
    url(r'^landing', VistaLanding.as_view(), name='landing'),
    url(r'^perfilArtista', perfilArtista.as_view(), name='perfilArtista'),
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
            'next_page': '/',
        },
        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
