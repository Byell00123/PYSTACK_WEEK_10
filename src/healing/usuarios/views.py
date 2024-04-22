from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib import auth

def cadastro(request): # http://127.0.0.1:8000/usuarios/cadastro/

    if request.method == "GET":
        return render(request, 'cadastro.html')
    elif request.method == "POST":
        nome_usuario = request.POST.get('nome_usuario')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        compara_usuarios = User.objects.filter(username=nome_usuario) # Exibe --> <QuerySet []> <-- E Retorna True(se tiver algo no colchetes) ou False(se não tiver algo no colchetes),
        # e True significa que esse valor de nome_usuario ja exite no Banco de Dados e False significa que esse valor de nome_usuario não exite no Banco de Dados logo podendo ser utilizado.

        if compara_usuarios.exists():  # Se compara_username == True, não permite criar o usuario pois ja existe alguem com aquele nome_usuario
            messages.add_message(request,constants.ERROR, "Este nome de usuário já está em uso. Por favor, escolha outro.")
            return redirect('/usuarios/cadastro/')

        elif senha != confirmar_senha:
            messages.add_message(request,constants.WARNING, "As senhas não correspondem. Por favor, verifique e tente novamente.")
            return redirect('/usuarios/cadastro/')

        elif len(senha) < 8 or valida_senha(request): #Se a senha tiver menos que 8 digitos ou a Senha for True(se não tiver caracters especiais + 0-9 + A-Z + a-z), 
            messages.add_message(request, constants.WARNING, "A senha precisa ter pelo menos 8 caracteres e incluir pelo menos um dos seguintes caracteres especiais: *, @, -, _. Além disso, a senha deve conter pelo menos um número, uma letra maiúscula e uma letra minúscula.")
            return redirect('/usuarios/cadastro/')

        try:
            cria_usuario = User.objects.create_user(username=nome_usuario, email=email, password=senha)
            # messages.info(request, "Você tem novas mensagens.")
            return redirect('/usuarios/login/') #TODO: Colocar uma mensagem aqui
        except:
            messages.add_message(request,constants.ERROR, "Algo inesperado aconteceu durante a criação do seu cadastro. Por favor, tente novamente.")
            return redirect('/usuarios/login/')

def login_view(request): # http://127.0.0.1:8000/usuarios/login/

    if request.method == "GET":
        return render(request,'login.html')
    
    elif request.method == "POST":
        nome_usuario = request.POST.get('nome_usuario')
        senha = request.POST.get('senha')

        valida_usuario = auth.authenticate(request, username=nome_usuario, password=senha) #Retorna True(se tiver usuario cadatrado com essas dados) ou False(se não tiver usuario 
# cadatrado com essas dados). True significa que esse valor de nome_usuario ja exite no Banco de Dados e False significa que esse valor de nome_usuario não exite no Banco de Dados 
# logo podendo ser utilizado.

        if valida_usuario: # Se valida_usuario == True, o usuario ja existe e sera feito o login
            auth.login(request, valida_usuario)
            #if not User.is_active: #TODO: Devido a forma que esta sendo feito o cadastro otdos os usuarios são ativados, depois precisa mudar isso para exibir a mensagem
            messages.info(request, "A primeira etapa do cadastro foi concluída com sucesso! Agora é só ativar sua conta adicionando mais alguns detalhes. Fique atento ao seu e-mail para as próximas instruções.")
                #return redirect('/pacientes/home/')
            return redirect('/pacientes/home/')
            
        messages.add_message(request, constants.ERROR, "Nome de Usuario e/ou senha errado")
        return redirect('/usuarios/login/')

def sair(resquest): # http://127.0.0.1:8000/usuarios/sair/
    auth.logout(resquest)
    return redirect('/usuarios/login/')

def valida_senha(request):
    #TODO: Depois trazer o o ` elif senha != confirmar_senha: ´ para essa função.
    senha = request.POST.get('senha')
    caracteresp = 0
    letrasmai = 0
    letrasmin = 0
    numero = 0
    
    for i in senha:
        if i == "*" or i == "@" or i == "-" or i == "_":
            caracteresp += 1
        elif i.isupper(): # isupper() == letras maiúsculas.
            letrasmai += 1
        elif i.islower(): # islower() == letras minúsculas.
            letrasmin += 1
        elif i.isdigit(): # isdigit() == numeros de 0 a 9
            numero += 1
            
    if caracteresp < 1 or letrasmai < 1 or letrasmin < 1 or numero < 1:
        return True # É Verdadeiro o afirmação de que a senha é ruim. Ou tente entender como: é Verdadeiro que senha reprovou em algo
    else:
        return False # É Falso o afirmação de que a senha é ruim. Ou tente entender como: é Falso que senha reprovou em algo