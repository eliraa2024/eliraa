from django.db import models

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



