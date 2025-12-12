from django.urls import path
from . import views

urlpatterns = [
    # CATEGORÍAS
    path('categorias/', views.categorias_list, name='categorias_list'),
    path('categorias/crear/', views.categorias_crear, name='categorias_crear'),
    path('categorias/editar/<int:id>/', views.categorias_editar, name='categorias_editar'),
    path('categorias/eliminar/<int:id>/', views.categorias_eliminar, name='categorias_eliminar'),

    # PROVEEDORES
    path('proveedores/', views.proveedores_list, name='proveedores_list'),
    path('proveedores/crear/', views.proveedores_crear, name='proveedores_crear'),
    path('proveedores/editar/<int:id>/', views.proveedores_editar, name='proveedores_editar'),
    path('proveedores/eliminar/<int:id>/', views.proveedores_eliminar, name='proveedores_eliminar'),

    # PRODUCTOS
    path('productos/', views.productos_list, name='productos_list'),
    path('productos/crear/', views.productos_crear, name='productos_crear'),
    path('productos/editar/<int:id>/', views.productos_editar, name='productos_editar'),
    path('productos/eliminar/<int:id>/', views.productos_eliminar, name='productos_eliminar'),

    # MOVIMIENTOS
    path('movimientos/', views.movimientos_list, name='movimientos_list'),
    path('movimientos/crear/', views.movimientos_crear, name='movimientos_crear'),
    path('movimientos/eliminar/<int:id>/', views.movimientos_eliminar, name='movimientos_eliminar'),
]
