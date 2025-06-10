#importamos la libreria url para usar la funcion path
from django.urls import path
from . import views
from ..ventas import views as views_ventas

urlpatterns = [    
    #====================== para productos ================================
    path("", views.productos_list, name="productos"),
    path("registra_producto/", views.registra_producto, name="registra_producto"),
    path("guarda_productos/", views.guarda_productos, name="guarda_productos"),
    path("modifica_productos/<uuid>", views.modifica_productos, name="modifica_productos"),
    path("guarda_mod_det_prod/", views.guarda_mod_det_prod, name="guarda_mod_det_prod"),
    path("elimina_producto/<uuid>", views.elimina_producto, name="elimina_producto"),
    path("consulta_listas/<tipos>/<dato>", views.consulta_listas, name="consulta_listas"),
    path("guarda_lista/", views.guarda_lista, name="guarda_lista"),
    path("modal_tallas/", views.modal_tallas, name="modal_tallas"),
    path("elimina_det_talla/", views.elimina_det_talla, name="elimina_det_talla"),
    path("agrega_mod_tallas/", views.agrega_mod_tallas, name="agrega_mod_tallas"),
    path("modal_imagenes/", views.modal_imagenes, name="modal_imagenes"),    
    path("elimina_images/", views.elimina_images, name="elimina_images"),    
    path("agrega_imagen_modal/", views.agrega_imagen_modal, name="agrega_imagen_modal"),    
    path("elimina_mod_prod/", views.elimina_mod_prod, name="elimina_mod_prod"),    
    #====================== para colores ==================================
    path("colores/", views.colores_list, name="colores"),
    path("registra_color/", views.registra_color, name="registra_color"),
    path("guarda_color/", views.guarda_color, name="guarda_color"),
    path("modifica_color/<uuid>", views.modifica_color, name="modifica_color"),
    path("guarda_mod_color/", views.guarda_mod_color, name="guarda_mod_color"),
    path("elimina_color/<uuid>", views.elimina_color, name="elimina_color"),
        
    #====================== para colores ==================================
    path("tipo/", views.tipo_list, name="tipo"),
    path("registra_tipo/", views.registra_tipo, name="registra_tipo"),
    path("guarda_tipo_vestimenta/", views.guarda_tipo_vestimenta, name="guarda_tipo_vestimenta"),
    path("modifica_tipo_vest/<uuid>", views.modifica_tipo_vest, name="modifica_tipo_vest"),
    path("guarda_mod_tipo_vest/", views.guarda_mod_tipo_vest, name="guarda_mod_tipo_vest"),
    path("elimina_tipo_vest/<uuid>", views.elimina_tipo_vest, name="elimina_tipo_vest"),
    
    
    #====================== para seccion ==================================
    path("seccion/", views.seccion_list, name="seccion"),
    path("registra_seccion/", views.registra_seccion, name="registra_seccion"),
    path("guarda_seccion/", views.guarda_seccion, name="guarda_seccion"),
    path("modifica_seccion/<uuid>", views.modifica_seccion, name="modifica_seccion"),
    path("guarda_mod_seccion/", views.guarda_mod_seccion, name="guarda_mod_seccion"),    
    path("elimina_seccion/<uuid>", views.elimina_seccion, name="elimina_seccion"),
    
    
    #====================== para tallas ==================================
    path("talla/", views.talla_list, name="talla"),
    path("registra_talla/", views.registra_talla, name="registra_talla"),
    path("guarda_talla/", views.guarda_talla, name="guarda_talla"),
    path("modifica_talla/<uuid>", views.modifica_talla, name="modifica_talla"),
    path("guarda_mod_talla/", views.guarda_mod_talla, name="guarda_mod_talla"),
    path("elimina_talla/<uuid>", views.elimina_talla, name="elimina_talla"),
    
    
    #====================== para INVENTARIO ==================================
    path("inventario/", views.inventario_list, name="inventario"),
    path("carga_datos_list/", views.carga_datos_list, name="carga_datos_list"),
    path("guarda_inventario/", views.guarda_inventario, name="guarda_inventario"),
    path("carga_modal_progre/", views.carga_modal_progre, name="carga_modal_progre"),
    
    
    #====================== para punto venta ==================================
    path("punto_venta/", views_ventas.index, name="punto_venta"),
]