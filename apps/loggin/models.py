from django.db import models
import uuid # para referenciar el uuid
from django.utils import timezone # para obtener el tiempo actual


# para guardar imagenes
def imagenes_usuario(instancia, filename):
    return "{0}/{1}".format(instancia.nombre, filename)

# Create your models here.
class pais(models.Model):
    id_pais = models.AutoField(primary_key=True, editable=False)
    uuid_pais = models.UUIDField(default=uuid.uuid4, editable=False)
    pais = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.pais


class estados(models.Model):
    id_estados = models.AutoField(primary_key=True, editable=False)
    uuid_estados = models.UUIDField(default=uuid.uuid4, editable=False)
    estados = models.CharField(max_length=200)
    fk_pais = models.ForeignKey(pais, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fk_pais.pais + ' --- ' + self.estados


class municipios(models.Model):
    id_municipios = models.AutoField(primary_key=True, editable=False)
    uuid_mun = models.UUIDField(default=uuid.uuid4, editable=False)
    municipios = models.CharField(max_length=200)
    fk_estados = models.ForeignKey(estados, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fk_estados.estados + ' --- ' + self.municipios
    


class usuarios(models.Model):
    id_usuarios = models.AutoField(primary_key=True, editable=False)
    uuid_usu = models.UUIDField(default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    fecha_nac = models.DateField()


    #para select en formato admin
    estado_civil_opt = (
        ("soltero", "Soltero"),
        ("casado", "Casado"),
        ("union_libre", "Union Libre"),
        ("viudo", "Viudo(a)"),
        ("sin_espec", "No especificar"),
    )



    #para select en formato de admin
    estado_civil = models.CharField(max_length=20, choices=estado_civil_opt)

    #para radio en formato admin
    sexo_radio = (
        ("M", "Masculino"),
        ("F", "Femenino"),
        ("N", "No Definir"),
    )

    sexo = models.CharField(max_length=1,choices=sexo_radio)
    telefono = models.BigIntegerField()
    foto = models.ImageField(upload_to=imagenes_usuario, blank=True, null=True,)
    fk_municipios = models.BigIntegerField(blank=True,null=True)
    fk_cod_postal = models.BigIntegerField(blank=True,null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre + ' ' + self.apellidos
    


class permisos(models.Model):
    id_permisos = models.AutoField(primary_key=True, editable=False)
    uuid_permisos = models.UUIDField(default=uuid.uuid4, editable=False)
    permisos = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.permisos


class sesiones(models.Model): 
    id_sesion = models.AutoField(primary_key=True, editable=False)
    uuid_sesion = models.UUIDField(default=uuid.uuid4, editable=False)    
    correo = models.EmailField(null=True)
    usuario_sesion = models.CharField(max_length=100)
    contra = models.CharField(max_length=200)
    fk_usuario = models.ForeignKey(usuarios, on_delete=models.CASCADE)
    fk_permisos = models.ForeignKey(permisos, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.usuario_sesion + ' --- ' + self.fk_permisos.permisos
    


class historial_sesiones(models.Model):
    id_historial = models.AutoField(primary_key=True, editable=False)
    uuid_historial = models.UUIDField(default=uuid.uuid4, editable=False)
    fecha = models.DateField()
    direccion_ip = models.GenericIPAddressField()
    nombre_equipo = models.CharField(max_length=200,blank=True,null=True)
    fk_sesion = models.ForeignKey(sesiones, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.direccion_ip + ' ----- ' + str(self.fecha)


class restablecer_contras(models.Model):
    id_restablece = models.AutoField(primary_key=True, editable=False)
    uuid_restablece = models.UUIDField(default=uuid.uuid4, editable=False)
    contra_anterior = models.CharField(max_length=200)
    contra_anterior = models.CharField(max_length=200)
    #para radio en formato admin
    activa_opt = (
        ("SI", "SI"),
        ("NO", "NO"),
    )
    activa = models.CharField(max_length=2,choices=activa_opt)
    bandera = models.IntegerField()
    bandera2 = models.IntegerField()
    fk_sesion = models.ForeignKey(sesiones, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return str(self.id_restablece) + '-----' + self.activa
    

class datos_api_cp(models.Model):
    id_datos_cp = models.AutoField(primary_key=True, editable=False)
    uuid_datos_cp = models.UUIDField(default=uuid.uuid4, editable=False)
    codigo_postal_api = models.BigIntegerField()
    estado_api = models.CharField(max_length=200)
    municipio_api = models.CharField(max_length=200)
    colonia_api = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    fk_cod_postal = models.ForeignKey(usuarios, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.estado_api) + '-----' + self.municipio_api + '-----' + self.colonia_api