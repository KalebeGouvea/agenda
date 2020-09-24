from django.shortcuts import render, HttpResponse, redirect
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime, timedelta
from django.http.response import Http404, JsonResponse
from django.contrib.auth.models import User

# Create your views here.
"""def retorna_local(request, titulo_evento):
    Evento.objects.get(titulo=titulo_evento)
    return HttpResponse(f'<h1>Local: {Evento.local}</h1>')"""

def index(request):
    return redirect('/agenda')

def login_user(request):
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('/')

def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('/')
        else:
            messages.error(request,'Usuário ou senha inválida')
            return redirect('/')

@login_required(login_url='/login/')
def lista_eventos(request):
    user = request.user
    data_agora = datetime.now() - timedelta(hours=1)
    evento = Evento.objects.filter(usuario=user, data_evento__gt=data_agora)
    dados = {'eventos':evento}
    return render(request, 'agenda.html', dados)

@login_required(login_url='/login/')
def evento(request):
    id_evento = request.GET.get('id')
    dados = {}
    if id_evento:
        dados['evento'] = Evento.objects.get(id=id_evento)
    return render(request, 'evento.html', dados)

@login_required(login_url='/login/')
def submit_evento(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        data_evento = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        local = request.POST.get('local')
        id_evento = request.POST.get('id_evento')
        usuario = request.user
        if id_evento:
            Evento.objects.filter(id=id_evento).update(titulo=titulo, data_evento=data_evento, descricao=descricao, local=local)
        else:
            Evento.objects.create(titulo=titulo, data_evento=data_evento, descricao=descricao, local=local, usuario=usuario)
    return redirect('/')

@login_required(login_url='/login/')
def delete_evento(request, id_evento):
    usuario = request.user
    try:
        evento = Evento.objects.get(id=id_evento)
    except Exception:
        raise Http404()
    if usuario == evento.usuario:
        evento.delete()
    else:
        raise Http404()
    return redirect('/')

def json_lista_evento(request, id_usuario):
    usuario = User.objects.get(id=id_usuario)
    evento = Evento.objects.filter(usuario=usuario).values('id', 'titulo')
    return JsonResponse(list(evento), safe=False)