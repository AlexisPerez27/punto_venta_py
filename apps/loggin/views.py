from django.shortcuts import render,redirect,get_object_or_404 #importamos funciones de operacion para django
from django.http import HttpResponse, JsonResponse #para mostrar mensajes o resultados en la pagina
from .models import pais,estados,municipios, usuarios, sesiones, historial_sesiones, restablecer_contras,datos_api_cp
from django.db.models import Q
import requests
from django.contrib import messages
import bcrypt
from django.contrib.auth import login,logout, authenticate
import socket
from django.utils import timezone
from django.contrib.auth.decorators import login_required



# Create your views here.
def iniciar_sesion(request):
    return render(request,"iniciar_sesion.html")


def inicio_sesion(request):

    correo_us = request.POST['correo_usu']
    contras = request.POST['pass']

    #consultar usuario o correo
    # _correo_us = sesiones.objects.filter(correo=correo_us) | sesiones.objects.filter(usuario_sesion=correo_us)
    # el Q sirve para concatenar condiciones pero solo son para los OR en AND no sirve
    _correo_us = sesiones.objects.filter(Q(correo=correo_us) | Q(usuario_sesion=correo_us))

    #autenticamos al usuario y contraseña
    ses = authenticate(request, usuario_sesion=correo_us,contra=contras)      

    # login(request,ses)

    # Verificar si el usuario existe
    if _correo_us.exists():

        # Asegurarse de obtener el primer usuario encontrado
        user = _correo_us.first()
        # Obtener la contraseña almacenada en la base de datos
        _contra = user.contra
        #obtenemos id de sesion
        _id_sesion = user.id_sesion

        #colocamos encode a la contraseña del input
        contra_bytes = contras.encode("utf-8")

        #consultamos en la tabla restablece contras la ultima contraseña activa por el usuario
        _restablece_pass = restablecer_contras.objects.filter(fk_sesion_id = _id_sesion, activa = 'SI', bandera = 1).count()

        # return HttpResponse("conteo de restablece pass= %s" %_restablece_pass)
    
        # condicion para comparar la contraseña del input contra la contraseña de la bd que tiene bcrypt
        if bcrypt.checkpw(contra_bytes,_contra.encode("utf-8")) and _restablece_pass == 1:
            #agregamos variables de sesiones
            usu_correo = request.session['usu_correo'] = user.correo
            usu_usuario = request.session['usu_usuario'] = user.usuario_sesion
            usu_uuid = request.session['usu_uuid'] = user.uuid_sesion.__str__()
            usu_permisos = request.session['usu_permisos'] = user.fk_permisos_id
            usu_img_perfil = request.session['usu_img_perfil'] = user.fk_usuario.foto.url

            hostname = socket.gethostname()
            IPAddr = socket.gethostbyname(hostname)

            _historial_sesion = historial_sesiones.objects.create(
                fecha = timezone.now(), #feca hora actual
                direccion_ip = IPAddr,
                fk_sesion_id = _id_sesion,
                nombre_equipo = hostname

            )
            
            return redirect('inicio')
        else: 
            messages.error(request,'La contraseña son incorrectos')
            return redirect('iniciar_sesion')

    else:
        messages.error(request, 'El usuario/correo son incorrectos')
        return redirect('iniciar_sesion')
    

def cerrar_sesion(request):
    #para eliminar sesiones
    del request.session['usu_correo']
    del request.session['usu_usuario']
    del request.session['usu_uuid']

    request.session.clear()
    request.session.flush()

    logout(request,)

    return redirect("inicio")




def registrar_usu(request):
    _pais = pais.objects.all()
    _estado_civil = usuarios.objects.all()
    return render(request,"registrar_usuario.html", {'paises':_pais})


def consulta_estados(request):
    if request.POST:
        _id_pais = request.POST['id_pais']
        
        _estados = estados.objects.filter(fk_pais = _id_pais)

        return render(request,"registrar/consulta_estados.html",{'estados_con': _estados})

def alta_estado_mod(request):

    if request.POST:
        _id_pais = request.POST['id_pais']
        _estado = request.POST['estado']

        _estados = estados.objects.create(
            estados = _estado,
            fk_pais_id = _id_pais,
        )


        _estados_con = estados.objects.filter(fk_pais = _id_pais)

        return render(request,"registrar/consulta_estados.html",{'estados_con': _estados_con})


