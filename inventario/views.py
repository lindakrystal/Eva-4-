from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages

from .models import Categoria, Proveedor, Producto, MovimientoStock
from .serializers import (
    CategoriaSerializer,
    ProveedorSerializer,
    ProductoSerializer,
    MovimientoStockSerializer,
)

# ============================================================
# PERMISO PERSONALIZADO API
# ============================================================
class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_staff


# ============================================================
# API REST (VIEWSETS)
# ============================================================
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsStaffOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['nombre']
    ordering_fields = ['nombre']


class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    permission_classes = [IsStaffOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['nombre', 'email']
    ordering_fields = ['nombre']


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['categoria', 'proveedor']
    search_fields = ['nombre', 'sku']
    ordering_fields = ['nombre', 'precio', 'stock_actual']


class MovimientoStockViewSet(viewsets.ModelViewSet):
    queryset = MovimientoStock.objects.select_related('producto')
    serializer_class = MovimientoStockSerializer
    permission_classes = [permissions.IsAuthenticated]


# ============================================================
# LOGOUT
# ============================================================
def logout_view(request):
    logout(request)
    messages.success(request, "La sesión se ha cerrado correctamente.")
    return redirect('login')


# ============================================================
# DASHBOARD
# ============================================================
@login_required
def inicio_view(request):
    return render(request, 'inicio.html')


# ============================================================
# CRUD CATEGORÍAS
# ============================================================
@login_required
def categorias_list(request):
    categorias = Categoria.objects.all()
    return render(request, 'categorias/list.html', {'categorias': categorias})


@login_required
def categorias_crear(request):
    if request.method == 'POST':
        Categoria.objects.create(
            nombre=request.POST.get('nombre'),
            descripcion=request.POST.get('descripcion', '')
        )
        return redirect('categorias_list')
    return render(request, 'categorias/crear.html')


@login_required
def categorias_editar(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    if request.method == 'POST':
        categoria.nombre = request.POST.get('nombre')
        categoria.descripcion = request.POST.get('descripcion', '')
        categoria.save()
        return redirect('categorias_list')
    return render(request, 'categorias/editar.html', {'categoria': categoria})


@login_required
def categorias_eliminar(request, id):
    get_object_or_404(Categoria, id=id).delete()
    return redirect('categorias_list')


# ============================================================
# CRUD PROVEEDORES
# ============================================================
@login_required
def proveedores_list(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'proveedores/list.html', {'proveedores': proveedores})


@login_required
def proveedores_crear(request):
    if request.method == 'POST':
        Proveedor.objects.create(
            nombre=request.POST.get('nombre'),
            email=request.POST.get('email'),
            telefono=request.POST.get('telefono')
        )
        return redirect('proveedores_list')
    return render(request, 'proveedores/crear.html')


@login_required
def proveedores_editar(request, id):
    proveedor = get_object_or_404(Proveedor, id=id)
    if request.method == 'POST':
        proveedor.nombre = request.POST.get('nombre')
        proveedor.email = request.POST.get('email')
        proveedor.telefono = request.POST.get('telefono')
        proveedor.save()
        return redirect('proveedores_list')
    return render(request, 'proveedores/editar.html', {'proveedor': proveedor})


@login_required
def proveedores_eliminar(request, id):
    get_object_or_404(Proveedor, id=id).delete()
    return redirect('proveedores_list')


# ============================================================
# CRUD PRODUCTOS (🔥 AQUÍ ESTABA EL ERROR)
# ============================================================
@login_required
def productos_list(request):
    productos = Producto.objects.select_related('categoria', 'proveedor')
    return render(request, 'productos/list.html', {'productos': productos})


@login_required
def productos_crear(request):
    categorias = Categoria.objects.all()
    proveedores = Proveedor.objects.all()

    if request.method == 'POST':
        Producto.objects.create(
            nombre=request.POST.get('nombre'),
            sku=request.POST.get('sku'),
            descripcion=request.POST.get('descripcion', ''),
            precio=request.POST.get('precio'),
            stock_actual=request.POST.get('stock_actual'),
            categoria_id=request.POST.get('categoria'),
            proveedor_id=request.POST.get('proveedor'),
        )
        return redirect('productos_list')

    return render(request, 'productos/crear.html', {
        'categorias': categorias,
        'proveedores': proveedores
    })


@login_required
def productos_editar(request, id):
    producto = get_object_or_404(Producto, id=id)
    categorias = Categoria.objects.all()
    proveedores = Proveedor.objects.all()

    if request.method == 'POST':
        producto.nombre = request.POST.get('nombre')
        producto.sku = request.POST.get('sku')
        producto.descripcion = request.POST.get('descripcion', '')
        producto.precio = request.POST.get('precio')
        producto.stock_actual = request.POST.get('stock_actual')
        producto.categoria_id = request.POST.get('categoria')
        producto.proveedor_id = request.POST.get('proveedor')
        producto.save()
        return redirect('productos_list')

    return render(request, 'productos/editar.html', {
        'producto': producto,
        'categorias': categorias,
        'proveedores': proveedores
    })


@login_required
def productos_eliminar(request, id):
    if request.method == 'POST':
        get_object_or_404(Producto, id=id).delete()
    return redirect('productos_list')

# ============================================================
# CRUD MOVIMIENTOS
# ============================================================
@login_required
def movimientos_list(request):
    movimientos = MovimientoStock.objects.select_related('producto')
    return render(request, 'movimientos/list.html', {'movimientos': movimientos})


@login_required
def movimientos_crear(request):
    productos = Producto.objects.all()

    if request.method == 'POST':
        producto = Producto.objects.get(id=request.POST.get('producto'))
        tipo = request.POST.get('tipo')
        cantidad = int(request.POST.get('cantidad'))

        if tipo == 'SALIDA' and cantidad > producto.stock_actual:
            return render(request, 'movimientos/crear.html', {
                'productos': productos,
                'error': 'Stock insuficiente'
            })

        MovimientoStock.objects.create(
            producto=producto,
            tipo=tipo,
            cantidad=cantidad
        )

        producto.stock_actual += cantidad if tipo == 'ENTRADA' else -cantidad
        producto.save()

        return redirect('movimientos_list')

    return render(request, 'movimientos/crear.html', {'productos': productos})


@login_required
def movimientos_eliminar(request, id):
    get_object_or_404(MovimientoStock, id=id).delete()
    return redirect('movimientos_list')
