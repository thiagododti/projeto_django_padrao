from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..forms import UsuarioPerfil
from django.shortcuts import render, redirect


@login_required
def perfil(request):
    user = request.user

    if request.method == 'POST':
        form = UsuarioPerfil(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()  # Agora vai manter a imagem anterior automaticamente
            return redirect('perfil')
    else:
        form = UsuarioPerfil(instance=user)

    return render(request, 'configuracoes/perfil.html', {'form': form, 'user': user})
