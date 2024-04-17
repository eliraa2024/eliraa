from itertools import count
from django.contrib.auth.mixins import LoginRequiredMixin  # para cbv
from django.contrib.auth.decorators import login_required  # para fbv
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Bairro, Rua, LiraBoletim as Boletim, LiraBoletimDado, Indice, Ciclo
from .forms import LiraBoletimDadoForm, IndiceForm
import folium
from django.contrib import messages
from django.forms import ValidationError


class BairroListView(LoginRequiredMixin, ListView):
    model = Bairro
    template_name = 'bairro/bairro_list.html'


class BairroCreateView(LoginRequiredMixin, CreateView):
    model = Bairro
    fields = ['sigla', 'nome']
    template_name = 'bairro/bairro_form.html'
    success_url = reverse_lazy('bairro_list')


class BairroUpdateView(LoginRequiredMixin, UpdateView):
    model = Bairro
    fields = ['sigla', 'nome']
    template_name = 'bairro/bairro_form.html'
    success_url = reverse_lazy('bairro_list')


class BairroDeleteView(LoginRequiredMixin, DeleteView):
    model = Bairro
    template_name = 'bairro/bairro_confirm_delete.html'
    success_url = reverse_lazy('bairro_list')

################## Rua #########################################


class RuaListView(LoginRequiredMixin, ListView):
    model = Rua
    template_name = 'rua/rua_list.html'


class RuaCreateView(LoginRequiredMixin, CreateView):
    model = Rua
    fields = ['nome']
    template_name = 'rua/rua_form.html'
    success_url = reverse_lazy('rua_list')


class RuaUpdateView(LoginRequiredMixin, UpdateView):
    model = Rua
    fields = ['nome']
    template_name = 'rua/rua_form.html'
    success_url = reverse_lazy('rua_list')


class RuaDeleteView(LoginRequiredMixin, DeleteView):
    model = Rua
    template_name = 'rua/rua_confirm_delete.html'
    success_url = reverse_lazy('rua_list')


################## LiraBoletim #################################

class LiraBoletimListView(LoginRequiredMixin, ListView):
    model = Boletim
    template_name = 'boletim/lira_boletim_list.html'

    def get_queryset(self):
        u = self.request.user

        # listagem para os chefes
        if u.is_staff == True and u.is_superuser == False:
            return Boletim.objects.filter(chefe=u).order_by('-created_at')

        # listagem para o digitador (superusuário)
        elif u.is_staff == True and u.is_superuser == True:
            return Boletim.objects.all().order_by('usuario')

        # listagem para os ACEs
        else:
            return Boletim.objects.filter(usuario=u)


class LiraBoletimCreateView(LoginRequiredMixin, CreateView):
    model = Boletim
    fields = ['ciclo', 'bairro', 'num_quart',
              'num_imoveis', 'extrato', 'chefe']
    template_name = 'boletim/lira_boletim_form.html'
    success_url = reverse_lazy('lira_boletim_list')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class LiraBoletimUpdateView(LoginRequiredMixin, UpdateView):
    model = Boletim
    fields = ['ciclo', 'bairro', 'num_quart',
              'num_imoveis', 'extrato', 'chefe']
    template_name = 'boletim/lira_boletim_form.html'
    success_url = reverse_lazy('lira_boletim_list')

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class LiraBoletimDeleteView(LoginRequiredMixin, DeleteView):
    model = Boletim
    template_name = 'boletim/lira_boletim_confirm_delete.html'
    success_url = reverse_lazy('lira_boletim_list')


@login_required
def liraboletim_detail(request, pk):
    template_name = 'boletim/liraboletim_detail.html'
    boletim = get_object_or_404(Boletim, pk=pk)
    context = {
        'boletim': boletim,
        'pk': pk
    }
    return render(request, template_name, context)


################### LiraBoletimDado ##################################

@login_required
def lira_boletim_dado_list_view(request, pk):
    template_name = 'dado/lira_boletim_dado_list.html'
    boletim = get_object_or_404(Boletim, pk=pk)
    object_list = LiraBoletimDado.objects.filter(boletim=pk)

    # Soma todos os tubitos do boletim
    tubitos_total = 0
    for a in object_list:
        tubitos_total += a.num_tubitos

    # banco de dados não reconheceu o distinct, 
    # metodo ste retorna uma tupla, o len conta elementos da tupla
    quarteiroes = len(set(object_list.values_list('quart')))

    # Conta quandos elementos na lista
    # Atualiza/salva o numero de imoveis
    boletim.num_imoveis = len(object_list)
    boletim.save()

    context = {
        'quarteiroes': quarteiroes,
        'tubitos_total': tubitos_total,
        'boletim': boletim,
        'object_list': object_list,
        'pk': pk
    }
    return render(request, template_name, context)


