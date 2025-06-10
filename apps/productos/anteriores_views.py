from django.shortcuts import render,redirect,get_object_or_404 #importamos funciones de operacion para django
from django.http import HttpResponse, JsonResponse #para mostrar mensajes o resultados en la pagina
from .models import productos #, tipo_producto, seccion_prod, galeria_prod, detalle_prod
from ..loggin import models as model_loggin
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
#para correo
from django.core.mail import EmailMessage, EmailMultiAlternatives 
from django.template.loader import render_to_string
from django.conf import settings

import random,string
from django.db.models import Count


# ========================================= PRODUCTOS ===============================================================
# Create your views here.
def productos_list(request):
    # return HttpResponse("pagina de productos")
    #consultamos las sesion dependiendo del usuario
    ses = model_loggin.sesiones.objects.filter(usuario_sesion = request.session['usu_usuario'])
    #obtenemos el registro de la tabla sesion
    sesion = ses.get()

    #consultamos todos los productos
    # con_prods = productos.objects.all()
    con_prods = detalle_prod.objects.raw("""SELECT * 
    FROM productos_detalle_prod AS dp
    INNER JOIN productos_productos AS p ON p.id_producto = dp.fk_productos_id
    INNER JOIN productos_seccion_prod AS s ON s.id_seccion = dp.fk_seccion_id
    INNER JOIN productos_tipo_producto AS t ON t.id_tipo_prod = dp.fk_tipo_id
    GROUP BY dp.fk_productos_id
    ORDER BY dp.fk_productos_id""")

    #retornamos a vista
    return render(request,"catalogos/productos/productos.html",{'productos':con_prods, 'sesion':sesion})


def alta_prod(request):

    while True:
        # Generar el código con la estructura especificada
        codigo = (
            random.choice(string.digits) + random.choice(string.digits) +  # 2 números
            random.choice(string.ascii_uppercase) + random.choice(string.ascii_uppercase) +  # 2 letras
            random.choice(string.digits) + random.choice(string.ascii_uppercase) +  # 1 número, 1 letra
            random.choice(string.digits) + random.choice(string.ascii_uppercase)  # 1 número, 1 letra
            # random.choice(string.digits)  # 1 número
        )

        #consultamos que el codigo no se encuentre ya registrado
        c_cod_producto = productos.objects.filter(codigo = codigo)

        #contamos cuantos registros tiene la consulta
        count_cod = c_cod_producto.count()

        #si el count es igual a 0 entra aqui 
        if count_cod == 0:
            
            #hacemos una consulta a la tabla de seccion
            seccion = seccion_prod.objects.all()


            #hacemos una consulta a la tabla de tipo pero agrupamos el registro con la funcion annotate y contamos la cantidad de tipo
            #solo asi sirve la agrupa cion e importamos de models la funcion count
            tipo = tipo_producto.objects.values('tipo').annotate(cantidad=Count('tipo')).order_by('tipo')

            #retornamos la vista a visualizar con los datos que queremos mandar tambien rompe el ciclo while
            return render(request,"catalogos/productos/alta_productos.html",{"seccion":seccion,'codigo':codigo,"tipo":tipo})





def carga_modal_seccion(request):
    return render(request,'catalogos/productos/modal_seccion.html')


def guarda_modal_seccion(request):
    m_seccion = request.POST['seccion_prod']

    gsm = seccion_prod.objects.create(
        seccion = m_seccion,
        bandera = 0
    )

    c_seccion = seccion_prod.objects.all()

    return render(request,'catalogos/productos/con_seccion.html',{"res_seccion":c_seccion})



def carga_modal_tipo(request):
    return render(request,'catalogos/productos/modal_tipo.html')


def guarda_modal_tipo(request):
    tipo_p = request.POST['tipo_prod']
    talla = request.POST.getlist('talla')
    color = request.POST['color']
    cod_color = request.POST['cod_color']
    
    if request.POST:
        for t in talla:
            gtp = tipo_producto.objects.create(
                tipo = tipo_p,
                talla = t,
                color = color,
                codigo_color = cod_color
            )

    c_tipo = tipo_producto.objects.values('tipo').annotate(cantidad=Count('tipo')).order_by('tipo')

    return render(request,'catalogos/productos/con_tipo.html',{"res_tipo":c_tipo})


def consulta_cod_prod(request):

    while True:
        # Generar el código con la estructura especificada
        codigo = (
            random.choice(string.digits) + random.choice(string.digits) +  # 2 números
            random.choice(string.ascii_uppercase) + random.choice(string.ascii_uppercase) +  # 2 letras
            random.choice(string.digits) + random.choice(string.ascii_uppercase) +  # 1 número, 1 letra
            random.choice(string.digits) + random.choice(string.ascii_uppercase)  # 1 número, 1 letra
            # random.choice(string.digits)  # 1 número
        )

        c_cod_producto = productos.objects.filter(codigo = codigo)

        count_cod = c_cod_producto.count()

        if count_cod == 0:

            # Generar y mostrar el código
            return codigo