def consulta_municipios(request):
    if request.POST:
        _id_estado = request.POST['id_estado']
        
        _municipios = municipios.objects.filter(fk_estados = _id_estado)

        return render(request,"registrar/consulta_municipios.html",{'municipios_con': _municipios})
    


def alta_municipio_mod(request):

    if request.POST:
        _id_estado = request.POST['id_estado']
        _municipio = request.POST['municipio']

        _municipios = municipios.objects.create(
            municipios = _municipio,
            fk_estados_id = _id_estado,
        )


        _municipios_con = municipios.objects.filter(fk_estados = _id_estado)

        return render(request,"registrar/consulta_municipios.html",{'municipios_con': _municipios_con})
    

def consulta_cp(request):

    _cp = request.POST['cp']

    ########################################################################################################################################
    #
    #               ESTE SE OCUPA CUANDO EL JSON TRAE O TIENE MUCHOS REGISTROS
    #
    #########################################################################################################################################
    """ URL_API = "https://fakestoreapi.com/products"
    try:
        # Intenta realizar la solicitud GET a la API
        response = requests.get(URL_API)
        if response.status_code == 200:
            # se utiliza el método json() para extraer los datos en formato JSON de la respuesta y se almacenan en la variable productos
            productos = response.json()
        else:
            # En caso de un código de respuesta no exitoso, manejar de acuerdo a tus necesidades
            print(f"Error en la solicitud: {response.status_code}")
            productos = []

    except requests.RequestException as e:
        # Manejar errores de solicitud, por ejemplo, problemas de red
        print(f"Error en la solicitud: {e}")
        productos = []

    return render(request, 'registrar/consulta_cp.html', {'productos': productos}) """



    ########################################################################################################################################
    #
    #               ESTE SE OCUPA CUANDO EL JSON TRAE UN SOLO REGISTRO
    #
    #########################################################################################################################################

    # URL de productos
    URL_API = "http://127.0.0.1:8000/codigos/"+ str(_cp)

    # Realizar la solicitud GET a la API
    response = requests.get(URL_API)

    if response.status_code == 200:
        codigo = response.json()
        
        # for codigo in codigo:
        #     print(codigo)
        # _cp = _cp.split(' ')
        # return JsonResponse(productos)
        
        # return JsonResponse(codigo_postal)

        return render(request,"registrar/consulta_cp.html",{'cp': codigo})
    else:
        # Lista vacia
        productos = []
   



def busca_usuario(request):
    usu = request.POST['usuario']

    _usuarios = sesiones.objects.filter(usuario_sesion = usu).count()
    
    if (_usuarios > 0):
        return HttpResponse("Error el usuario %s " %usu  + " ya existe" )
    else:
        return HttpResponse("")



def busca_correo(request):
    mail = request.POST['correo']

    _correo = sesiones.objects.filter(correo = mail).count()
    
    if (_correo > 0):
        return HttpResponse("Error el correo %s " %mail  + " ya existe" )
    else:
        return HttpResponse("")



