from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required

from .forms import RegisterForm

@staff_member_required # somente staff tem acesso
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

