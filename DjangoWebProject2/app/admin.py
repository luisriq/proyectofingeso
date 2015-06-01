from django.contrib import admin

from .models import Musico, Banda, Usuario, Normal, Artista

admin.site.register(Musico)
admin.site.register(Banda)
admin.site.register(Usuario)
admin.site.register(Normal)
admin.site.register(Artista)