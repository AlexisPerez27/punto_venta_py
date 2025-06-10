#importamos la libreria url para usar la funcion path
from django.urls import path
from . import views
from ..ventas import views as view_ventas
from ..administrador import views as view_admin


urlpatterns = [
    #==================== para sesion
    path("iniciar_sesion/", views.iniciar_sesion, name='inicar_sesion'),
    path("inicio_sesion/", views.inicio_sesion, name='inicio_sesion'),
    path("cerrar_sesion/", views.cerrar_sesion, name='cerrar_sesion'),
    #==================== para registrar usuario
    path("registrar_usuario/", views.registrar_usu, name='registrar_usuario'),
    path("alta_estado_mod/", views.alta_estado_mod, name='alta_estado_mod'),
    path("consulta_estados/", views.consulta_estados, name='consulta_estados'),
    path("alta_municipio_mod/", views.alta_municipio_mod, name='alta_municipio_mod'),
    path("consulta_municipios/", views.consulta_municipios, name='consulta_municipios'),
    path("consulta_cp/", views.consulta_cp, name='consulta_cp'),
    path("alta_usuario/", views.alta_usuario, name='alta_usuario'),
    path("busca_usuario/", views.busca_usuario, name='busca_usuario'),
    path("busca_correo/", views.busca_correo, name='busca_correo'),
    path("", view_ventas.index, name='inicio'),
    #======================= para editar perdil
    path("perfil/", views.perfil, name='perfil'),
    path("editar_perfil/<uuid>", views.editar_perfil, name='editar_perfil'),
    path("alta_estado_mod_editar/", views.alta_estado_mod_editar, name='alta_estado_mod_editar'),
    path("consulta_estados_editar/", views.consulta_estados_editar, name='consulta_estados_editar'),
    path("alta_municipio_mod_editar/", views.alta_municipio_mod_editar, name='alta_municipio_mod_editar'),
    path("consulta_municipios_editar/", views.consulta_municipios_editar, name='consulta_municipios_editar'),
    path("consulta_cp_editar/", views.consulta_cp_editar, name='consulta_cp_editar'),
    path("guarda_editar_perfil/", views.guarda_editar_perfil, name='guarda_editar_perfil'),
    #======================== para editar usuario
    path("editar_usuario/<uuid>", views.editar_usuario, name='editar_usuario'),
    path("busca_usuario_editar/", views.busca_usuario_editar, name='busca_usuario_editar'),
    path("busca_correo_editar/", views.busca_correo_editar, name='busca_correo_editar'),
    path("guarda_edit_usuario/", views.guarda_edit_usuario, name='guarda_edit_usuario'),

    #======================== para solicitar ser administrador
    path("solicita/", view_admin.inicio_admin, name='solicita'),
    
    # ======================== para panel administrador
    path("administrador/", view_admin.admin, name='administrador'),
]