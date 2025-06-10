from django.shortcuts import render,redirect,get_object_or_404 #importamos funciones de operacion para django
from django.http import HttpResponse, JsonResponse #para mostrar mensajes o resultados en la pagina
from .models import productos, color, tipo, seccion, tallas, galeria_prod, detalle_prod,inventario
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
    con_prods = productos.objects.all()

    #retornamos a vista
    return render(request,"catalogos/productos/productos.html",{'productos':con_prods, 'sesion':sesion})



def registra_producto(request):
    
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
            _seccion = seccion.objects.all()
            
            #hacemos una consulta a la tabla de tipo pero agrupamos el registro con la funcion annotate y contamos la cantidad de tipo
            #solo asi sirve la agrupa cion e importamos de models la funcion count
            # tipo = tipo_producto.objects.values('tipo').annotate(cantidad=Count('tipo')).order_by('tipo')
            
            #hacemos consulta d tipo producto 
            _tipo = tipo.objects.all()
            
            #hacemos consulta de colores
            _color = color.objects.all()
            
            #hacemos consulta de tallas
            _tallas = tallas.objects.all()

            #retornamos la vista a visualizar con los datos que queremos mandar tambien rompe el ciclo while
            # return render(request,"catalogos/productos/alta_productos.html",{"seccion":seccion,'codigo':codigo,"tipo":tipo})

            return render(request,"catalogos/productos/registra_productos.html",{"cod":codigo,"seccion":_seccion,"tipo": _tipo,"color":_color,"tallas":_tallas})
        
        
def guarda_productos(request):
    cod_prod = request.POST['cod_prod']
    nom_producto = request.POST['producto']
    descripcion = request.POST['descripcion']
    precio = request.POST['precio']
    id_seccion = request.POST['id_seccion']
    seccion = request.POST['seccion']
    id_tipo = request.POST['id_tipo']
    tipo = request.POST['tipo']
    id_color = request.POST['id_color']
    color = request.POST['color']
    id_tallas = request.POST['id_tallas']
    tallas = request.POST['tallas']
    # images = request.FILES.getlist('images')
    
    
    p = productos.objects.filter(codigo = cod_prod,nombre = nom_producto)
    count_prod = p.count()
    
    if count_prod == 0:
    
        #para insertar productos
        prod = productos.objects.create(
            codigo = cod_prod,
            nombre = nom_producto,
            descripcion = descripcion, 
            precio = precio,
            bandera = 0
        )
    
    
    
    
    pro = productos.objects.all().order_by('-id_producto')[:1]
    pro = pro.get()
    
    id_prod = pro.id_producto
    
    #para insertar la galeria de productos con un file multiple
    if request.FILES:
        files = request.FILES.getlist('images')  # Nombre del campo de los archivos

        if files:
            # Aquí puedes procesar los archivos
            # Por ejemplo, guardarlos o hacer algo con ellos
            for file in files:
                # print(file.name)  # Imprimir el nombre de cada archivo
                obj = galeria_prod.objects.create(imagenes=file,fk_color_id = id_color,fk_productos_id = id_prod)

            # return JsonResponse({'message': 'Archivos recibidos correctamente'}, status=200)
            print('Archivos recibidos correctamente')

        else:
            # return JsonResponse({'message': 'No se han enviado archivos'}, status=400)
            print('No se han enviado archivos')


    tallas_array = id_tallas.split(",") #es para dividir una cadena y comvertirla en arreglo
    
    for t in tallas_array:
        
        _det = detalle_prod.objects.filter(fk_color_id = id_color,
        fk_productos_id = id_prod,
        fk_talla_id = t,
        fk_tipo_id = id_tipo,
        fk_seccion_id = id_seccion)
        
        count_det = _det.count()
        
        # print(count_det)
        
        if count_det == 0:
        
            det_pr = detalle_prod.objects.create(
                bandera = 0,
                fk_color_id = id_color,
                fk_productos_id = id_prod,
                fk_talla_id = t,
                fk_tipo_id = id_tipo,
                fk_seccion_id = id_seccion
            )


    return HttpResponse("%s"%tallas_array)



