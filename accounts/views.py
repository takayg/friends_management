from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from .forms import LoginForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

class Login(LoginView):
    """ Login Page """

    form_class = LoginForm
    template_name = 'login.html'

class Logout(LoginRequiredMixin, LogoutView):
    """ Logout Page """

    template_name = 'index.html'

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('friend:index')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})