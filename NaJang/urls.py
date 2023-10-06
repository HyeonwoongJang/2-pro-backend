from django.contrib import admin
from django.urls import path, include
from NaJang import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include("users.urls")),
]

# 개발 중에만 이 방식으로 사용하도록 설정.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)