def alta_usuario(request):
   
    nombre = request.POST['nombre']
    apellidos = request.POST['apellidos']
    fecha_nac = request.POST['fecha_nac']
    telefono = request.POST['telefono']
    sexo = request.POST.get('sexo')
    civil = request.POST['civil']
    cod_postal = request.POST['cod_postal']

    if cod_postal == "":
        cod_postal = 0    
    
    _estado = request.POST['estado_select']
    _municipio = request.POST['municipio_select']
    correo = request.POST['correo']
    usuario = request.POST['usuario']
    password = request.POST['pass']
    pass_confirm = request.POST['pass_confirm']
    foto = request.FILES['foto']


    contra = password.encode('utf-8')

    pass_encry = bcrypt.gensalt()

    pass_en = bcrypt.hashpw(contra, pass_encry)

    #esta linea se ocupa para que mi contraseña no se guarde en la bd como b'contraseña' y se guarde como 'contraseña' 
    pass_decode = pass_en.decode("utf-8")


    # return HttpResponse("contra utf8 = %s" %contra + "<br>contra gensalt = %s" %pass_encry + "<br>contra hash = %s" %pass_en + "<br> pass_ = %s" %pass_)

    #  de esta manera guardamos en lka base de datos
    _usu = usuarios.objects.create(
        nombre = nombre,
        apellidos = apellidos,
        fecha_nac = fecha_nac,
        estado_civil = civil,
        sexo = sexo,
        telefono = telefono,
        foto = foto,
        fk_municipios = _municipio,
        fk_cod_postal = cod_postal
    )


    usu_filtro = usuarios.objects.all().order_by('-id_usuarios')[:1] #para hacer un top a la consulta :1,:5,:10
    usu_filtro = usu_filtro.get() #para obtener los datos de la consulta unica

    usu_filtro.id_usuarios

    # for usu in usu_filtro:
    #     id_usuario_fil = usu.id_usuarios
    

    #guardamos en la tabla de la base de datos un nuevo registro
    _sesion = sesiones.objects.create(
        correo = correo,
        usuario_sesion = usuario,
        contra = pass_decode,
        fk_permisos_id = 1,
        fk_usuario_id = usu_filtro.id_usuarios
    )


    ses_filtro = sesiones.objects.all().order_by('-id_sesion')[:1] #para hacer un top a la consulta :1,:5,:10
    id_ses_fil = ses_filtro.get() #para obtener los datos de la consulta unica

    id_ses_ = id_ses_fil.id_sesion
    
    contras_restablece = restablecer_contras.objects.create(
        contra_anterior = pass_decode,
        activa = 'SI',
        bandera = 1,
        bandera2 = 0,
        fk_sesion_id = id_ses_
    )


    if cod_postal != 0:
        _estado_api = request.POST['estado_api']
        _muni_api = request.POST['muni_api']
        _colonias_api = request.POST['colonias_select_api']

        _datos_api_cp = datos_api_cp.objects.create(
            codigo_postal_api = cod_postal,
            estado_api = _estado_api,
            municipio_api = _muni_api,
            colonia_api = _colonias_api,
            fk_cod_postal_id = usu_filtro.id_usuarios
        )

    # messages.success(request,'Registro de usuario Existoso, Ahora puedes iniciar sesion')

    # lista = [nombre,apellidos,fecha_nac,telefono,sexo,civil,cod_postal, _estado,_municipio, correo,usuario,password,pass_confirm, foto]    
    # lista2 = [fecha,direccion_ip,fk_sesion_id,nombre_equipo]
    # return HttpResponse("esto es el alta ")

    return redirect('iniciar_sesion')





# =============================== PARA LA MODIFICACION DE PERFIL =============================================
def perfil(request):
    
    usuario = sesiones.objects.filter(uuid_sesion = request.session['usu_uuid'])

    usuario = usuario.get()

    return render(request,"perfil/perfil.html", {'usuario': usuario})


def editar_perfil(request,uuid):    

    # para consultar usuario
    usuario = usuarios.objects.filter(uuid_usu = uuid)
    usuario = usuario.get()
    usuario.id_usuarios
    _cp = usuario.fk_cod_postal


    # para consultar datos_api_cp
    datos_api = datos_api_cp.objects.filter(fk_cod_postal_id = usuario.id_usuarios)
    datos_api = datos_api.get()


    _pais = pais.objects.all()

    #consulta anidada 
    _pais_selec = pais.objects.raw("""SELECT * 
    FROM loggin_usuarios AS u
    INNER JOIN loggin_municipios AS m ON m.id_municipios = u.fk_municipios
    INNER JOIN loggin_estados AS e ON e.id_estados = m.fk_estados_id
    INNER JOIN loggin_pais AS p ON p.id_pais = e.fk_pais_id
    WHERE u.id_usuarios = %s""",[usuario.id_usuarios])

    
    for p in _pais_selec:
        _id_pais = p.id_pais
        _id_estado = p.id_estados
        _id_muni = p.id_municipios

    # codigo = ""

    if _cp != 0 :
        # URL de productos
        URL_API = "http://127.0.0.1:8000/codigos/"+ str(_cp)

        # Realizar la solicitud GET a la API
        response = requests.get(URL_API)

        if response.status_code == 200:
            codigo = response.json()
            # return render(request,"perfil/consulta_cp_editar.html",{'cp': codigo, 'tipo':2})
        else:
            # Lista vacia
            productos = []  
            return HttpResponse("5")
        
        return render(request,"perfil/editar_perfil.html", {'paises': _pais,'pais_select': _pais_selec,'usuario' : usuario, 'cod_pos': datos_api, 'datos_cp_api' : codigo}) #
    else:
        #pra estados
        _estados = estados.objects.filter(fk_pais_id = _id_pais)

        #para municipios
        _municipio = municipios.objects.filter(fk_estados_id = _id_estado)

        return render(
            request,
            "perfil/editar_perfil.html", 
            {
                'paises': _pais,
                'pais_select': _pais_selec,
                'usuario' : usuario, 
                'cod_pos': datos_api, 
                'res_estados':_estados, 
                'res_municipios': _municipio
            }
        )

    