def busca_color(request):
    tipo_p = request.POST['tipo']
    # talla_p = request.POST['talla']

    # color = tipo_producto.objects.filter(tipo = tipo_p,talla = talla_p)
    color = tipo_producto.objects.filter(tipo = tipo_p).values('color').annotate(cantidad=Count('color')).order_by('color')
    # talla = talla.get()

    return render(request,"catalogos/productos/color.html",{"color":color})


def busca_talla(request):
    tipo_p = request.POST['tipo']
    color_p = request.POST['color']

    # talla = tipo_producto.objects.filter(tipo = tipo_p).values('talla').annotate(cantidad=Count('talla')).order_by('talla')
    talla = tipo_producto.objects.filter(tipo = tipo_p,color = color_p)
    # talla = talla.get()

    return render(request,"catalogos/productos/talla.html",{"talla":talla})




def busca_talla_mod(request):
    tipo_p = request.POST['tipo']
    color_p = request.POST['color']

    # talla = tipo_producto.objects.filter(tipo = tipo_p).values('talla').annotate(cantidad=Count('talla')).order_by('talla')
    talla = tipo_producto.objects.filter(tipo = tipo_p,color = color_p)
    # talla = talla.get()

    return render(request,"catalogos/productos/talla_mod.html",{"talla":talla})


def guarda_prod(request):

    #para insertar el producto
    nombre_prod = request.POST['nombre']
    descrip = request.POST['descripcion']
    precio = request.POST['precio']
    cod_producto = request.POST['cod_producto']

    
    prod = productos.objects.create(
        nombre = nombre_prod,
        descripcion = descrip,
        precio = precio,
        bandera = 0,
        codigo = cod_producto
    )


    #consultamos el maximo id productos
    p = productos.objects.all().order_by('-id_producto')[:1] #hacemos un top a la consulta :1, junto con un order by descendente -id_producto
    p = p.get()

    id_prod = p.id_producto

    #para insertar la galeria de productos con un file multiple
    if request.FILES:
        for f in request.FILES.getlist('images'):
            obj = galeria_prod.objects.create(imagenes=f,fk_productos_id = id_prod)

    # para insertar en el detalle del producto
    id_seccion = request.POST['seccion_prod']
    talla = request.POST.getlist('talla')

    if request.POST:
        for t in talla:
            det_prod = detalle_prod.objects.create(
                cantidad = 0,
                stock = 0,
                almacen = 0,
                fk_productos_id = id_prod,
                fk_seccion_id = id_seccion,
                fk_tipo_id = t
            )

   

    messages.error(request,'Alta de producto existosa')

    return redirect('productos')



def elimina_img(request):
    id_img = request.POST['id_img']
    id_prod = request.POST['id_prod']
    uuid_prod = request.POST['uuid_prod']
    
    
    img = galeria_prod.objects.get(id_galeria=id_img)
    img.delete()    
    
    con_galeria = galeria_prod.objects.filter(fk_productos_id=id_prod)
    
    return render(request,"catalogos/productos/con_galeria.html",{"images":con_galeria})
    


def modifica_producto(request,uuid):
    #consultamos el productopor uuid
    con_prods = detalle_prod.objects.raw("""SELECT * 
    FROM productos_detalle_prod AS dp
    INNER JOIN productos_productos AS p ON p.id_producto = dp.fk_productos_id
    INNER JOIN productos_seccion_prod AS s ON s.id_seccion = dp.fk_seccion_id
    INNER JOIN productos_tipo_producto AS t ON t.id_tipo_prod = dp.fk_tipo_id
    WHERE dp.uuid_det_prod = %s""",[uuid])
    
    
    #consulta seccion
    seccion = seccion_prod.objects.all()
    
    for c in con_prods:
        id_prod = c.id_producto
        tipo_cp = c.tipo
        talla_cp = c.talla
        color_cp = c.color
    
    #consulta tipo
    tipo = tipo_producto.objects.all().values('tipo').annotate(cantidad=Count('tipo')).order_by('tipo')
    
    
    #consulta color
    color = tipo_producto.objects.filter(tipo = tipo_cp).values('color').annotate(cantidad=Count('color')).order_by('color')
    
    #consulta talla 
    talla = tipo_producto.objects.filter(tipo = tipo_cp,color = color_cp)
    
    
    #consulta imagenes
    images = galeria_prod.objects.filter(fk_productos_id = id_prod)
    
    
    
    return render(request,"catalogos/productos/modifica_productos.html",{"producto":con_prods,"seccion":seccion,"tipo":tipo,"talla":talla,"color":color,"images":images})