def elimina_producto(request,uuid):
    prod = productos.objects.get(uuid_producto = uuid)
    
    prod.delete()
    
    return redirect('productos')


# ============================================================= PARA MODIFICACION DE PRODUCTOS ===================================================================
def modifica_productos(request,uuid): 
    prod = productos.objects.get(uuid_producto = uuid)
    det_prod = detalle_prod.objects.raw("""SELECT * 
    FROM productos_detalle_prod AS dp 
    INNER JOIN productos_productos AS p ON p.id_producto = dp.fk_productos_id
    INNER JOIN productos_color AS c ON c.id_color = dp.fk_color_id
    INNER JOIN productos_tallas AS t ON t.id_tallas = dp.fk_talla_id
    INNER JOIN productos_tipo AS tp ON tp.id_tipo = dp.fk_tipo_id
    INNER JOIN productos_seccion AS s ON s.id_seccion = dp.fk_seccion_id
    WHERE p.uuid_producto = %s
    GROUP BY c.color""",[uuid])
    
    ta = tallas.objects.all()
    
    #hacemos una consulta a la tabla de seccion
    _seccion = seccion.objects.all()
    
    #hacemos consulta d tipo producto 
    _tipo = tipo.objects.all()
    
    #hacemos consulta de colores
    _color = color.objects.all()
    

    return render(request,"catalogos/productos/modifica_productos.html",{"prod":prod, "det_prod":det_prod,"tallas":ta,"seccion":_seccion,"tipo": _tipo,"color":_color})


def guarda_mod_det_prod(request):
    
    id_prod = request.POST['id_prod']
    tipo_opcion = request.POST['tipo_opcion']
    
    
    if tipo_opcion == '1':
        nombre = request.POST['nom_prod']
        descripcion = request.POST['descripcion']
        precio = request.POST['precio']
        
        _prod = productos.objects.get(id_producto = id_prod)
        
        _prod.nombre = nombre
        _prod.descripcion = descripcion
        _prod.precio = precio
        _prod.save()
        
        return HttpResponse("Se guardo correctamente la modificacion del producto")
    
    elif tipo_opcion == '2':
        
        id_seccion = request.POST['id_seccion']    
        id_tipo = request.POST['id_tipo']    
        id_color = request.POST['id_color']  
        id_tallas = request.POST['id_tallas']
        
        tallas_array = id_tallas.split(",") #es para dividir una cadena y comvertirla en arreglo
        
        for t in tallas_array:
            
            _det = detalle_prod.objects.filter(fk_color_id = id_color,
            fk_productos_id = id_prod,
            fk_talla_id = t,
            fk_tipo_id = id_tipo,
            fk_seccion_id = id_seccion)
            
            count_det = _det.count()
            
            # print(count_det)
            
            if count_det == 0:
            
                det_pr = detalle_prod.objects.create(
                    bandera = 0,
                    fk_color_id = id_color,
                    fk_productos_id = id_prod,
                    fk_talla_id = t,
                    fk_tipo_id = id_tipo,
                    fk_seccion_id = id_seccion
                )
                
                
        #para insertar la galeria de productos con un file multiple
        if request.FILES:
            files = request.FILES.getlist('images')  # Nombre del campo de los archivos

            if files:
                # Aquí puedes procesar los archivos
                # Por ejemplo, guardarlos o hacer algo con ellos
                for file in files:
                    # print(file.name)  # Imprimir el nombre de cada archivo
                    obj = galeria_prod.objects.create(imagenes=file,fk_color_id = id_color,fk_productos_id = id_prod)

                # return JsonResponse({'message': 'Archivos recibidos correctamente'}, status=200)
                print('Archivos recibidos correctamente')

            else:
                # return JsonResponse({'message': 'No se han enviado archivos'}, status=400)
                print('No se han enviado archivos')
                
        
        
        det_prod = detalle_prod.objects.raw("""SELECT * 
        FROM productos_detalle_prod AS dp 
        INNER JOIN productos_productos AS p ON p.id_producto = dp.fk_productos_id
        INNER JOIN productos_color AS c ON c.id_color = dp.fk_color_id
        INNER JOIN productos_tallas AS t ON t.id_tallas = dp.fk_talla_id
        INNER JOIN productos_tipo AS tp ON tp.id_tipo = dp.fk_tipo_id
        INNER JOIN productos_seccion AS s ON s.id_seccion = dp.fk_seccion_id
        WHERE p.id_producto = %s
        GROUP BY c.color""",[id_prod])
        
        return render(request,"catalogos/productos/detalle_producto.html",{"det_prod":det_prod})

