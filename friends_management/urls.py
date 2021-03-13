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

# 開発サーバでメディアを配信できるようにする設定
urlpatterns += static(
    base.MEDIA_URL,
    document_root=base.MEDIA_ROOT
)
