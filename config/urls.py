from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('artists/', include('artists.urls')),
    path('groups/', include('groups.urls')),
    path('catalog/', include('catalog.urls')),
    path('', include('core.urls')),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