def consulta_estados_editar(request):
    if request.POST:
        _id_pais = request.POST['id_pais']
        
        _estados = estados.objects.filter(fk_pais = _id_pais)

        return render(request,"perfil/consulta_estados_editar.html",{'estados_con': _estados})

def alta_estado_mod_editar(request):

    if request.POST:
        _id_pais = request.POST['id_pais']
        _estado = request.POST['estado']

        _estados = estados.objects.create(
            estados = _estado,
            fk_pais_id = _id_pais,
        )


        _estados_con = estados.objects.filter(fk_pais = _id_pais)

        return render(request,"perfil/consulta_estados_editar.html",{'estados_con': _estados_con})


def consulta_municipios_editar(request):
    if request.POST:
        _id_estado = request.POST['id_estado']
        
        _municipios = municipios.objects.filter(fk_estados = _id_estado)

        return render(request,"perfil/consulta_municipios_editar.html",{'municipios_con': _municipios})
    


def alta_municipio_mod_editar(request):

    if request.POST:
        _id_estado = request.POST['id_estado']
        _municipio = request.POST['municipio']

        _municipios = municipios.objects.create(
            municipios = _municipio,
            fk_estados_id = _id_estado,
        )


        _municipios_con = municipios.objects.filter(fk_estados = _id_estado)

        return render(request,"perfil/consulta_municipios_editar.html",{'municipios_con': _municipios_con})
    

def consulta_cp_editar(request):

    _cp = request.POST['cp']

    _tipo = request.POST['tipo']

    if _tipo == '1':

        # URL de productos
        URL_API = "http://127.0.0.1:8000/codigos/"+ str(_cp)

        # Realizar la solicitud GET a la API
        response = requests.get(URL_API)

        if response.status_code == 200:
            codigo = response.json()           
            
            # for codigo in codigo:
            #     print(codigo)
            # _cp = _cp.split(' ')
            # return JsonResponse(productos)
            
            # return JsonResponse(codigo_postal)

            _usuario = sesiones.objects.filter(uuid_sesion = request.session['usu_uuid'])

            _user = _usuario.get()

            _datos_cp = datos_api_cp.objects.filter(fk_cod_postal_id = _user.fk_usuario.id_usuarios, codigo_postal_api = _cp)
            
            # return HttpResponse("%s" %_datos_cp)

            return render(request,"perfil/consulta_cp_editar.html",{'datos_cp': _datos_cp,'cp': codigo,'tipo':1})
        else:
            # Lista vacia
            productos = []
    
    else:
        # URL de productos
        URL_API = "http://127.0.0.1:8000/codigos/"+ str(_cp)

        # Realizar la solicitud GET a la API
        response = requests.get(URL_API)

        if response.status_code == 200:
            codigo = response.json()
            
            # for codigo in codigo:
            #     print(codigo)
            # _cp = _cp.split(' ')
            # return JsonResponse(productos)
            
            # return JsonResponse(codigo_postal)

            return render(request,"perfil/consulta_cp_editar.html",{'cp': codigo, 'tipo':2})
        else:
            # Lista vacia
            productos = []  
            return HttpResponse("5")
        



