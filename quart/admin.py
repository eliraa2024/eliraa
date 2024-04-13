from django.contrib import admin
from .models import Bairro, Rua, LiraBoletim, LiraBoletimDado, Indice, Ciclo

# Register your models here.
admin.site.register(Bairro)
admin.site.register(Rua)
admin.site.register(LiraBoletim)
admin.site.register(LiraBoletimDado)
admin.site.register(Indice)
admin.site.register(Ciclo)
