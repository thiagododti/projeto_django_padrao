from ..forms import RegistrarUsuario
from django.contrib import messages
from django.shortcuts import render, redirect


def registrar(request):
    if request.method == "POST":
        form = RegistrarUsuario(request.POST, request.FILES)
        if form.is_valid():
            usuario = form.save(commit=False)
            senha = form.cleaned_data.get("password1")
            usuario.set_password(senha)
            usuario.is_active = True
            usuario.save()

            messages.success(request, "Cadastro realizado com sucesso!")
            return redirect("login")
    else:
        form = RegistrarUsuario()

    return render(request, 'configuracoes/registrar.html', {'form': form})
