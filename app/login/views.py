from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import FormularioLogin

# Create your views here.
def loginPage(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('cliente'))
    if request.method == 'POST':
        formulario = FormularioLogin(request.POST)
        if formulario.is_valid():
            usuario = request.POST['username']
            clave = request.POST['password']
            user = authenticate(username=usuario, password=clave)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.warning(request, 'logueado correcto')
                    return HttpResponseRedirect(reverse('cliente'))
                else:
                    messages.warning(request, 'Usuario inactivo')
            else:
                messages.warning(request, 'Usuario y/o contraseña incorrectos')
    else:
        formulario = FormularioLogin()

    context = {
        'f': formulario,
    }
    return render (request, 'login/login.html', context)

def logoutPage(request):
    messages.warning(request, 'Sesión Cerrada con Exito')
    logout(request)
    return HttpResponseRedirect(reverse('home_Page'))
