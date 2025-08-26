from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect


@login_required()
def logout_view(request):
    logout(request)
    return redirect('login')
