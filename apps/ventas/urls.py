#importamos la libreria url para usar la funcion path
from django.urls import path,include
from . import views
from ..loggin import views as view_login
from ..administrador import views as view_admin

urlpatterns = [
    path("", views.index, name='punto_venta'),
    path("iniciar_sesion/", view_login.iniciar_sesion ,name="iniciar_sesion"),
    path("cerrar_sesion/", view_login.cerrar_sesion ,name="cerrar_sesion"),
    path("perfil/", view_login.perfil ,name="perfil"),
    path("administrador/", view_admin.admin ,name="administrador"),
    path("producto_pv/<uuid>", views.producto_pv ,name="producto_pv"),
    path("select_color/", views.select_color ,name="select_color"),
    path("select_tallas/", views.select_tallas ,name="select_tallas"),
    path("select_images/", views.select_images ,name="select_images"),
    path("pruebabi/", views.pruebabi ,name="pruebabi"),
]

