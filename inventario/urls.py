from django.urls import path
from . import views

urlpatterns = [
    path('categorias/', views.categorias_list, name='categorias_list'),
    path('categorias/nueva/', views.categoria_create, name='categoria_create'),
    path('categorias/editar/<int:id>/', views.categoria_edit, name='categoria_edit'),
    path('categorias/eliminar/<int:id>/', views.categoria_delete, name='categoria_delete'),
]
