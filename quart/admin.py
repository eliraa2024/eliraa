from django.contrib import admin
from .models import Bairro, Rua, Quarteirao, Imovel

# Register your models here.
admin.site.register(Bairro)
admin.site.register(Rua)
admin.site.register(Quarteirao)
admin.site.register(Imovel)
