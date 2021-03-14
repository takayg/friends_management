from django.urls import path
from . import views

""" match when url is [/login/]"""

app_name = 'accounts'

urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
]