def guarda_editar_perfil(request):
    id_usu = request.POST['id_usu']
    uuid_usu = request.POST['uuid_usu']
    nombre = request.POST['nombre']
    apellidos = request.POST['apellidos']
    fecha_nac = request.POST['fecha_nac']
    tel = request.POST['tel']
    genero = request.POST['genero']
    civil = request.POST['civil']
    pais = request.POST['pais']

    if(pais == '108'):
        cod_postal_api = request.POST['cod_postal']
        estado_api = request.POST['estado_api']
        muni_api = request.POST['muni_api']
        colonias_select_api = request.POST['colonias_select_api']
        municipio_select = 0

        _datos_api = datos_api_cp.objects.get(fk_cod_postal_id = id_usu)

        _datos_api.codigo_postal_api = cod_postal_api
        _datos_api.estado_api = estado_api
        _datos_api.municipio_api = muni_api
        _datos_api.colonia_api = colonias_select_api

        _datos_api.save()
        
    else:
        cod_postal_api = 0
        estado_select = request.POST['estado_select']
        municipio_select = request.POST['municipio_select']

    

    _usuario = usuarios.objects.get(id_usuarios=id_usu)

    #utilizar este codigo ppara decir que un campo no esta vacio
    if request.FILES.get('foto'):
        foto = request.FILES['foto']
    else:  
        foto = _usuario.foto
        



    _usuario.nombre = nombre
    _usuario.apellidos = apellidos
    _usuario.fecha_nac = fecha_nac
    _usuario.sexo = genero
    _usuario.telefono = tel
    _usuario.estado_civil = civil
    _usuario.foto = foto
    _usuario.fk_municipios = municipio_select
    _usuario.fk_cod_postal = cod_postal_api

    _usuario.save()


    usuario = sesiones.objects.filter(uuid_sesion = request.session['usu_uuid'])

    usuario = usuario.get()    

    return render(request,"perfil/perfil.html", {'usuario': usuario})




# =============================== PARA LA MODIFICACION DE USUARIO =============================================

def editar_usuario(request,uuid):

    _sesion = sesiones.objects.get(uuid_sesion = request.session['usu_uuid'])    

    return render(request,"usuario/usuario.html", {'sesion': _sesion})

def busca_usuario_editar(request):
    usu = request.POST['usuario']

    _usuarios = sesiones.objects.filter(usuario_sesion = usu).count()
    
    if (_usuarios > 0):
        return HttpResponse("Error el usuario %s " %usu  + " ya existe" )
    else:
        return HttpResponse("")



def busca_correo_editar(request):
    mail = request.POST['correo']

    _correo = sesiones.objects.filter(correo = mail).count()
    
    if (_correo > 0):
        return HttpResponse("Error el correo %s " %mail  + " ya existe" )
    else:
        return HttpResponse("")
    


def guarda_edit_usuario(request):
    id_sesion = request.POST['id_sesion']
    uuid_sesion = request.POST['uuid_sesion']
    correo = request.POST['correo']
    usuario = request.POST['usuario']


    _sesion = sesiones.objects.get(id_sesion = id_sesion)

    if request.POST.get('cambia_contra'): 
        nueva_contra = request.POST['nueva_contra']
        confirm_new_contra = request.POST['confirm_new_contra']

        #colocamos encode a la contraseña del input
        contra_bytes = nueva_contra.encode("utf-8")
        pass_encry = bcrypt.gensalt()

        pass_en = bcrypt.hashpw(contra_bytes, pass_encry)

        #esta linea se ocupa para que mi contraseña no se guarde en la bd como b'contraseña' y se guarde como 'contraseña' 
        pass_decode = pass_en.decode("utf-8")

        _restablece = restablecer_contras.objects.filter(fk_sesion_id = id_sesion).order_by('-id_restablece')[:1]
        _restablece = _restablece.get()


        _restablece.activa = 'NO'
        _restablece.bandera = 2
        _restablece.save()

        restablecer_contras.objects.create(
            contra_anterior = pass_decode,
            activa = 'SI',
            fk_sesion_id = id_sesion,
            bandera = 1,
            bandera2 = 0,
        )

    else: 
        pass_decode = _sesion.contra
    
    

    _sesion.correo = correo
    _sesion.usuario_sesion = usuario
    _sesion.contra = pass_decode
    _sesion.save()
    
    return redirect('perfil')








