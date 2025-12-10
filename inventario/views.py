from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Categoria, Proveedor, Producto, MovimientoStock
from .serializers import (
    CategoriaSerializer,
    ProveedorSerializer,
    ProductoSerializer,
    MovimientoStockSerializer,
)


# Permiso personalizado: solo admin puede modificar, usuarios normales solo leen
class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Lectura para cualquier usuario autenticado.
    Escritura solo para usuarios staff.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            return request.user.is_authenticated
        return request.user.is_staff


# -------------------------------
# CATEGORÍAS
# -------------------------------
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsStaffOrReadOnly]

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['nombre']
    ordering_fields = ['nombre', 'creado_en']


# -------------------------------
# PROVEEDORES
# -------------------------------
class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    permission_classes = [IsStaffOrReadOnly]

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['nombre', 'email']
    ordering_fields = ['nombre', 'creado_en']


# -------------------------------
# PRODUCTOS
# -------------------------------
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]

    # Filtros
    filterset_fields = {
        'categoria': ['exact'],
        'proveedor': ['exact'],
        'activo': ['exact'],
    }

    # Búsquedas
    search_fields = ['nombre', 'sku', 'descripcion']

    # Ordenamientos
    ordering_fields = ['nombre', 'precio', 'stock_actual', 'creado_en']


# -------------------------------
# MOVIMIENTOS DE STOCK
# -------------------------------
class MovimientoStockViewSet(viewsets.ModelViewSet):
    queryset = MovimientoStock.objects.select_related('producto').all()
    serializer_class = MovimientoStockSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['tipo', 'producto']
    ordering_fields = ['creado_en', 'cantidad']