def consulta_listas(request,tipos,dato):
    t = tipos
    
    if t == '1':
        consulta = seccion.objects.all()
    elif t == '2':
        consulta = tipo.objects.all()
    elif t == '3':
        consulta = color.objects.all()
    
    return render(request,"catalogos/productos/consulta_listas.html",{"tipo":t,"consulta":consulta,"dato":dato})


def guarda_lista(request):
    tip = request.POST['tipo']
    id_producto = request.POST['id_producto']
    id_seccion = request.POST['id_seccion']
    id_tipo = request.POST['id_tipo']
    id_color = request.POST['id_color']
    
    if tip == '1':
        new_seccion = request.POST['new_id_seccion']
        
        # para actualizar multiples filas y diferentes campos
        det = detalle_prod.objects.filter(fk_color_id = id_color, fk_productos_id = id_producto, fk_tipo_id = id_tipo, fk_seccion_id = id_seccion).update(fk_seccion_id = new_seccion)

        return HttpResponse("se guardo nueva seccion")
    elif tip == '2':
        new_tipo= request.POST['new_id_tipo']
        
        # para actualizar multiples filas y diferentes campos
        det = detalle_prod.objects.filter(fk_color_id = id_color, fk_productos_id = id_producto, fk_tipo_id = id_tipo, fk_seccion_id = id_seccion).update(fk_tipo_id = new_tipo)
        
        return HttpResponse("se guardo nuevo tipo")
    
    elif tip == '3':
        new_color= request.POST['new_id_color']
        
        # para actualizar multiples filas y diferentes campos
        det = detalle_prod.objects.filter(fk_color_id = new_color, fk_productos_id = id_producto, fk_tipo_id = id_tipo, fk_seccion_id = id_seccion)
        det = det.count()
        
        if det == 0:
            # para actualizar multiples filas y diferentes campos
            det = detalle_prod.objects.filter(fk_color_id = id_color, fk_productos_id = id_producto, fk_tipo_id = id_tipo, fk_seccion_id = id_seccion).update(fk_color_id = new_color)
            
            return HttpResponse("se guardo nuevo color")
        else:
            
            return HttpResponse("1")

def modal_tallas(request):
    
    all_tallas = tallas.objects.all()
    
    uuid_prod = request.POST['uuid_prod']
    id_seccion = request.POST['id_seccion']
    id_tipo = request.POST['id_tipo']
    id_color = request.POST['id_color']
    
    ta = tallas.objects.raw("""SELECT * 
    FROM productos_detalle_prod AS dp 
    INNER JOIN productos_productos AS p ON p.id_producto = dp.fk_productos_id
    INNER JOIN productos_tallas AS t ON t.id_tallas = dp.fk_talla_id
    WHERE p.uuid_producto = %s
    AND dp.fk_color_id = %s
    AND dp.fk_tipo_id = %s
    AND dp.fk_seccion_id = %s""",[uuid_prod,id_color,id_tipo,id_seccion])
    
    variable = []
    
    for at in all_tallas:
        at_id = at.id_tallas
        at_talla = at.talla
        
        for t in ta:
            ta_id = t.id_tallas
            ta_talla = t.talla
            
            if ta_id == at_id:
                # print("iguales " + ta_talla)
                variable.append({"id_talla": ta_id, "talla": ta_talla,"check":1})
                # print(variable)
                break
        
        if ta_id != at_id:
            # print("no ioguales, ta_id: " + str(ta_id) + " at_id: " + str(at_id))
            variable.append({"id_talla": at_id, "talla": at_talla,"check":0})
    
    
    
    return render(request,"catalogos/productos/modal_tallas.html",{"tallas_con": ta,"tallas":variable})


