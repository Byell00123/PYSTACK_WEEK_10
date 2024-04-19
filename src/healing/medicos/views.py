from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Especialidades, DadosMedico, is_medico
from django.contrib.messages import constants
from django.contrib import messages

@login_required
def cadastro_medico(request):
    if is_medico(request.user):
        messages.add_message(request, constants.ERROR, 'Você já está cadastrado como médico.')
        return redirect('/medicos/abrir_horario') #TODO: Sera feito somente na segunda aula do curso, por enquanto deve dar o erro 404(pagina não encontrada)
    
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

        return redirect('/medicos/abrir_horario') #TODO: Sera feito somente na segunda aula do curso, por enquanto deve dar o erro 404(pagina não encontrada)