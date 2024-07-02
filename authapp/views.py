from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm

def loginCustom(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('main:home')
        else:
            print(form.errors)
    return render(request, 'authapp/login.html', {'form': form})

@login_required
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('main:settings')
    else:
        form = CustomUserCreationForm()
    return render(request, 'authapp/register.html', {'form': form})


def logoutCustom(request):
	logout(request)
	return redirect('auth:login')
