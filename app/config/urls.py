
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),
    path('api/', include('yorozu.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# http://127.0.0.1:8081/api/auth/jwt/createに
# メールアドレスとpasswordを送るとトークンが帰ってくる
