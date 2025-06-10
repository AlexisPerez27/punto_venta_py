#importamos la libreria url para usar la funcion path
from django.urls import path
from . import views
from ..loggin import views as views_loggin
from ..productos import views as view_prod
from ..ventas import views as views_ventas



urlpatterns = [
    path("solicita/", views.inicio_admin, name="inicio_admin"),
    path("busca_codigo/", views.busca_codigo, name="busca_codigo/"),
    path("busca_correo/", views.busca_correo, name="busca_correo/"),
    path("valida_admin/<uuid>", views.valida_admin, name="valida_admin/"),
    path("actualizar_admin/<uuid>", views.actualizar_admin, name="actualizar_admin/"),
    # ==================== PARA ADMINISTRADOR ==============================================
    path("",views.admin,name="administrador"),

    #================================== para productos ====================================
    path("productos/",view_prod.productos,name="productos/"),
    
    #================================== para productos ====================================
    path("inverntario/",view_prod.inventario_list,name="inverntario/"),

    # ================================ para cerrar sesion =================================
    path("perfil/", views_loggin.perfil, name='perfil'),
    path("cerrar_sesion/", views_loggin.cerrar_sesion, name='cerrar_sesion/'), 
    
    
    #====================== para punto venta ==================================
    path("punto_venta/", views_ventas.index, name="punto_venta"),
]