from django.shortcuts import render,get_object_or_404 #importamos funciones de operacion para django
from django.http import HttpResponse, JsonResponse #para mostrar mensajes o resultados en la pagina
from ..productos import models as models_productos
from django.db.models import Count

# Create your views here.
def index(request):
    # hacemos una consulta con un JOIN
    prod = models_productos.productos.objects.raw(""" SELECT *
    FROM productos_productos AS p
    INNER JOIN productos_galeria_prod AS g ON g.fk_productos_id = p.id_producto
    GROUP BY p.codigo
    ORDER BY p.id_producto """)
            
    return render(request,"index.html",{"prod":prod}) 



def producto_pv(request,uuid): 
    
    # prod = models_productos.productos.objects.get(uuid_producto = uuid)
    det_prod = models_productos.detalle_prod.objects.filter(fk_productos__uuid_producto=uuid).order_by('-fk_productos__id_producto')
    prod = det_prod.first()
    
    id_prod = prod.fk_productos
    id_color = prod.fk_color    
    
    color = det_prod.values("fk_color__color","fk_color__cod_color","fk_color__id_color").annotate(count=Count("fk_color_id")).order_by('fk_color_id') 

    tallas = det_prod.filter(fk_color_id = id_color).annotate(count=Count("fk_talla_id")).order_by('fk_talla_id') 
    
    inven_tallas = []
    
    for t in tallas:
        id_det_tallas = t.id_detalle
        
        inv_tallas = models_productos.inventario.objects.filter(fk_det_productos_id = id_det_tallas)
        inv_tallas = inv_tallas.get()
        
        count_tallas = inv_tallas.cantidad
        id_inv_tallas = inv_tallas.fk_det_productos_id
        
        inven_tallas.append({"id_inv_tallas":id_inv_tallas,"count_tallas":count_tallas})
    
    img = models_productos.galeria_prod.objects.filter(fk_productos_id = id_prod, fk_color_id = id_color)  
    
    min_id_img = img.first()
    min_id_img = min_id_img.id_galeria
    
    max_id_img = img.last()
    max_id_img = max_id_img.id_galeria

    return render(request,"producto/producto_venta.html",{"prod":prod,"img":img,"color":color,"tallas":tallas,"inv_tallas":inven_tallas,"min_id_img":min_id_img,"max_id_img":max_id_img})



def select_color(request):
    id_prod = request.POST['id_producto']
    id_color = request.POST['id_color'] 
    
    
    det_prod = models_productos.detalle_prod.objects.filter(fk_productos_id=id_prod, fk_color_id = id_color).order_by('-fk_productos__id_producto')
    prod = det_prod.first()  
    
    color = models_productos.detalle_prod.objects.filter(fk_productos_id = id_prod).values("fk_color__color","fk_color__cod_color","fk_color__id_color").annotate(count=Count("fk_color_id")).order_by('fk_color_id') 
    
    
    
        
    return render(request,"producto/paleta_colores.html",{"prod":prod,"color":color})


def select_tallas(request):
    
    id_prod = request.POST['id_producto']
    id_color = request.POST['id_color'] 
    
    
    det_prod = models_productos.detalle_prod.objects.filter(fk_productos_id=id_prod, fk_color_id = id_color).order_by('-fk_productos__id_producto')
    prod = det_prod.first()
    
    tallas = det_prod.filter(fk_color_id = id_color).annotate(count=Count("fk_talla_id")).order_by('fk_talla_id') 
    
    inven_tallas = []
    
    for t in tallas:
        id_det_tallas = t.id_detalle
        
        inv_tallas = models_productos.inventario.objects.filter(fk_det_productos_id = id_det_tallas)
        inv_tallas = inv_tallas.get()
        
        count_tallas = inv_tallas.cantidad
        id_inv_tallas = inv_tallas.fk_det_productos_id
        
        inven_tallas.append({"id_inv_tallas":id_inv_tallas,"count_tallas":count_tallas})
        
    return render(request,"producto/paleta_tallas.html",{"tallas":tallas,"inv_tallas":inven_tallas})


def select_images(request):
    id_prod = request.POST['id_producto']
    id_color = request.POST['id_color'] 
    
    img = models_productos.galeria_prod.objects.filter(fk_productos_id = id_prod, fk_color_id = id_color) 
    
    min_id_img = img.first()
    min_id_img = min_id_img.id_galeria
    
    max_id_img = img.last()
    max_id_img = max_id_img.id_galeria    
    
    return render(request,"producto/paleta_images.html",{"img":img,"min_id_img":min_id_img,"max_id_img":max_id_img})