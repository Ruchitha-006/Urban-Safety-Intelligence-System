from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def home(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    return redirect('/login')


@login_required(login_url='/login')
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')