def elimina_det_talla(request):
    id_detalle = request.POST['id_det_talla']
    
    det = detalle_prod.objects.get(id_detalle = id_detalle)
    
    det.delete()
    
    all_tallas = tallas.objects.all()
    
    uuid_prod = request.POST['uuid_prod']
    id_seccion = request.POST['id_seccion']
    id_tipo = request.POST['id_tipo']
    id_color = request.POST['id_color']
    
    ta = tallas.objects.raw("""SELECT * 
    FROM productos_detalle_prod AS dp 
    INNER JOIN productos_productos AS p ON p.id_producto = dp.fk_productos_id
    INNER JOIN productos_tallas AS t ON t.id_tallas = dp.fk_talla_id
    WHERE p.uuid_producto = %s
    AND dp.fk_color_id = %s
    AND dp.fk_tipo_id = %s
    AND dp.fk_seccion_id = %s""",[uuid_prod,id_color,id_tipo,id_seccion])
    
    variable = []
    
    for at in all_tallas:
        at_id = at.id_tallas
        at_talla = at.talla
        
        for t in ta:
            ta_id = t.id_tallas
            ta_talla = t.talla
            
            if ta_id == at_id:
                # print("iguales " + ta_talla)
                variable.append({"id_talla": ta_id, "talla": ta_talla,"check":1})
                # print(variable)
                break
        
        if ta_id != at_id:
            # print("no ioguales, ta_id: " + str(ta_id) + " at_id: " + str(at_id))
            variable.append({"id_talla": at_id, "talla": at_talla,"check":0})
    
    
    
    return render(request,"catalogos/productos/modal_tallas.html",{"tallas_con": ta,"tallas":variable})



def agrega_mod_tallas(request):
    
    all_tallas = tallas.objects.all()
    
    id_prod = request.POST['id_producto']
    uuid_prod = request.POST['uuid_prod']
    id_seccion = request.POST['id_seccion']
    id_tipo = request.POST['id_tipo']
    id_color = request.POST['id_color']
    tallas_array = request.POST.getlist("id_talla[]")
    
    # print(tallas_array)
    
    
    count_tallas = 0
    for t in tallas_array:
        
        _det = detalle_prod.objects.filter(fk_color_id = id_color,
        fk_productos_id = id_prod,
        fk_talla_id = t,
        fk_tipo_id = id_tipo,
        fk_seccion_id = id_seccion)
        
        count_det = _det.count()
        
        # print(count_det)
        
        if count_det == 0:
        
            det_pr = detalle_prod.objects.create(
                bandera = 0,
                fk_color_id = id_color,
                fk_productos_id = id_prod,
                fk_talla_id = t,
                fk_tipo_id = id_tipo,
                fk_seccion_id = id_seccion
            )
            
            count_tallas +=  1
            # print(t)
            
    ta = tallas.objects.raw("""SELECT * 
    FROM productos_detalle_prod AS dp 
    INNER JOIN productos_productos AS p ON p.id_producto = dp.fk_productos_id
    INNER JOIN productos_tallas AS t ON t.id_tallas = dp.fk_talla_id
    WHERE p.uuid_producto = %s
    AND dp.fk_color_id = %s
    AND dp.fk_tipo_id = %s
    AND dp.fk_seccion_id = %s""",[uuid_prod,id_color,id_tipo,id_seccion])
    
    variable = []
    
    for at in all_tallas:
        at_id = at.id_tallas
        at_talla = at.talla
        
        for t in ta:
            ta_id = t.id_tallas
            ta_talla = t.talla
            
            if ta_id == at_id:
                # print("iguales " + ta_talla)
                variable.append({"id_talla": ta_id, "talla": ta_talla,"check":1})
                # print(variable)
                break
        
        if ta_id != at_id:
            # print("no ioguales, ta_id: " + str(ta_id) + " at_id: " + str(at_id))
            variable.append({"id_talla": at_id, "talla": at_talla,"check":0})
    
    
    
    return render(request,"catalogos/productos/modal_tallas.html",{"tallas_con": ta,"tallas":variable})       



