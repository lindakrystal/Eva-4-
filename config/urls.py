from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from django.contrib.auth import views as auth_views  # LOGIN / LOGOUT
from inventario.views import inicio_view  # VISTA INICIO

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

from inventario.views import (
    CategoriaViewSet,
    ProveedorViewSet,
    ProductoViewSet,
    MovimientoStockViewSet,
)

# ------------------------------
# ROUTER REST FRAMEWORK
# ------------------------------
router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet)
router.register(r'proveedores', ProveedorViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'movimientos', MovimientoStockViewSet)


# ------------------------------
# URLS PRINCIPALES
# ------------------------------
urlpatterns = [
    path('admin/', admin.site.urls),

    # LOGIN Y LOGOUT
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),

    # PÁGINA DE INICIO DEL SISTEMA
    path('', inicio_view, name='inicio'),

    # CRUD VISUAL DEL INVENTARIO (categorías, productos, movimientos)
    path('', include('inventario.urls')),

    # API REST
    path('api/', include(router.urls)),

    # Autenticación por Token
    path('api/api-token-auth/', obtain_auth_token, name='api_token_auth'),

    # Documentación OpenAPI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