@login_required
def lira_boletim_dado_create_view(request, pk):
    lira_boletim = get_object_or_404(Boletim, id_boletim=pk)
    if request.method == 'POST':
        form = LiraBoletimDadoForm(data=request.POST)
        if form.is_valid():
            dado = form.save(commit=False)
            dado.boletim = lira_boletim
            dado.save()
            return redirect('lira_boletim_dado_list', pk)

    return render(request, 'dado/lira_boletim_dado_form.html', {
        'form': LiraBoletimDadoForm(),
    })


class LiraBoletimDadoUpdateView(LoginRequiredMixin, UpdateView):
    model = LiraBoletimDado
    fields = ['boletim', 'quart', 'rua', 'numero',
              'complemento', 'tipo', 'a1', 'a2', 'b', 'c', 'd1', 'd2']
    template_name = 'dado/lira_boletim_dado_form.html'
    success_url = reverse_lazy('lira_boletim_list')


class LiraBoletimDadoDeleteView(LoginRequiredMixin, DeleteView):
    model = LiraBoletimDado
    template_name = 'dado/lira_boletim_dado_confirm_delete.html'
    success_url = reverse_lazy('lira_boletim_list')


@login_required
def lira_boletim_dado_detail(request, pk):
    lira_boletim_dado = get_object_or_404(LiraBoletimDado, pk=pk)
    return render(request, 'dado/lira_boletim_dado_detail.html', {'lira_boletim_dado': lira_boletim_dado})


#################### Ciclo ###################################


class CicloList(LoginRequiredMixin, ListView):
    model = Ciclo
    fields = '__all__'
    template_name = 'ciclo/ciclo_list.html'


class CicloCreate(LoginRequiredMixin, CreateView):
    model = Ciclo
    fields = '__all__'
    template_name = 'ciclo/ciclo_form.html'


###################### Indice #################################

@login_required
def indice(request, ciclo):
    template_name = 'indice/indice_list.html'
    c = get_object_or_404(Ciclo, ciclo=ciclo)
    indices = Indice.objects.filter(ciclo=ciclo)

    new_indice = None  # indice postado
    '''if request.method == 'POST': 
        indice_form = IndiceForm(data=request.POST) 
        if indice_form.is_valid():                       
            # cria o indice mas não o salva no bd ainda
            new_indice = indice_form.save(commit=False)
            # actrinui o atual indice ao ciclo
            new_indice.ciclo = c
            # agora salva no bd
            new_indice.save()

    else:
        indice_form = IndiceForm()'''
    print(c)
    context = {
        'ciclo': c,
        'indices': indices,
        'new_indice': new_indice,
        # 'indice_form': indice_form,
    }

    return render(request, template_name, context)


@login_required
def indice_create_view(request, pk):
    cic = get_object_or_404(Ciclo, pk=pk)
    print(pk)
    if request.method == 'POST':
        form = IndiceForm(data=request.POST)
        if form.is_valid():
            dado = form.save(commit=False)
            dado.ciclo = cic
            dado.save()
            return redirect('indice', cic.id)

    return render(request, 'indice/indice_form.html', {
        'form': IndiceForm(),
    })


###################### Mapa ###################################


