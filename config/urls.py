from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from inventario.views import inicio_view, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),

    # LOGIN
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='login.html'
        ),
        name='login'
    ),

    # LOGOUT CON MENSAJE
    path('logout/', logout_view, name='logout'),

    # DASHBOARD (PROTEGIDO)
    path('', inicio_view, name='inicio'),

    # INVENTARIO
    path('inventario/', include('inventario.urls')),
]
