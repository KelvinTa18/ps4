from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
# Create your views here.


def login_def(request):
    # return HttpResponse("Login")
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if (form.is_valid()):
            # Login
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, form.get_user())
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                return redirect('Schedule:read')
    else:
        form = AuthenticationForm()
    return render(request, "user/login.html", {"form": form})


def register_def(request):
    # return HttpResponse("Register")
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if (form.is_valid()):
            # form.save() will return username
            login(request, form.save())
            return redirect('Schedule:read')
    else:
        form = UserCreationForm()
    return render(request, "user/register.html", {"form": form})


def logout_def(request):
    if request.method == "POST":
        logout(request)
    return redirect('Schedule:read')
