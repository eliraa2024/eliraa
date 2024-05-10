from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4


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


class Ciclo(models.Model):
    ano = models.CharField(max_length=4)
    ciclo = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.ano+'_'+self.ciclo

    class Meta:
        ordering = ['-ano', '-ciclo']


TIPO_IMOVEL = [("tb", "tb"), ("out", "outros")]

class LiraBoletim(models.Model):
    ciclo = models.ForeignKey(
        Ciclo, related_name='ciclo_boletim', on_delete=models.DO_NOTHING, null=True, blank=False)
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    # limit_choices_to={"is_staff": True} para selecionar so os chefes
    chefe = models.ForeignKey(User, related_name='chefe',
                              on_delete=models.DO_NOTHING, limit_choices_to={"is_staff": True}, null=True, blank=False)
    updated_by = models.ForeignKey(
        User, related_name='modificado_por', on_delete=models.DO_NOTHING, null=True, blank=False)


    def __str__(self):
        return str(self.usuario)+'_'+str(self.created_at)[:10]
    
    class Meta:
        ordering = ['-created_at']

        

class LiraBoletimDado(models.Model):
    id_dado = models.UUIDField(
        primary_key=True, default=uuid4, editable=False)
    boletim = models.ForeignKey(LiraBoletim, related_name='lira_boletim', on_delete=models.DO_NOTHING)
    quart = models.CharField(max_length=6)
    rua = models.ForeignKey(Rua, related_name='rua_lira', on_delete=models.DO_NOTHING)
    numero = models.CharField(max_length=6)
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
        return str(self.quart)+'_'+str(self.numero)+'_'+str(self.complemento)


class Indice(models.Model):
    ciclo = models.ForeignKey(Ciclo, related_name='ciclo_indice', on_delete=models.DO_NOTHING)
    bairro_nome = models.ForeignKey(
        Bairro, related_name='bairros', on_delete=models.DO_NOTHING)
    indice_bairro = models.DecimalField(
        max_digits=3, decimal_places=1, null=True, blank=True, default=0)

    def __str__(self):
        indice = str(self.ciclo)+'_'+str(self.bairro_nome)
        return indice

    class Meta:
        ordering = ['bairro_nome']

    
