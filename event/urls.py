from django.urls import path
from . import views

""" match when url is [/event/]"""

app_name = 'event'

urlpatterns = [
    path('calendar/', views.CalendarRedirectView.as_view(), name='calendar_redirect'),
    path('calendar/<int:year>/<int:month>/', views.CalendarView.as_view(), name='calendar'),
    path('event_create/<int:year>/<int:month>/<int:day>/', views.EventCreateView.as_view(), name='event_create'),
    path('add_friend/<int:pk>/', views.add_friend, name='add_friend'),
    path('event_detail/<int:pk>', views.EventDetailView.as_view(), name='event_detail'),
    path('event_update/<int:pk>', views.EventUpdateView.as_view(), name='event_update'),
    path('update_friend/<int:pk>/', views.update_friend, name='update_friend'),
    path('event_delete/<int:pk>', views.EventDeleteView.as_view(), name='event_delete'),
]