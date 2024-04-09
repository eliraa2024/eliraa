from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.models import User

from .forms import RegisterForm

from django import forms


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            #User.objects.create_user(form)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'registration/signup.html', {'form': form})


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("home")
    template_name = "registration/signup.html"
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



def email_is_valid(request):
    # Recupera uma lista de todos os emails dos usuários ativos
    emails_dos_usuarios = User.objects.filter(is_active=True).values_list('email', flat=True)

    # Supondo que 'emails_dos_usuarios' seja a lista de emails que você recuperou anteriormente
    email_para_testar = request.cleaned_data.get('email')
    print('O email está cadastrado.', email_para_testar)
    if request.method == 'POST':
        # Verifica se o email está na lista
        if email_para_testar in emails_dos_usuarios:
            print('O email está cadastrado.')
            return render(request, 'password_reset_done.html')
    else:
        return render(request, 'password_reset_done.html')

