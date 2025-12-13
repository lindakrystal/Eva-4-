from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

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
        auth_views.LoginView.as_view(
            template_name='login.html'
        ),
        name='login'
    ),

    path('logout/', logout_view, name='logout'),

    # =========================
    # DASHBOARD
    # =========================
    path('', inicio_view, name='inicio'),
    path('inicio/', inicio_view, name='inicio'),

    # =========================
    # INVENTARIO (CRUD)
    # =========================
    path('inventario/', include('inventario.urls')),

    # =========================
    # API REST
    # =========================
    path('api/', include('inventario.api_urls')),

    # =========================
    # API DOCUMENTATION (SWAGGER / REDOC)
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
