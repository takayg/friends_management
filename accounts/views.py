from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginForm

""" View for Login """
class Login(LoginView):

    form_class = LoginForm
    template_name = 'login.html'

""" View for Logout """
class Logout(LoginRequiredMixin, LogoutView):

    template_name = 'index.html'

""" View for Signup """
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