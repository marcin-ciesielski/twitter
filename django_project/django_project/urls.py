from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.template.context_processors import static
from django.urls import include
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('twitter.urls')),
    path('avatar/', include('avatar.urls')),
    path('admin/', admin.site.urls),
    path('login/',
         auth_views.LoginView.as_view(template_name='twitter/login.html'),
         name='login'),
    path('logout/',
         auth_views.LogoutView.as_view(template_name='twitter/logout.html'),
         name='logout'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='twitter/password_reset.html'),
         name='password-reset'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)