def modal_imagenes(request):
    id_prod = request.POST['id_producto']
    id_color = request.POST['id_color']
    
    images = galeria_prod.objects.filter(fk_color_id = id_color, fk_productos_id = id_prod)
    
    datos_img = images.first()
    return render(request,"catalogos/productos/modal_imagenes.html",{"images":images,"datos_img":datos_img})  


def elimina_images(request):
    id_galeria = request.POST['id_galeria']
    id_prod = request.POST['id_producto']
    id_color = request.POST['id_color']
    
    #eliminamos imagen
    gal = galeria_prod.objects.get(id_galeria = id_galeria)
    
    gal.delete()
    
    
    
    images = galeria_prod.objects.filter(fk_color_id = id_color, fk_productos_id = id_prod)
    
    datos_img = images.first()
    return render(request,"catalogos/productos/modal_imagenes.html",{"images":images,"datos_img":datos_img})  



def agrega_imagen_modal(request):
    
    id_prod = request.POST['id_producto']
    id_color = request.POST['id_color']
    
    #para insertar la galeria de productos con un file multiple
    if request.FILES:
        files = request.FILES.getlist('images')  # Nombre del campo de los archivos

        if files:
            # Aquí puedes procesar los archivos
            # Por ejemplo, guardarlos o hacer algo con ellos
            for file in files:
                # print(file.name)  # Imprimir el nombre de cada archivo
                obj = galeria_prod.objects.create(imagenes=file,fk_color_id = id_color,fk_productos_id = id_prod)

            # return JsonResponse({'message': 'Archivos recibidos correctamente'}, status=200)
            print('Archivos recibidos correctamente')

        else:
            # return JsonResponse({'message': 'No se han enviado archivos'}, status=400)
            print('No se han enviado archivos')
            
            
    images = galeria_prod.objects.filter(fk_color_id = id_color, fk_productos_id = id_prod)
    
    datos_img = images.first()
    return render(request,"catalogos/productos/modal_imagenes.html",{"images":images,"datos_img":datos_img})



def elimina_mod_prod(request):
    id_prod = request.POST['id_producto']
    id_seccion = request.POST['id_seccion']
    id_tipo = request.POST['id_tipo']
    id_color = request.POST['id_color']
    
    det = detalle_prod.objects.filter(fk_color_id = id_color, fk_productos_id = id_prod, fk_tipo_id = id_tipo, fk_seccion_id = id_seccion).delete()
    
    gal = galeria_prod.objects.filter(fk_color_id = id_color,fk_productos_id = id_prod).delete()
        
    
    return HttpResponse("elimina prod")
    
    

# ========================================= COLORES VESTIMENTA ===============================================================
def colores_list(request):
    # consultamos los colores
    color_ls = color.objects.all()
    
    return render(request,"catalogos/colores/color.html",{"color":color_ls})
   
   
def registra_color(request):
    return render(request,"catalogos/colores/registra_color.html")

def guarda_color(request):
    cod_color = request.POST['cod_color']
    nom_color = request.POST['nombre_color']
    
    c = color.objects.create(
        color = nom_color,
        cod_color = cod_color,
        bandera = 0
    )
    
    
    messages.error(request,'Alta de Color existosa')

    return redirect('colores')


def modifica_color(request,uuid):
    col = color.objects.get(uuid_color = uuid)
    return render(request,"catalogos/colores/modifica_color.html",{"color":col})


