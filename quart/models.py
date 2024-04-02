from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4

# Create your models here.
class Bairro(models.Model):
    sigla = models.CharField(max_length=2, unique=True)
    nome = models.CharField(max_length=25, unique=True)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome

class Rua(models.Model):
    nome = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nome    

class Quarteirao(models.Model):
    bairro = models.ForeignKey(
        Bairro, related_name='bairro', on_delete=models.DO_NOTHING)
    numero = models.CharField(max_length=3)

    class Meta:
        ordering = ['numero']
        verbose_name_plural = 'Quarteiroes'

    def __str__(self):
        return str(self.bairro)+'_'+str(self.numero)

TIPO_IMOVEL = [("tb", "tb"), ("out", "outros")]

class Imovel(models.Model):
    numero = models.CharField(max_length=4)
    complemento = models.CharField(max_length=6, blank=True)
    tipo = models.CharField(choices=TIPO_IMOVEL, max_length=6)
    quarteirao = models.OneToOneField(
        Quarteirao, related_name='quarteirao', unique=True, on_delete=models.DO_NOTHING)
    lado = models.IntegerField()
    rua = models.OneToOneField(
        Rua, related_name='rua', unique=True, on_delete=models.DO_NOTHING)
    
    class Meta:
        ordering = ['id']

    def __str__(self):
        return str(self.quarteirao)+'_'+self.numero+'_'+self.complemento


class LiraBoletim(models.Model):
    id_boletim = models.UUIDField(
        primary_key=True, default=uuid4, editable=False)
    bairro = models.ForeignKey(
        Bairro, related_name='bairro_lira', on_delete=models.DO_NOTHING)
    num_quart = models.CharField(max_length=4)
    num_imoveis = models.CharField(max_length=4)
    extrato = models.CharField(max_length=4)
    data = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(
        User, related_name='usuario_lira', on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return str(self.usuario)+'_'+str(self.id_boletim)
    

class LiraBoletimDado(models.Model):
    id_dado = models.UUIDField(
        primary_key=True, default=uuid4, editable=False)
    boletim = models.ForeignKey(LiraBoletim, related_name='lira_boletim', on_delete=models.DO_NOTHING)
    quart = models.ForeignKey(
        Quarteirao, related_name='quart_lira', on_delete=models.DO_NOTHING)
    rua = models.ForeignKey(Rua, related_name='rua_lira', on_delete=models.DO_NOTHING)
    numero = models.CharField(max_length=4)
    complemento = models.CharField(max_length=6, blank=True)
    tipo = models.CharField(choices=TIPO_IMOVEL, max_length=6)
    a1 = models.IntegerField(default=0)
    a2 = models.IntegerField(default=0)
    b = models.IntegerField(default=0)
    c = models.IntegerField(default=0)
    d1 = models.IntegerField(default=0)
    d2 = models.IntegerField(default=0)
    
    @property
    def num_tubitos(self):
        num_tubitos = int(self.a1)+int(self.a2) + \
            int(self.b)+int(self.c)+int(self.d1)+int(self.d2)
        return num_tubitos

    def __str__(self):
        return str(self.boletim)+'_'+str(self.id_dado)
