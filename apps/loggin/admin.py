from django.contrib import admin


#importamos modelos
from .models import pais,estados,municipios,usuarios,sesiones,historial_sesiones,permisos,restablecer_contras, datos_api_cp

# agregamos esta linea para anexar el modelo
admin.site.register(pais)
admin.site.register(estados)
admin.site.register(municipios)
admin.site.register(usuarios)
admin.site.register(sesiones)
admin.site.register(historial_sesiones)
admin.site.register(permisos)
admin.site.register(restablecer_contras)
admin.site.register(datos_api_cp)


