from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


def login_view(request):
    if request.method == 'POST':
        # Aqui você pode adicionar a lógica de autenticação
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Verifique as credenciais do usuário
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Se as credenciais forem válidas, faça o login
            login(request, user)
            return redirect('index')
        else:
            # Se as credenciais forem inválidas, exiba uma mensagem de erro
            return render(request, 'usuarios/login.html', {'error': 'Credenciais inválidas'})
    return render(request, 'usuarios/login.html')


@login_required()
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required()
def index(request):
    # Renderiza a página inicial para usuários autenticados
    return render(request, 'usuarios/index.html', {'user': request.user})