def guarda_mod_prod(request):
    if request.POST:
        id_det_prod = request.POST['id_det_prod']
        id_pro = request.POST['id_prod']
        uuid_producto = request.POST['uuid_prod']
        cod_producto = request.POST['cod_producto']
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        precio = request.POST['precio']
        id_seccion_prod = request.POST['seccion_prod']        
        id_tipo_prod = request.POST['talla']
        
        #para insertar la galeria de productos con un file multiple
        if request.FILES:
            for f in request.FILES.getlist('images'):
                obj = galeria_prod.objects.create(imagenes=f,fk_productos_id = id_pro)
                
        
        #para actualizar producto
        prod = productos.objects.get(id_producto = id_pro)
        
        # prod = prod.get()
    

        prod.nombre = nombre
        prod.descripcion = descripcion
        prod.precio = precio
        prod.save()
        
        det_prod = detalle_prod.objects.get(id_det_prod = id_det_prod)
        
        det_prod.fk_seccion_id = id_seccion_prod
        det_prod.fk_tipo_id = id_tipo_prod
        det_prod.save()
        
        
        messages.error(request,'Modificacion de producto existosa')

        return redirect('productos')
        
    else:
        
        messages.error(request,'No se hizo nunguna modificacion de producto')

        return redirect('productos')
    
    
    

def elimina_prod(request,id_prod):
    
    prod = productos.objects.get(id_producto = id_prod)
    
    prod.delete()
    
    messages.error(request,'Eliminacion de producto existosa')

    return redirect('productos')


# ========================================= TIPO PRODUCTOS ===============================================================
def tipo_prod_list(request):
    lista_tipo_prod = tipo_producto.objects.all()
    return render(request,"catalogos/tipo_prod/tipo_prod.html",{'tipo_prod':lista_tipo_prod})



def alta_tipo_prod(request):
    return render(request,"catalogos/tipo_prod/alta_tipo_prod.html")


def guarda_tipo_prod(request):
    tipo_p = request.POST['tipo_prod']
    talla = request.POST.getlist('talla')
    color = request.POST['color']
    cod_color = request.POST['cod_color']
    
    if request.POST:
        for t in talla:
            gtp = tipo_producto.objects.create(
                tipo = tipo_p,
                talla = t,
                color = color,
                codigo_color = cod_color
            )
        
    messages.error(request,'Alta de tipo producto existoso')


    return redirect('tipo_productos')


def modifica_tipo_prod(request,uuid):
    mtp = tipo_producto.objects.filter(uuid_tipo_prod = uuid)
    mtp = mtp.get()

    return render(request, "catalogos/tipo_prod/modifica_tipo_prod.html", {'mod_tipo_prod':mtp})



def guarda_mod_tipo_prod(request):

    id_tp = request.POST['id_tipo_prod']
    uuid_tp = request.POST['uuid_tipo_prod']
    tipo_tp = request.POST['tipo_prod']
    talla_tp = request.POST['talla']
    color_tp = request.POST['color']
    cod_color_tp = request.POST['cod_color']

    tp = tipo_producto.objects.get(id_tipo_prod = id_tp)

    tp.tipo = tipo_tp
    tp.talla = talla_tp
    tp.color = color_tp
    tp.codigo_color = cod_color_tp
    tp.save()


    messages.error(request,'Modificacion de tipo producto existoso')


    return redirect('tipo_productos')


def elimina_tipo_prod(request,id_tp):
    
    tp = tipo_producto.objects.get(id_tipo_prod=id_tp)
    tp.delete()

    messages.error(request,'Eliminacion de tipo producto existoso')

    return redirect('tipo_productos')



# ========================================= SECCION  PRODUCTOS ===============================================================
def seccion_prod_list(request):
    lista_seccion = seccion_prod.objects.all()
    return render(request,"catalogos/seccion/seccion_prod.html",{'seccion_prod':lista_seccion})



def alta_seccion_prod(request):
    return render(request,"catalogos/seccion/alta_seccion_prod.html")


def guarda_seccion_prod(request):
    seccion_p = request.POST['seccion_prod']

    gsp = seccion_prod.objects.create(
        seccion = seccion_p,
        bandera = 0
    )

    messages.error(request,'Alta de seccion producto existoso')


    return redirect('seccion_prod')


def modifica_seccion_prod(request,uuid):
    msp = seccion_prod.objects.filter(uuid_seccion = uuid)
    msp = msp.get()

    return render(request, "catalogos/seccion/modifica_seccion.html", {'msp':msp})



def guarda_mod_seccion(request):

    id_seccion = request.POST['id_seccion_prod']
    uuid_seccion = request.POST['uuid_seccion_prod']
    seccion = request.POST['seccion_prod']

    sp = seccion_prod.objects.get(id_seccion = id_seccion)

    sp.seccion = seccion
    sp.save()

    messages.error(request,'Modificacion de seccion producto existoso')

    return redirect('seccion_prod')



def elimina_seccion(request,id_sp):
    
    sp = seccion_prod.objects.get(id_seccion=id_sp)
    sp.delete()

    messages.error(request,'Eliminacion de seccion producto existoso')

    return redirect('seccion_prod')




# ======================================================================= INVENTARIO =============================================================================
