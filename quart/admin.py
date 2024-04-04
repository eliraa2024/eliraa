from django.contrib import admin
from .models import Bairro, Rua, LiraBoletim, LiraBoletimDado

# Register your models here.
admin.site.register(Bairro)
admin.site.register(Rua)
admin.site.register(LiraBoletim)
admin.site.register(LiraBoletimDado)
