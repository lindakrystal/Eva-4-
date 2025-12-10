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


# ============================================================
# PERMISOS PERSONALIZADOS
# ============================================================
class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Lectura para cualquier usuario autenticado.
    Escritura solo para usuarios staff.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_staff


# ============================================================
# API REST: VIEWSETS
# ============================================================

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsStaffOrReadOnly]

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['nombre']
    ordering_fields = ['nombre', 'creado_en']


class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    permission_classes = [IsStaffOrReadOnly]

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['nombre', 'email']
    ordering_fields = ['nombre', 'creado_en']


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]

    filterset_fields = {
        'categoria': ['exact'],
        'proveedor': ['exact'],
        'activo': ['exact'],
    }

    search_fields = ['nombre', 'sku', 'descripcion']
    ordering_fields = ['nombre', 'precio', 'stock_actual', 'creado_en']


class MovimientoStockViewSet(viewsets.ModelViewSet):
    queryset = MovimientoStock.objects.select_related('producto').all()
    serializer_class = MovimientoStockSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['tipo', 'producto']
    ordering_fields = ['creado_en', 'cantidad']


# ============================================================
# VISTA HTML PRINCIPAL (Dashboard)
# ============================================================
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required


@login_required
def inicio_view(request):
    """Vista principal del sistema."""
    return render(request, 'inicio.html')


# ============================================================
# CRUD HTML - CATEGORÍAS
# ============================================================

@login_required
def categorias_list(request):
    categorias = Categoria.objects.all()
    return render(request, 'categorias/list.html', {'categorias': categorias})


@login_required
def categoria_create(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')

        if nombre:
            Categoria.objects.create(nombre=nombre, descripcion=descripcion)
            return redirect('categorias_list')

    return render(request, 'categorias/create.html')


@login_required
def categoria_edit(request, id):
    categoria = get_object_or_404(Categoria, id=id)

    if request.method == 'POST':
        categoria.nombre = request.POST.get('nombre')
        categoria.descripcion = request.POST.get('descripcion')
        categoria.save()
        return redirect('categorias_list')

    return render(request, 'categorias/edit.html', {'categoria': categoria})


@login_required
def categoria_delete(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    categoria.delete()
    return redirect('categorias_list')
