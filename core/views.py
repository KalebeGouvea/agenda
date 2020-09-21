from django.shortcuts import render, HttpResponse, redirect
from core.models import Evento

# Create your views here.
"""def retorna_local(request, titulo_evento):
    Evento.objects.get(titulo=titulo_evento)
    return HttpResponse(f'<h1>Local: {Evento.local}</h1>')"""

def index(request):
    return redirect('/agenda')

def lista_eventos(request):
    evento = Evento.objects.all()
    dados = {'eventos':evento}
    return render(request, 'agenda.html', dados)