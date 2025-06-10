#importamos la libreria url para usar la funcion path
from django.urls import path
from . import views


urlpatterns = [    
    #====================== para productos ================================
    path("", views.productos_list, name="productos"),
    path("alta_productos/",views.alta_prod,name="alta_productos"),
    path("carga_modal_seccion/",views.carga_modal_seccion,name="carga_modal_seccion"),
    path("guarda_modal_seccion/",views.guarda_modal_seccion,name="guarda_modal_seccion"),    
    path("consulta_cod_prod/",views.consulta_cod_prod,name="consulta_cod_prod"),
    path("carga_modal_tipo/",views.carga_modal_tipo,name="carga_modal_tipo"),
    path("guarda_modal_tipo/",views.guarda_modal_tipo,name="guarda_modal_tipo"),  
    path("busca_talla/",views.busca_talla,name="busca_talla"),
    path("busca_color/",views.busca_color,name="busca_color"),
    path("busca_talla_mod/",views.busca_talla_mod,name="busca_talla_mod"),
    path("guarda_producto/",views.guarda_prod,name="guarda_producto"),
    path("modifica_producto/<uuid>",views.modifica_producto,name="modifica_producto"),
    path("elimina_img/",views.elimina_img,name="elimina_img"),
    path("guarda_mod_prod/",views.guarda_mod_prod,name="guarda_mod_prod"),
    path("elimina_prod/<id_prod>",views.elimina_prod,name="elimina_prod"),    

    #==================== para tipo producto ==================================
    path("tipo_productos/",views.tipo_prod_list,name="tipo_productos"),
    path("alta_tipo_prod/",views.alta_tipo_prod,name="alta_tipo_prod"),
    path("guarda_tipo_prod/",views.guarda_tipo_prod,name="guarda_tipo_prod"),
    path("modifica_tipo_prod/<uuid>",views.modifica_tipo_prod,name="modifica_tipo_prod"),# para mandar varios parametros es necesrio colocarlos de esta manera "/<talla>/<talla2>" 
    path("guarda_mod_tipo_prod/",views.guarda_mod_tipo_prod,name="guarda_mod_tipo_prod"),
    path("elimina_tipo_prod/<id_tp>",views.elimina_tipo_prod,name="elimina_tipo_prod"),

    #======================== para seccion =======================================
    path("seccion_prod/",views.seccion_prod_list,name="seccion_prod"),
    path("alta_seccion_prod/",views.alta_seccion_prod,name="alta_seccion_prod"),
    path("guarda_seccion_prod/",views.guarda_seccion_prod,name="guarda_seccion_prod"),
    path("modifica_seccion_prod/<uuid>",views.modifica_seccion_prod,name="modifica_seccion_prod"),
    path("guarda_mod_seccion/",views.guarda_mod_seccion,name="guarda_mod_seccion"),
    path("elimina_seccion/<id_sp>",views.elimina_seccion,name="elimina_seccion"),
    
    # ======================================= para inventario ==================================================
    path("seccion_prod/",views.seccion_prod_list,name="seccion_prod"),
]