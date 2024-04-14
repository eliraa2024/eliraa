from django.forms import ModelForm
from .models import LiraBoletimDado, Indice
from django import forms

class LiraBoletimDadoForm(ModelForm):
    class Meta:
        model = LiraBoletimDado
        fields = fields = ['quart', 'rua', 'numero',
                           'complemento', 'tipo', 'a1', 'a2', 'b', 'c', 'd1', 'd2']


class IndiceForm(forms.ModelForm):

    class Meta:
        model = Indice
        fields = ['bairro_nome', 'indice_bairro']
