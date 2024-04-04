from django.forms import ModelForm
from .models import LiraBoletimDado


class LiraBoletimDadoForm(ModelForm):
    class Meta:
        model = LiraBoletimDado
        fields = fields = ['quart', 'rua', 'numero',
                           'complemento', 'tipo', 'a1', 'a2', 'b', 'c', 'd1', 'd2']
