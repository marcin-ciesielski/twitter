from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include
from django.urls import path

urlpatterns = [
    path('', include('twitter.urls')),
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
]