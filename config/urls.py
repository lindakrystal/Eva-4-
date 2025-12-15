from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from rest_framework.authtoken import views as token_views

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

from inventario.views import inicio_view, logout_view

urlpatterns = [
    # =========================
    # ADMIN
    # =========================
    path('admin/', admin.site.urls),

    # =========================
    # LOGIN / LOGOUT
    # =========================
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='login.html'),
        name='login'
    ),
    path('logout/', logout_view, name='logout'),

    # =========================
    # 👉 RAÍZ SIEMPRE AL LOGIN
    # =========================
    path('', auth_views.LoginView.as_view(template_name='login.html')),

    # =========================
    # DASHBOARD
    # =========================
    path('inicio/', inicio_view, name='inicio'),

    # =========================
    # INVENTARIO (HTML)
    # =========================
    path('inventario/', include('inventario.urls')),

    # =========================
    # API REST
    # =========================
    path('api/', include('inventario.api_urls')),

    # =========================
    # API TOKEN
    # =========================
    path('api/token/', token_views.obtain_auth_token, name='api_token_auth'),

    # =========================
    # API DOCUMENTATION
    # =========================
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui'
    ),
    path(
        'api/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc'
    ),
]