def guarda_mod_color(request):
    id_color = request.POST['id_color']
    uuid_color = request.POST['uuid_color']
    cod_color = request.POST['cod_color']
    nombre_color = request.POST['nombre_color']
    
    
    col = color.objects.get(id_color = id_color)
    
    col.cod_color = cod_color
    col.color = nombre_color
    col.save()
    
    
    messages.error(request,'Modificacion de Color existosa')

    return redirect('colores')


def elimina_color(request,uuid):
    col = color.objects.get(uuid_color = uuid)
    
    col.delete()
    
    messages.error(request,'Eliminacion de Color existosa')

    return redirect('colores')



# ========================================= TIPO VESTIMENTA ===============================================================
def tipo_list(request):
    # consultamos los colores
    tipo_ls = tipo.objects.all()
    
    return render(request,"catalogos/tipo/tipo.html",{"tipo":tipo_ls})



def registra_tipo(request):
    return render(request,"catalogos/tipo/registra_tipo.html")


def guarda_tipo_vestimenta(request):
    tipo_vestimenta = request.POST['tipo_vestimenta']
    
    tp = tipo.objects.create(
        tipo = tipo_vestimenta,
        bandera = 0
    )
    
    
    messages.error(request,'Registo de Tipo Vestimenta existosa')

    return redirect('tipo')


def modifica_tipo_vest(request,uuid):
    tp = tipo.objects.get(uuid_tipo = uuid)
    
    return render(request,"catalogos/tipo/modifica_tipo.html",{"tipo":tp})


def guarda_mod_tipo_vest(request):
    id_tipo = request.POST['id_tipo_vest']
    uuid_tipo = request.POST['uuid_tipo_vest']
    tipo_vest = request.POST['tipo_vestimenta']
    
    tp = tipo.objects.get(id_tipo = id_tipo)
    
    tp.tipo = tipo_vest
    tp.save()
    
    
    messages.error(request,'Modificacion de Tipo Vestimenta existosa')

    return redirect('tipo')


def elimina_tipo_vest(request,uuid):
    tp = tipo.objects.get(uuid_tipo = uuid)
    
    tp.delete()
    
    
    messages.error(request,'Eliminacion de Tipo Vestimenta existosa')

    return redirect('tipo')
    
    
    
# ========================================= SECCION VESTIMENTA ===============================================================
def seccion_list(request):
    # consultamos los colores
    seccion_ls = seccion.objects.all()
    
    return render(request,"catalogos/seccion/seccion.html",{"seccion":seccion_ls})


def registra_seccion(request):
    return render(request,"catalogos/seccion/registra_seccion.html")


def guarda_seccion(request):
    seccion_vest = request.POST['seccion']
    
    sec = seccion.objects.create(
        seccion = seccion_vest,
        bandera = 0
    )
    
    
    messages.error(request,'Registro de Seccion Vestimenta existosa')

    return redirect('seccion')


def modifica_seccion(request,uuid):
    sec = seccion.objects.get(uuid_seccion = uuid)
    
    return render(request,"catalogos/seccion/modifica_seccion.html",{"seccion":sec})


def guarda_mod_seccion(request):
    id_seccion = request.POST['id_seccion']
    uuid_seccion = request.POST['uuid_seccion']
    seccion_vest = request.POST['seccion']
    
    
    sec = seccion.objects.get(id_seccion = id_seccion)
    
    sec.seccion = seccion_vest
    sec.save()
    
    messages.error(request,'Modificacion de Seccion Vestimenta existosa')

    return redirect('seccion')


def elimina_seccion(request,uuid):
    sec = seccion.objects.get(uuid_seccion = uuid)
    
    sec.delete()
    
    
    messages.error(request,'Eliminacion de Seccion Vestimenta existosa')

    return redirect('seccion')



# ========================================= TALLA VESTIMENTA ===============================================================
def talla_list(request):
    # consultamos los colores
    talla_ls = tallas.objects.all()
    
    return render(request,"catalogos/talla/talla.html",{"talla":talla_ls})


def registra_talla(request):
    return render(request,"catalogos/talla/registra_talla.html")