def mapa_dengue_caico(request, ciclo):
    # carregando os dados

    geojson_arquivo = "data/malha_bairro_caico.json"

    # filtrando os dados pelo ciclo
    indices = Indice.objects.filter(ciclo=ciclo)
    siglas = []
    indice = []
    # pegando as siglas e os indices
    for i in indices:
        siglas.append(i.bairro_nome.sigla)

    for i in indices:
        indice.append(float(i.indice_bairro))
    # juntando as duas listas
    dados = list(zip(siglas, indice))
    print(dados)
    # centralizando o mapa
    mapa_caico = folium.Map([-6.4648, -37.0853],
                            zoom_start=14, control_scale=True)

    # um tipo de tiles
    folium.TileLayer(tiles='https://{s}.tile.jawg.io/jawg-sunny/{z}/{x}/{y}{r}.png?access-token={accessToken}',
                     attr='<a href="http://jawg.io" title="Tiles Courtesy of Jawg Maps" target="_blank">&copy; <b>Jawg</b>Maps</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                     name='Sunny',
                     subdomains='abcd',
                     accessToken='M3WEKah99yGyp261TH3WrLRbMw82fe4LJuPqbtfwTyozuBmz67OzlNPOEwAjnW8c').add_to(mapa_caico)

    # colorir o mapa
    folium.Choropleth(
        geo_data=geojson_arquivo,
        data=dados,
        columns=["id", "Indice"],
        key_on="feature.id",
        # fill_color="GnBu",
        fill_color="YlOrRd",
        nan_fill_color="green",
        nan_fill_opacity=0.4,
        bins=[0, 1.0, 2.0, 4.0, 6.0, 8.0, 10.0, 100],
        legend_name='Indice de Infestação',
        highlight=True,
    ).add_to(mapa_caico)

    # Adicionando a fronteira dos bairros
    def estilo(x): return {"color": "black", "fillOpacity": 0, "weight": 3}

    # desenhando os bairros e add legendas
    folium.GeoJson(geojson_arquivo, style_function=estilo, tooltip=folium.GeoJsonTooltip(
        fields=["name"]), name="Caicó").add_to(mapa_caico)
    # Controle de camadas
    folium.LayerControl(position="topleft").add_to(mapa_caico)
    mapa_caico.add_child(folium.LatLngPopup())

    mapa_caico.save("mapas/mapa_do_ciclo_"+str(ciclo)+".html")

    context = {'map': mapa_caico._repr_html_(), 'ciclo': ciclo}
    return render(request, 'mapa/mapcaico.html', context)


