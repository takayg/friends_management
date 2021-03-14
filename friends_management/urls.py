from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import static
from .settings import base

urlpatterns = [
    path('', include('friend.urls')),
    path('admin/', admin.site.urls),
    path('login/', include('accounts.urls')),
    path('event/', include('event.urls')),
]

# Settings that allow media to be distributed on the development server
urlpatterns += static(
    base.MEDIA_URL,
    document_root=base.MEDIA_ROOT
)