def guarda_talla(request):
    _talla = request.POST['talla']
    cod_talla = request.POST['cod_talla']
    
    t = tallas.objects.create(
        talla = _talla,
        cod_talla = cod_talla,
        bandera = 0
    )
    
    messages.error(request,'Registro de Talla existosa')
    
    return redirect('talla')



def modifica_talla(request,uuid):
    _talla = tallas.objects.get(uuid_tallas = uuid)
    
    return render(request,"catalogos/talla/modifica_talla.html",{"talla":_talla})


def guarda_mod_talla(request):
    id_talla =  request.POST['id_talla']
    uuid_talla =  request.POST['uuid_talla']
    _talla =  request.POST['talla']
    cod_talla =  request.POST['cod_talla']
    
    t = tallas.objects.get(id_tallas = id_talla)
    
    t.talla = _talla
    t.cod_talla = cod_talla
    t.save()
    
    
    messages.error(request,'Modificacion de Talla existosa')
    
    return redirect('talla')


def elimina_talla(request,uuid):
    t = tallas.objects.get(uuid_tallas = uuid)
    
    t.delete()    
    
    messages.error(request,'Eliminacion de Talla existosa')
    
    return redirect('talla')
    
    
    
    
    
# ========================================= INVENTARIO ===============================================================
def inventario_list(request):
    prod = productos.objects.all()
    
    inv_prod = inventario.objects.raw("""SELECT *, SUM(stock) AS total_stock, 
    CASE WHEN SUM(stock) = '' OR SUM(stock) = 0 OR SUM(stock) = (NULL) THEN "#ffffff;" 
    WHEN SUM(stock) < 50 THEN "#f8a1a1;" 
    WHEN SUM(stock) < 500 THEN "#fff69b;" 
    WHEN SUM(stock) > 500 THEN "#b8ff9b;" 
    END AS cod_color
    FROM productos_inventario AS inv
    INNER JOIN productos_detalle_prod AS dp ON dp.id_detalle = inv.fk_det_productos_id
    RIGHT JOIN productos_productos AS p ON p.id_producto = dp.fk_productos_id
    GROUP BY p.id_producto""")
        
        
        
        
    return render(request,"inventario/inventario.html",{"productos":prod,"inv_prod":inv_prod})

