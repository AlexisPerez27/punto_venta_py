from django.db import models
import uuid # para referenciar el uuid
from django.utils import timezone # para obtener el tiempo actual



class codigos(models.Model):
    id_codigo = models.AutoField(primary_key=True, editable=False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    codigo = models.CharField(max_length=100)
    activo = models.IntegerField(blank=True,null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)