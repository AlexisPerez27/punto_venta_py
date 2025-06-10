from django.shortcuts import render,redirect,get_object_or_404 #importamos funciones de operacion para django
from django.http import HttpResponse, JsonResponse #para mostrar mensajes o resultados en la pagina
from .models import codigos
from ..loggin import models as model_loggin
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
#para correo
from django.core.mail import EmailMessage, EmailMultiAlternatives 
from django.template.loader import render_to_string
from django.conf import settings


#para mensajes whats
# import pywhatkit #es necesario tener whatsappweb
# Create your views here.


def admin(request):
    return render(request,"admin/dashboard.html")


# =============================================== para la solicitud de administrador =============================================================================
def inicio_admin(request):
    # pywhatkit.sendwhatmsg_instantly("+527229102777", "Hola") #es neceario whatsapp web

    _sesion = model_loggin.sesiones.objects.get(uuid_sesion = request.session['usu_uuid'])

    correo = _sesion.correo

    _codigos = codigos.objects.filter(Q(activo = 5) | Q(activo = 0)).order_by('id_codigo')[:1]
    _codigos = _codigos.get()

    cod = _codigos.codigo

    cod_activo = _codigos.activo
    


    if cod_activo == 0:
        _codigos.activo = 5
        _codigos.updated_at = timezone.now()
        _codigos.save()

        template = render_to_string('correo/correo_codigo.html',{'correo': correo,'codigo':cod})


        #PARA CORREO CON FORMATO HTML   
        subject = "Codigo para activacion de cuenta administrador"
        from_email = "al221611668@gmail.com"
        to = correo
        text_content = template
        html_content = template
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        # msg.attach_file("../media/fondos/img3.webp")
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        messages.error(request,'Se te ha enviado un mensaje al correo %s para que continues con los pasos a seguir'%correo)

        return render(request,"inicio_admin.html")

    elif cod_activo == 5: 

        fecha = _codigos.updated_at

        #dividimos la fecha en un array donde encuentre la cadena +
        fecha = str(fecha).split("+")
        fecha2 = str(fecha[0]).split(".")

        # Convertir la fecha de la base de datos (suponiendo que está en formato 'YYYY-MM-DD HH:MM:SS')
        fecha_objeto = datetime.strptime(fecha2[0], '%Y-%m-%d %H:%M:%S')

        # Sumar 30 minutos a la fecha
        nueva_fecha = fecha_objeto + timedelta(minutes=1)

        ahora = timezone.now()

        fecha_actual = str(ahora).split("+")
        fecha_actual2 = str(fecha_actual[0]).split(".")

        # Convertir la fecha de la base de datos (suponiendo que está en formato 'YYYY-MM-DD HH:MM:SS')
        f_actual = datetime.strptime(fecha_actual2[0], '%Y-%m-%d %H:%M:%S')

        # return HttpResponse("fecha actual %s" %f_actual )

        tiempo_res = nueva_fecha -  f_actual

        if f_actual < nueva_fecha:

            messages.error(request,f'Tienes 10 Minutos para colocar el codigo que recibiste en tu correo: %s, \n tiempo restante %s'%(correo,tiempo_res))

            return render(request,"inicio_admin.html") 

        else:

            _codigos.activo = 2
            _codigos.updated_at = timezone.now()
            _codigos.save()

            return redirect("../solicita/") 
    

def busca_codigo(request):
    codigo = request.POST['codigo']

    _codigo = codigos.objects.filter(Q(codigo = codigo),Q(activo = 0))

    _count_cod = _codigo.count()

    if _count_cod == 1 :
        _cod = _codigo.get()  
        _cod.activo = 1;
        _cod.save()

        return render(request,"datos_info_admin.html")
    
    else:
        return HttpResponse('5')
        # return HttpResponse('<h4>El codigo proprocionado <strong> %s </strong> es incorrecto<h4>' %codigo)


def busca_correo(request):
    # correo = request.POST['correo']

    _sesion = model_loggin.sesiones.objects.get(uuid_sesion = request.session['usu_uuid'])

    correo = _sesion.correo
    user = _sesion.usuario_sesion
    uuid_sesion = _sesion.uuid_sesion

    codigo = request.POST['codigo']

    _codigo = codigos.objects.filter(Q(codigo = codigo),Q(activo = 5))

    _count_cod = _codigo.count()

    if _count_cod == 1 :
        _cod = _codigo.get()  
        _cod.activo = 1;
        _cod.save()

        _correo = model_loggin.sesiones.objects.filter(correo = correo)
        _count_correo = _correo.count()    

        if _count_correo == 1 : 
            template = render_to_string('correo/correo.html',{'correo': correo, 'usuario':user, 'uuid_sesion': uuid_sesion })


            #PARA CORREO CON FORMATO HTML   
            subject = "Solicitud de activacion de cuenta administrador"
            from_email = "alexis.perez@extralsa.com.mx"
            to = correo
            text_content = template
            html_content = template
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            # msg.attach_file("../media/fondos/img3.webp")
            msg.attach_alternative(html_content, "text/html")
            msg.send()


            
            # PARA CORREOS SIN FORMATO HTML
            # email = EmailMessage(
            #     'Solicitud de activacion de cuenta administrador',
            #     template, #hoja donde se muestra el contenido del correo
            #     settings.EMAIL_HOST_USER,  #configuracion del host 
            #     [correo] #el mail hacia donde se enviara el correo
            # )


            # email.fail_silently = False
            # email.send()


            return render(request,"info_correo.html")
        else:
            return HttpResponse("5")

        # return render(request,"datos_info_admin.html")
    
    else:
        return HttpResponse('')
    


def valida_admin(request,uuid):

    _sesion = model_loggin.sesiones.objects.get(uuid_sesion = uuid)

    correo = _sesion.correo
    user = _sesion.usuario_sesion

    
    return render(request,'verificacion.html', {'correo':correo,'user':user, 'uuid_sesion':uuid})


def actualizar_admin(request,uuid):
    _sesion = model_loggin.sesiones.objects.get(uuid_sesion = uuid)

    _sesion.fk_permisos_id = 2
    _sesion.updated_at = timezone.now()
    _sesion.save()

    return redirect("/")
    # return HttpResponse("acepta ser administrador %s" %uuid)

   

