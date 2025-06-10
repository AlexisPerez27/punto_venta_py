from django.db import models
import uuid # para referenciar el uuid
from django.utils import timezone # para obtener el tiempo actual


# para guardar imagenes
def galeria_prod(instancia, filename):
    return "productos/{0}/{1}".format(instancia.imagenes, filename)

# Create your models here.
class productos(models.Model):
    id_producto = models.AutoField(primary_key=True, editable=False)
    uuid_producto = models.UUIDField(default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10,decimal_places=2, null=True,blank=True)
    bandera = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    codigo = models.CharField(max_length=8,blank=True,null=True)

    #esto se coloca para cuando creemos usuario de superadmin y se visualice en ese apartado
    def __str__(self):
        return str(self.nombre) + '-----' + self.precio
    

class galeria_prod(models.Model):
    id_galeria = models.AutoField(primary_key=True, editable=False)
    uuid_galeria = models.UUIDField(default=uuid.uuid4, editable=False)
    imagenes = models.ImageField(upload_to=galeria_prod, blank=True, null=True,)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    fk_productos = models.ForeignKey(productos, on_delete=models.CASCADE)


class tipo_producto(models.Model):
    id_tipo_prod = models.AutoField(primary_key=True, editable=False)
    uuid_tipo_prod = models.UUIDField(default=uuid.uuid4, editable=False)
    tipo = models.CharField(max_length=50,blank=True,null=True)
    talla = models.CharField(max_length=50,blank=True,null=True)
    color = models.CharField(max_length=50,blank=True,null=True)
    codigo_color = models.CharField(max_length=10,blank=True,null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.tipo) + '-----' + self.talla


class seccion_prod(models.Model):
    id_seccion = models.AutoField(primary_key=True, editable=False)
    uuid_seccion = models.UUIDField(default=uuid.uuid4, editable=False)
    seccion = models.CharField(max_length=50)
    bandera = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
            return str(self.seccion)
    



class detalle_prod(models.Model):
    id_det_prod = models.AutoField(primary_key=True, editable=False)
    uuid_det_prod = models.UUIDField(default=uuid.uuid4, editable=False)
    cantidad = models.IntegerField()
    stock = models.BigIntegerField()
    almacen = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    fk_productos = models.ForeignKey(productos, on_delete=models.CASCADE)
    fk_seccion = models.ForeignKey(seccion_prod, on_delete=models.CASCADE)
    fk_tipo = models.ForeignKey(tipo_producto, on_delete=models.CASCADE)


    def __str__(self):
            return str(self.fk_productos.nombre) + '-----' + self.cantidad