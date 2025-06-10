from django.contrib import admin

#importamos modelos
from .models import productos #,galeria_prod,detalle_prod,seccion_prod,tipo_producto

# agregamos esta linea para anexar el modelo
admin.site.register(productos)
# @admin.register(curso)
 