'''


def ciclo_list(request):
    ciclos = Ciclo.objects.all()
    return render(request, 'ciclo_list.html', {'ciclos': ciclos})

def ciclo_detail(request, ciclo_id):
    ciclo = get_object_or_404(Ciclo, pk=ciclo_id)
    return render(request, 'ciclo_detail.html', {'ciclo': ciclo})

def ciclo_new(request):
    if request.method == 'POST':
        form = CicloForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('ciclo_list'))
    else:
        form = CicloForm()
    return render(request, 'ciclo_edit.html', {'form': form})

def ciclo_edit(request, ciclo_id):
    ciclo = get_object_or_404(Ciclo, pk=ciclo_id)
    if request.method == 'POST':
        form = CicloForm(request.POST, instance=ciclo)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('ciclo_list'))
    else:
        form = CicloForm(instance=ciclo)
    return render(request, 'ciclo_edit.html', {'form': form})

def ciclo_delete(request, ciclo_id):
    ciclo = get_object_or_404(Ciclo, pk=ciclo_id)
    ciclo.delete()
    return HttpResponseRedirect(reverse('ciclo_list'))




%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (CreateView, ListView, UpdateView, DeleteView)

from .models import (Bairro, Rua, Quarteirao, Imovel, LiraBoletim, LiraBoletimDado)

class BairroListView(LoginRequiredMixin, ListView):
    model = Bairro
    template_name = 'bairro_list.html'

class BairroCreateView(LoginRequiredMixin, CreateView):
    model = Bairro
    fields = ['sigla', 'nome']
    template_name = 'bairro_form.html'
    success_url = reverse_lazy('bairro_list')

class BairroUpdateView(LoginRequiredMixin, UpdateView):
    model = Bairro
    fields = ['sigla', 'nome']
    template_name = 'bairro_form.html'
    success_url = reverse_lazy('bairro_list')

class BairroDeleteView(LoginRequiredMixin, DeleteView):
    model = Bairro
    template_name = 'bairro_confirm_delete.html'
    success_url = reverse_lazy('bairro_list')

class RuaListView(LoginRequiredMixin, ListView):
    model = Rua
    template_name = 'rua_list.html'

class RuaCreateView(LoginRequiredMixin, CreateView):
    model = Rua
    fields = ['nome']
    template_name = 'rua_form.html'
    success_url = reverse_lazy('rua_list')

class RuaUpdateView(LoginRequiredMixin, UpdateView):
    model = Rua
    fields = ['nome']
    template_name = 'rua_form.html'
    success_url= reverse_lazy('rua_list')

class RuaDeleteView(LoginRequiredMixin, DeleteView):
    model = Rua
    template_name = 'rua_confirm_delete.html'
    success_url = reverse_lazy('rua_list')

class QuarteiraoListView(LoginRequiredMixin, ListView):
    model = Quarteirao
    template_name = 'quarteirao_list.html'

class QuarteiraoCreateView(LoginRequiredMixin, CreateView):
    model = Quarteirao
    fields = ['bairro', 'numero']
    template_name = 'quarteirao_form.html'
    success_url = reverse_lazy('quarteirao_list')

class QuarteiraoUpdateView(LoginRequiredMixin, UpdateView):
    model = Quarteirao
    fields = ['bairro', 'numero']
    template_name = 'quarteirao_form.html'
    success_url = reverse_lazy('quarteirao_list')

class QuarteiraoDeleteView(LoginRequiredMixin, DeleteView):
    model = Quarteirao
    template_name = 'quarteirao_confirm_delete.html'
    success_url = reverse_lazy('quarteirao_list')

class ImovelListView(LoginRequiredMixin, ListView):
    model = Imovel
    template_name = 'imovel_list.html'

class ImovelCreateView(LoginRequiredMixin, CreateView):
    model = Imovel
    fields = ['numero', 'complemento', 'tipo', 'quarteirao', 'lado', 'rua']
    template_name = 'imovel_form.html'
    success_url = reverse_lazy('imovel_list')

class ImovelUpdateView(LoginRequiredMixin, UpdateView):
    model = Imovel
    fields = ['numero', 'complemento', 'tipo', 'quarteirao', 'lado', 'rua']
    template_name = 'imovel_form.html'
success_url = reverse_lazy('imovel_list')

class ImovelDeleteView(LoginRequiredMixin, DeleteView):
    model = Imovel
    template_name = 'imovel_confirm_delete.html'
    success_url = reverse_lazy('imovel_list')

class LiraBoletimListView(LoginRequiredMixin, ListView):
    model = LiraBoletim
    template_name = 'lira_boletim_list.html'

class LiraBoletimCreateView(LoginRequiredMixin, CreateView):
    model = LiraBoletim
    fields = ['bairro', 'num_quart', 'num_imoveis', 'extrato', 'usuario']
    template_name = 'lira_boletim_form.html'
    success_url = reverse_lazy('lira_boletim_list')

class LiraBoletimUpdateView(LoginRequiredMixin, UpdateView):
    model = LiraBoletim
    fields = ['bairro', 'num_quart', 'num_imoveis', 'extrato', 'usuario']
    template_name = 'lira_boletim_form.html'
    success_url = reverse_lazy('lira_boletim_list')

class LiraBoletimDeleteView(LoginRequiredMixin, DeleteView):
    model = LiraBoletim
    template_name = 'lira_boletim_confirm_delete.html'
    success_url = reverse_lazy('lira_boletim_list')

class LiraBoletimDadoListView(LoginRequiredMixin, ListView):
    model = LiraBoletimDado
    template_name = 'lira_boletim_dado_list.html'

class LiraBoletimDadoCreateView(LoginRequiredMixin, CreateView):
    model = LiraBoletimDado
    fields = ['boletim', 'quart', 'rua', 'numero', 'complemento', 'tipo', 'a1', 'a2', 'b', 'c', 'd1', 'd2']
    template_name = 'lira_boletim_dado_form.html'
    success_url = reverse_lazy('lira_boletim_dado_list')

class LiraBoletimDadoUpdateView(LoginRequiredMixin, UpdateView):
    model = LiraBoletimDado
    fields = ['boletim', 'quart', 'rua', 'numero', 'complemento', 'tipo', 'a1', 'a2', 'b', 'c', 'd1', 'd2']
    template_name = 'lira_boletim_dado_form.html'
    success_url = reverse_lazy('lira_boletim_dado_list')

class LiraBoletimDadoDeleteView(LoginRequiredMixin, DeleteView):
    model = LiraBoletimDado
    template_name = 'lira_boletim_dado_confirm_delete.html'
    success_url = reverse_lazy('lira_boletim_dado_list')

def lira_boletim_dado_detail(request, pk):
    lira_boletim_dado = get_object_or_404(LiraBoletimDado, pk=pk)
    return render(request, 'lira_boletim_dado_detail.html', {'lira_boletim_dado': lira_boletim_dado})

'''
