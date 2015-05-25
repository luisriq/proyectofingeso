from django.contrib import admin

from .models import Musico, Banda, Usuario

admin.site.register(Musico)
admin.site.register(Banda)
admin.site.register(Usuario)