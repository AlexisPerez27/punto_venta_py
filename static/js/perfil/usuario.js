$(document).ready(function () {
    $("#correo").focusout(function (e) {
        if($(this).val() == ""){
            $("#span_correo").text("El campo Correo no puede ir vacio");
        }else{
            $("#span_correo").text("");

            $.post("../busca_correo_editar/",{correo: $(this).val(), 'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()},function (res) { 
                $("#span_correo").text(res);
            });
        }
    });


    $("#usuario").focusout(function (e) {
        if($(this).val() == ""){
            $("#span_usuario").text("El campo Usuario no puede ir vacio");
        }else{
            $("#span_usuario").text("");

            $.post("../busca_usuario_editar/",{usuario: $(this).val(), 'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()},function (res) { 
                $("#span_usuario").text(res);
            });
        }
    });

    $("#cambia_contra").click(function () { 
        if($("#cambia_contra").is(":checked")){
            $("#nueva_contra").prop("readonly",false);
            $("#confirm_new_contra").prop("readonly",false);
        }else{
            $("#nueva_contra").prop("readonly",true);
            $("#confirm_new_contra").prop("readonly",true);
        }
    });


    $('#nueva_contra').popover({
        placement: 'bottom',
        container: 'body',
        html: true,
        content: function () {
            return $('.popover').html();
        },
        title: function () {
            return $('.popover_title').html();
        },
    });

    $('#confirm_new_contra').popover({
        placement: 'bottom',
        container: 'body',
        html: true,
        content: function () {
            return $('.popover-confirm').html();
        },
        title: function () {
            return $('.popover_title').html();
        },
    });


    $("#nueva_contra").focusout(function (e) {
        if($(this).val() == ""){
            $("#span_pass").text("El campo Contraseña no puede ir vacio");
        }else{
            $("#span_pass").text("");
        }
    });


    $("#confirm_new_contra").focusout(function (e) {
        if($(this).val() == ""){
            $("#span_pass_confirm").text("El campo Contraseña no puede ir vacio");
        }else{
            $("#span_pass_confirm").text("");

            var pass = $("#nueva_contra").val();

            if(pass != $(this).val()){
                $("#span_pass_confirm").text("Las contraseñas deven coincidir");
            }else{
                $("#span_pass_confirm").text("");
            }
        }
    });
});