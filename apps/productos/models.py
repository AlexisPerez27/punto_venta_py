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
    codigo = models.CharField(max_length=8,blank=True,null=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10,decimal_places=2, null=True,blank=True)
    bandera = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    #esto se coloca para cuando creemos usuario de superadmin y se visualice en ese apartado
    def __str__(self):
        return str(self.nombre) + '-----' + self.precio
    
    
class color(models.Model):
    id_color = models.AutoField(primary_key=True, editable=False)
    uuid_color = models.UUIDField(default=uuid.uuid4, editable=False)
    color = models.CharField(max_length=50,blank=True, null=True,)
    cod_color = models.CharField(max_length=10, blank=True, null=True,)
    bandera = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)  
        
    

class galeria_prod(models.Model):
    id_galeria = models.AutoField(primary_key=True, editable=False)
    uuid_galeria = models.UUIDField(default=uuid.uuid4, editable=False)
    imagenes = models.ImageField(upload_to=galeria_prod, blank=True, null=True,)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    fk_productos = models.ForeignKey(productos, on_delete=models.CASCADE)
    fk_color = models.ForeignKey(color, on_delete=models.CASCADE)




    
class tipo(models.Model):
    id_tipo = models.AutoField(primary_key=True, editable=False)
    uuid_tipo = models.UUIDField(default=uuid.uuid4, editable=False)
    tipo = models.CharField(max_length=50,blank=True, null=True,)
    bandera = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    

class seccion(models.Model):
    id_seccion = models.AutoField(primary_key=True, editable=False)
    uuid_seccion = models.UUIDField(default=uuid.uuid4, editable=False)
    seccion = models.CharField(max_length=50,blank=True, null=True,)
    bandera = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    

class tallas(models.Model):
    id_tallas = models.AutoField(primary_key=True, editable=False)
    uuid_tallas = models.UUIDField(default=uuid.uuid4, editable=False)
    talla = models.CharField(max_length=50,blank=True, null=True,)
    cod_talla = models.CharField(max_length=50,blank=True, null=True,)
    bandera = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    

class detalle_prod(models.Model):
    id_detalle = models.AutoField(primary_key=True, editable=False)
    uuid_detalle = models.UUIDField(default=uuid.uuid4, editable=False)
    fk_productos = models.ForeignKey(productos, on_delete=models.CASCADE)
    fk_color = models.ForeignKey(color, on_delete=models.CASCADE)
    fk_tipo = models.ForeignKey(tipo, on_delete=models.CASCADE)
    fk_talla = models.ForeignKey(tallas, on_delete=models.CASCADE)
    fk_seccion = models.ForeignKey(seccion, on_delete=models.CASCADE, default=1)
    bandera = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    


    
class  inventario(models.Model):
    id_inventario = models.AutoField(primary_key=True, editable=False)
    uuid_inventario = models.UUIDField(default=uuid.uuid4, editable=False)
    fk_det_productos = models.ForeignKey(detalle_prod, on_delete=models.CASCADE)
    stock = models.BigIntegerField()
    cantidad = models.BigIntegerField()
    almacen = models.IntegerField()
    bandera = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)