# fantasma_project/urls.py

from django.contrib import admin
from django.urls import path, include
from main.views import LogoutViewAllowGet
from django.contrib.auth import views as auth_views
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Página principal protegida
    path('', views.home, name='home'),

    # Login / Logout
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('logout/', LogoutViewAllowGet.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),
    path('register/success/', views.register_success, name='register_success'),
]
