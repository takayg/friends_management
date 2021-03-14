from django.urls import path
from . import views

""" match when url is [/]"""

app_name = 'friend'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('friend_list/', views.FriendListView.as_view(), name='friend_list'),
    path('friend_detail/<int:pk>/', views.FriendDetailView.as_view(), name='friend_detail'),
    path('friend_create/', views.FriendCreateView.as_view(), name='friend_create'),
    path('friend_update/<int:pk>/', views.FriendUpdateView.as_view(), name='friend_update'),
    path('friend_delete/<int:pk>/', views.FriendDeleteView.as_view(), name='friend_delete'),
    path('friend_event_list/<int:pk>/', views.FriendEventListView.as_view(), name='friend_event_list'),
]