def carga_datos_list(request):
    
    id_prod = request.POST['id_prod']
    
    
    inv = inventario.objects.filter(fk_det_productos__fk_productos_id = id_prod)
    
    count_inv = inv.count()
    
    if count_inv > 0: 
        
        det_inv = inventario.objects.raw("""SELECT * 
        FROM productos_inventario AS inv 
        INNER JOIN productos_detalle_prod AS dp ON dp.id_detalle = inv.fk_det_productos_id
        INNER JOIN productos_productos AS p ON p.id_producto = dp.fk_productos_id
        INNER JOIN productos_color AS c ON c.id_color = dp.fk_color_id
        INNER JOIN productos_tallas AS t ON t.id_tallas = dp.fk_talla_id
        INNER JOIN productos_tipo AS tp ON tp.id_tipo = dp.fk_tipo_id
        INNER JOIN productos_seccion AS s ON s.id_seccion = dp.fk_seccion_id
        WHERE p.id_producto = %s
        GROUP BY c.color""",[id_prod])
        
        
        
        variable =[]
        
        for d in det_inv:
            id_prod_inv = d.id_producto
            id_color_inv = d.id_color
            
            
            det_prod_inv = detalle_prod.objects.raw("""SELECT * 
            FROM productos_inventario AS inv 
            RIGHT JOIN productos_detalle_prod AS dp ON dp.id_detalle = inv.fk_det_productos_id
            INNER JOIN productos_productos AS p ON p.id_producto = dp.fk_productos_id
            INNER JOIN productos_color AS c ON c.id_color = dp.fk_color_id
            INNER JOIN productos_tallas AS t ON t.id_tallas = dp.fk_talla_id
            INNER JOIN productos_tipo AS tp ON tp.id_tipo = dp.fk_tipo_id
            INNER JOIN productos_seccion AS s ON s.id_seccion = dp.fk_seccion_id
            WHERE p.id_producto = %s
            AND c.id_color = %s """,[id_prod_inv,id_color_inv])
            
            variable.append(det_prod_inv)
            
        
        
        
            
        
        # return HttpResponse("ayuda %s" %id_prod)    
        return render(request,"inventario/det_inventario.html",{"det":det_inv,"variable":variable,"tipo":1})
    
    else:
        
    
        # det = detalle_prod.objects.filter(fk_productos_id = id_prod)
        det_prod = detalle_prod.objects.raw("""SELECT * 
        FROM productos_detalle_prod AS dp 
        INNER JOIN productos_productos AS p ON p.id_producto = dp.fk_productos_id
        INNER JOIN productos_color AS c ON c.id_color = dp.fk_color_id
        INNER JOIN productos_tallas AS t ON t.id_tallas = dp.fk_talla_id
        INNER JOIN productos_tipo AS tp ON tp.id_tipo = dp.fk_tipo_id
        INNER JOIN productos_seccion AS s ON s.id_seccion = dp.fk_seccion_id
        WHERE p.id_producto = %s
        GROUP BY c.color""",[id_prod])
        
        
        variable =[]
        
        for d in det_prod:
            id_prod_det = d.id_producto
            id_color_det = d.id_color
            
            
            det_prod_espec = detalle_prod.objects.raw("""SELECT * 
            FROM productos_detalle_prod AS dp 
            RIGHT JOIN productos_productos AS p ON p.id_producto = dp.fk_productos_id
            INNER JOIN productos_color AS c ON c.id_color = dp.fk_color_id
            INNER JOIN productos_tallas AS t ON t.id_tallas = dp.fk_talla_id
            INNER JOIN productos_tipo AS tp ON tp.id_tipo = dp.fk_tipo_id
            INNER JOIN productos_seccion AS s ON s.id_seccion = dp.fk_seccion_id
            WHERE p.id_producto = %s
            AND c.id_color = %s """,[id_prod_det,id_color_det])
            
            variable.append(det_prod_espec)
            
        
        
        
            
        
        # return HttpResponse("ayuda %s" %id_prod)    
        return render(request,"inventario/det_inventario.html",{"det":det_prod,"variable":variable,"tipo":2})
    
    

def carga_modal_progre(request):
    return render(request,"inventario/modal_progreso.html")
    
    

def guarda_inventario(request):
    
    tipo_inv = request.POST['tipo_inv']
    
    if tipo_inv == '1':  
        
        id_det_prod = request.POST['id_det_prod']
        cantidad = request.POST['cantidad']  
    
        inv = inventario.objects.filter(fk_det_productos__id_detalle= id_det_prod)
        
        count_inv = inv.count()
        
        print(count_inv)
        
        if count_inv == 0: 
            
            inv_prod = inventario.objects.create(
                stock = cantidad,
                cantidad = cantidad, 
                almacen = 1,
                bandera = 0,
                fk_det_productos_id = id_det_prod
            )
            
            return HttpResponse("aqui se guarda algo")
        else:           
            
            return HttpResponse("No se creo nada nada")
    
    else:
        id_inventario = request.POST['id_det_prod']
        cantidad = request.POST['cantidad']  
        
        inv = inventario.objects.filter(id_inventario = id_inventario)
        
        
        count_inv = inv.count()
        
        if count_inv == 0: 
            
            inv_prod = inventario.objects.create(
                stock = cantidad,
                cantidad = cantidad, 
                almacen = 1,
                bandera = 0,
                fk_det_productos_id = id_det_prod
            )
            
            return HttpResponse("aqui se guarda algo en la modificacion ")
        else: 
            
            inv = inv.get()     
        
            stock = inv.stock
            cant = inv.cantidad
            
            new_stock = int(stock) + int(cantidad)
            new_cantidad = int(cant) + int(cantidad)
            
            inv.stock = new_stock
            inv.cantidad = new_cantidad
            inv.save()
            
            return HttpResponse("aqui se actualizo algo")