from django.contrib.auth.mixins import LoginRequiredMixin # para cbv
from django.contrib.auth.decorators import login_required # para fbv
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Bairro, Rua, LiraBoletim as Boletim, LiraBoletimDado
from .forms import LiraBoletimDadoForm

class BairroListView(LoginRequiredMixin, ListView):
    model = Bairro
    template_name = 'myapp/bairro_list.html'


class BairroCreateView(LoginRequiredMixin, CreateView):
    model = Bairro
    fields = ['sigla', 'nome']
    template_name = 'quart/bairro_form.html'
    success_url = reverse_lazy('bairro_list')


class BairroUpdateView(LoginRequiredMixin, UpdateView):
    model = Bairro
    fields = ['sigla', 'nome']
    template_name = 'quart/bairro_form.html'
    success_url = reverse_lazy('bairro_list')


class BairroDeleteView(LoginRequiredMixin, DeleteView):
    model = Bairro
    template_name = 'quart/bairro_confirm_delete.html'
    success_url = reverse_lazy('bairro_list')

################## Rua #########################################


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
    success_url = reverse_lazy('rua_list')


class RuaDeleteView(LoginRequiredMixin, DeleteView):
    model = Rua
    template_name = 'rua_confirm_delete.html'
    success_url = reverse_lazy('rua_list')


################## LiraBoletim #################################

class LiraBoletimListView(LoginRequiredMixin, ListView):
    model = Boletim
    template_name = 'quart/lira_boletim_list.html'

    def get_queryset(self):
        u = self.request.user

        # listagem para os chefes
        if u.is_staff == True and u.is_superuser == False: 
            return Boletim.objects.filter(chefe=u).order_by('bairro')
        
        # listagem para o digitador (superusuário)
        elif u.is_staff == True and u.is_superuser == True:            
            return Boletim.objects.all().order_by('usuario')
        
        # listagem para os ACEs
        else:
            return Boletim.objects.filter(usuario=u)


class LiraBoletimCreateView(LoginRequiredMixin, CreateView):
    model = Boletim
    fields = ['bairro', 'num_quart', 'num_imoveis', 'extrato', 'chefe']
    template_name = 'quart/lira_boletim_form.html'
    success_url = reverse_lazy('lira_boletim_list')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)



class LiraBoletimUpdateView(LoginRequiredMixin, UpdateView):
    model = Boletim
    fields = ['bairro', 'num_quart', 'num_imoveis', 'extrato', 'chefe']
    template_name = 'quart/lira_boletim_form.html'
    success_url = reverse_lazy('lira_boletim_list')

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class LiraBoletimDeleteView(LoginRequiredMixin, DeleteView):
    model = Boletim
    template_name = 'quart/lira_boletim_confirm_delete.html'
    success_url = reverse_lazy('lira_boletim_list')


@login_required
def liraboletim_detail(request, pk):
    template_name = 'quart/liraboletim_detail.html'
    boletim = get_object_or_404(Boletim, pk=pk)
    context = {
        'boletim': boletim,
        'pk': pk
    }
    return render(request, template_name, context)


################### LiraBoletimDado ##################################

@login_required
def LiraBoletimDadoListView(request, pk):
    template_name = 'quart/lira_boletim_dado_list.html'
    object_list = LiraBoletimDado.objects.filter(boletim=pk)

    context = {
        'object_list': object_list,
        'pk': pk
    }
    return render(request, template_name, context)


@login_required
def LiraBoletimDadoCreateView(request, pk):    
    liraBoletim = get_object_or_404(Boletim,id_boletim=pk)
    if request.method == 'POST':
        form = LiraBoletimDadoForm(data=request.POST)
        if form.is_valid():
            dado = form.save(commit=False)
            dado.boletim = liraBoletim
            dado.save()
            return redirect('lira_boletim_dado_list', pk)
    
    return render(request, 'quart/lira_boletim_dado_form.html', {
        'form': LiraBoletimDadoForm(),
    })


class LiraBoletimDadoUpdateView(LoginRequiredMixin, UpdateView):
    model = LiraBoletimDado
    fields = ['boletim', 'quart', 'rua', 'numero',
              'complemento', 'tipo', 'a1', 'a2', 'b', 'c', 'd1', 'd2']
    template_name = 'quart/lira_boletim_dado_form.html'
    success_url = reverse_lazy('lira_boletim_list')


class LiraBoletimDadoDeleteView(LoginRequiredMixin, DeleteView):
    model = LiraBoletimDado
    template_name = 'quart/lira_boletim_dado_confirm_delete.html'
    success_url = reverse_lazy('lira_boletim_list')


@login_required
def lira_boletim_dado_detail(request, pk):
    lira_boletim_dado = get_object_or_404(LiraBoletimDado, pk=pk)
    return render(request, 'quart/lira_boletim_dado_detail.html', {'lira_boletim_dado': lira_boletim_dado})


# Create your views here.


class LiraBoletim(LoginRequiredMixin, ListView):
    model = Boletim
    fields = '__all__'
    template_name = 'index.html'





'''
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
