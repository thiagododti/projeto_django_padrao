
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect


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
            return render(request, 'configuracoes/login.html', {'error': 'Usuário ou senha inválidos, ou usuário inativo.'})
    return render(request, 'configuracoes/login.html')
