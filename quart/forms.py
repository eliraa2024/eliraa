from django.forms import ModelForm, ValidationError
from .models import LiraBoletimDado, Indice


class LiraBoletimDadoForm(ModelForm):
    class Meta:
        model = LiraBoletimDado
        fields = fields = ['quart', 'rua', 'numero',
                           'complemento', 'tipo', 'a1', 'a2', 'b', 'c', 'd1', 'd2']


class IndiceForm(ModelForm):
    class Meta:
        model = Indice
        fields = ['bairro_nome', 'indice_bairro']

    
