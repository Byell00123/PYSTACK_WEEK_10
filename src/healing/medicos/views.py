from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import DatasAbertas, Especialidades, DadosMedico, is_medico
from django.contrib.messages import constants
from django.contrib import messages
from datetime import datetime, timedelta
from pacientes.models import Consulta

@login_required
def cadastro_medico(request):
    if is_medico(request.user):
        messages.add_message(request, constants.ERROR, 'Você já está cadastrado como médico.')
        return redirect('/medicos/abrir_horario/')
    
    elif request.method == "GET":
        especialidade = Especialidades.objects.all()
        return render(request, 'cadastro_medico.html', {'Especialidades': especialidade})
    
    elif request.method == "POST":
        crm = request.POST.get('crm')
        nome = request.POST.get('nome')
        cep = request.POST.get('cep')
        rua = request.POST.get('rua')
        bairro = request.POST.get('bairro')
        numero = request.POST.get('numero')
        cim = request.FILES.get('cim')  #TODO: ` request.FILES.get ´ e não ` request.POST.get ´ ja que o campo <input> la no HTML é do ` type="file" ´.
        rg = request.FILES.get('rg')    #TODO: ` request.FILES.get ´ e não ` request.POST.get ´ ja que o campo <input> la no HTML é do ` type="file" ´.
        foto = request.FILES.get('foto')
        especialidade = request.POST.get('especialidade') #TODO: Vai trazer uma chave primaria(id) de uma das especialidades da tabela especialidades.
        descricao = request.POST.get('descricao')
        valor_consulta = request.POST.get('valor_consulta')

        #TODO: Validar todos os campos
        cria_medico = DadosMedico(
            crm=crm,
            nome=nome,
            cep=cep,
            rua=rua,
            bairro=bairro,
            numero=numero,
            rg=rg,
            cedula_identidade_medica=cim,
            foto=foto,
            user=request.user,
            descricao=descricao,
            especialidade_id=especialidade, #TODO: Pega o id passado no <select name="especialidade"><option value="{{i.id}}"> e atrubiur o value="{{i.id}} a especialidade que
            # devido a uma caracteristica do Django, na hora de migrar a tabela ele adiciona ` _id ´ ao final do nome das FK o que faz com que na hora de inserir um dado na tabela
            # o valo a forma de chamar as FK para receber um valor deve seguir a o padrão (NOME_DA_FK + _id) e nesse caso da FK especilidade fica ` especialidade_id ´.
            valor_consulta=valor_consulta
        )
        
        cria_medico.save()

        messages.add_message(request, constants.SUCCESS, 'Cadastro médico realizado com sucesso.')

        return redirect('/medicos/abrir_horario/')
    
@login_required
def abrir_horario(request):

    if not is_medico(request.user):

        messages.add_message(request, constants.WARNING, 'Somente médicos podem acessar essa página.')
        return redirect('/usuarios/sair/')

    if request.method == "GET":
        dados_medicos = DadosMedico.objects.get(user=request.user)
        datas_abertas = DatasAbertas.objects.filter(user=request.user)
        return render(request, 'abrir_horario.html', {'dados_medicos': dados_medicos, 'datas_abertas': datas_abertas})
    elif request.method == "POST":
        data = request.POST.get('data')
        data_formatada = datetime.strptime(data, "%Y-%m-%dT%H:%M")
        
        if data_formatada <= datetime.now():
            messages.add_message(request, constants.WARNING, 'A data deve ser maior ou igual a data atual.')
            return redirect('/medicos/abrir_horario/')

        horario_abrir = DatasAbertas(
            data=data,
            user=request.user
        )
        horario_abrir.save()


        messages.add_message(request, constants.SUCCESS, 'Horário cadastrado com sucesso.')
        return redirect('/medicos/abrir_horario/')

@login_required
def consultas_medico(request):
    if not is_medico(request.user):
        messages.add_message(request, constants.WARNING, 'Somente médicos podem acessar essa página.')
        return redirect('/usuarios/sair/')
    
    hoje = datetime.now().date()

    consultas_hoje = Consulta.objects.filter(data_aberta__user=request.user).filter(data_aberta__data__gte=hoje).filter(data_aberta__data__lt=hoje + timedelta(days=1))
    consultas_restantes = Consulta.objects.exclude(id__in=consultas_hoje.values('id'))

    return render(request, 'consultas_medico.html', {'consultas_hoje': consultas_hoje, 'consultas_restantes': consultas_restantes, 'is_medico': is_medico(request.user)})
