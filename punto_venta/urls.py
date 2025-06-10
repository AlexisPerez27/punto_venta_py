"""
URL configuration for punto_venta project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from django_postalcodes_mexico import urls as django_postalcodes_mexico_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("administrador/", include('apps.administrador.urls')),
    path("dashboard/", include('apps.administrador.urls')),
    path('',include('apps.ventas.urls')), # definimos la carpeta de las urls de donde se encuentra la aplicacion
    path('loggin/',include('apps.loggin.urls')), # definimos la carpeta de las urls de donde se encuentra la aplicacion
    path('codigos/', include(django_postalcodes_mexico_urls)), # para traer los codigos postales de la api de mexico
    path('productos/',include('apps.productos.urls')), # definimos la carpeta de las urls de donde se encuentra la aplicacion
]+ static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
