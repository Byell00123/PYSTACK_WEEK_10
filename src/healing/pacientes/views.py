from django.shortcuts import render
from . import models
from .models import DatasAbertas, Consulta
from medicos.models import DadosMedico, DatasAbertas, Especialidades
from datetime import datetime
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.messages import constants
from django.contrib import messages


def home(request):
    if request.method == "GET":
        medico_filtrar = request.GET.get('medico')
        medicos = DadosMedico.objects.all()
        especialidades = Especialidades.objects.all()  # Corrigido aqui
        especialidades_filtrar = request.GET.getlist('especialidades') 

        if medico_filtrar:
            medicos = medicos.filter(nome__icontains = medico_filtrar)

        if especialidades_filtrar:
            medicos = medicos.filter(especialidade_id__in=especialidades_filtrar)
        return render(request, 'home.html', {'medicos': medicos, 'especialidades': especialidades})

@login_required
def escolher_horario(request, id_dados_medicos):
    if request.method == "GET":
        medico = DadosMedico.objects.get(id=id_dados_medicos)
        datas_abertas = DatasAbertas.objects.filter(user=medico.user).filter(data__gte=datetime.now()).filter(agendado=False)
        return render(request, 'escolher_horario.html', {'medico': medico, 'datas_abertas': datas_abertas})

@login_required
def agendar_horario(request, id_data_aberta):
    if request.method == "GET":
        data_aberta = DatasAbertas.objects.get(id=id_data_aberta)

        horario_agendado = Consulta(
            paciente=request.user,
            data_aberta=data_aberta
        )

        horario_agendado.save()

        # TODO: Sugestão Tornar atomico

        data_aberta.agendado = True
        data_aberta.save()

        messages.add_message(request, constants.SUCCESS, 'Horário agendado com sucesso.')

        return redirect('/pacientes/minhas_consultas/')

@login_required
def minhas_consultas(request):
    if request.method == "GET":
        #TODO: desenvolver o filtros igual la no home
        minhas_consultas = Consulta.objects.filter(paciente=request.user).filter(data_aberta__data__gte=datetime.now())
        return render(request, 'minhas_consultas.html', {'minhas_consultas': minhas_consultas})

