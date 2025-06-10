$(document).ready(function () {
    $('#pass').popover({
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

    $('#pass_confirm').popover({
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

    $('#pais').select2({
        theme: "bootstrap-5",
        placeholder: $(this).data('placeholder'),
    });


    $("#pais").change(function (e) {
        var pais = $(this).val();

        if (pais == 108) {
            console.log("es mexico");
            $("#div_estado").prop("hidden", true);
            $("#div_mun").prop("hidden", true);
            $("#div_cp").prop("hidden", false);
        } else {
            $("#div_estado").prop("hidden", false);
            $("#div_mun").prop("hidden", false);
            $("#div_cp").prop("hidden", true);
            $("#datos_api").prop("hidden", true);

            $("#div_estado").find('option:contains("Seleccionar")').prop('selected', true);
            $("#div_mun").find('option:contains("Seleccionar")').prop('selected', true);

            var data = { id_pais: pais, 'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val() }


            $.post("../consulta_estados/", data, function (res) {
                console.log(res)
                $("#div_estado").html(res)
            });
        }
    });


    $("#guardar_mod_estado").click(function (e) {
        var id_pais = $("#pais").val();
        var estado = $("#estado_mod").val();


        var data = { id_pais: id_pais, estado: estado, 'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val() }


        $.post("../alta_estado_mod/", data, function (res) {
            console.log(res)
            $("#div_estado").html(res);
            $("#estado_mod").val('');
        });
    });



    $(document).on("change", "#estado_select", function (e) {
        var estado = $(this).val();

        var data = { id_estado: estado, 'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val() }


        $.post("../consulta_municipios/", data, function (res) {
            console.log(res)
            $("#div_mun").html(res);
            $("#muni_modal").val('');
        });
    });


    $("#guardar_mod_municipio").click(function (e) {
        var id_estado = $("#estado_select").val();
        var municipio = $("#muni_modal").val();


        var data = { id_estado: id_estado, municipio: municipio, 'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val() }


        $.post("../alta_municipio_mod/", data, function (res) {
            console.log(res)
            $("#div_mun").html(res);
            $("#muni_modal").val('');
        });
    });


    $(document).on('keyup','#cod_postal',function (e) {
        var cp = $(this).val();

        if (cp.length == 5) {
            $.post("../consulta_cp/", {cp:cp, 'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()}, function (res) {
                console.log(res)                
                $("#datos_api").prop("hidden", false);
                $("#datos_api").html(res);
            });
        }
    });



    // ====================================================================================================================
    // =
    // =
    // =                       VALIDACIONES
    // =
    // =
    // ====================================================================================================================


    $("#nombre").focusout(function (e) { 
        if($(this).val() == ""){
            $("#span_nombre").text("El campo Nombre no puede ir vacio");
        }else{
            $("#span_nombre").text("");
        }
    });


    $("#apellidos").focusout(function (e) { 
        if($(this).val() == ""){
            $("#span_apellidos").text("El campo Apellidos no puede ir vacio");
        }else{
            $("#span_apellidos").text("");
        }
    });


    $("#fecha_nac").focusout(function (e) { 
        if($(this).val() == ""){
            $("#span_fecha").text("El campo Fecha Nacimiento no puede ir vacio");
        }else{
            $("#span_fecha").text("");
        }
    });


    $("#telefono").focusout(function (e) { 
        if($(this).val() == ""){
            $("#span_tel").text("El campo Telefono no puede ir vacio");
        }else{
            $("#span_tel").text("");

            if($(this).val().length < 10){            
                $("#span_tel").text("El campo Telefono no puede ser menor a 10 digitos");
            }else{
                $("#span_tel").text("");
            }
        }        
    });


    $("#civil").focusout(function (e) { 
        if($(this).val() == 0){
            $("#span_civil").text("El campo Estado Civil no puede ir vacio");
        }else{
            $("#span_civil").text("");
        }
    });

    $(".select2").focusout(function (e) {
        var pais = $(".pais").val();

        if(pais == 0){
            $("#span_pais").text("El campo Pais no puede ir vacio");
        }else{
            $("#span_pais").text("");
        }
    });


    $("#cod_postal").focusout(function (e) { 
        if($(this).val() == ""){
            $("#span_postal").text("El campo Codigo Postal no puede ir vacio");
        }else{
            $("#span_postal").text("");
        }
    });


    $(document).on("focusout","#colonias_select_api",function (e) { 
        if($(this).val() == 0){
            $("#span_colonias").text("El campo Colonias no puede ir vacio");
        }else{
            $("#span_colonias").text("");
        }
    });


    $(document).on("focusout","#estado_select",function (e) { 
        if($(this).val() == 0){
            $("#span_estados").text("El campo Estado no puede ir vacio");
        }else{
            $("#span_estados").text("");
        }
    });

    $(document).on("focusout","#municipio_select",function (e) { 
        if($(this).val() == 0){
            $("#span_municipios").text("El campo Municipio no puede ir vacio");
        }else{
            $("#span_municipios").text("");
        }
    });


    $("#correo").focusout(function (e) {
        if($(this).val() == ""){
            $("#span_correo").text("El campo Correo no puede ir vacio");
        }else{
            $("#span_correo").text("");

            $.post("../busca_correo/",{correo: $(this).val(), 'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()},function (res) { 
                $("#span_correo").text(res);
            });
        }
    });


    $("#usuario").focusout(function (e) {



        if($(this).val() == ""){
            $("#span_usuario").text("El campo Usuario no puede ir vacio");
        }else{
            $("#span_usuario").text("");

            $.post("../busca_usuario/",{usuario: $(this).val(), 'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()},function (res) { 
                $("#span_usuario").text(res);
            });
        }
    });


    $("#pass").focusout(function (e) {
        if($(this).val() == ""){
            $("#span_pass").text("El campo Contraseña no puede ir vacio");
        }else{
            $("#span_pass").text("");
        }
    });


    $("#pass_confirm").focusout(function (e) {
        if($(this).val() == ""){
            $("#span_pass_confirm").text("El campo Contraseña no puede ir vacio");
        }else{
            $("#span_pass_confirm").text("");

            var pass = $("#pass").val();

            if(pass != $(this).val()){
                $("#span_pass_confirm").text("Las contraseñas deven coincidir");
            }else{
                $("#span_pass_confirm").text("");
            }
        }
    });


    $("#registrarse").click(function (e) { 
        
        var nombre = $("#nombre").val();
        var apellidos = $("#apellidos").val();
        var fecha_nac = $("#fecha_nac").val();
        var telefono = $("#telefono").val();
        var sexo = $("input[name='sexo']:checked").val();
        var civil = $("#civil").val();
        var pais = $("#pais").val();
        var cod_postal = $("#cod_postal").val();
        var estado_select = $("#estado_select").val();
        var municipio_select = $("#municipio_select").val();
        var correo = $("#correo").val();
        var usuario = $("#usuario").val();
        var pass = $("#pass").val();
        var pass_confirm = $("#pass_confirm").val();

        var datos = {
            nombre : $("#nombre").val(),
            apellidos : $("#apellidos").val(),
            fecha_nac : $("#fecha_nac").val(),
            telefono : $("#telefono").val(),
            sexo : $("input[name='sexo']:checked").val(),
            civil : $("#civil").val(),
            pais : $("#pais").val(),
            cod_postal : $("#cod_postal").val(),
            estado_select : $("#estado_select").val(),
            municipio_select : $("#municipio_select").val(),
            correo : $("#correo").val(),
            usuario : $("#usuario").val(),
            pass : $("#pass").val(),
            pass_confirm : $("#pass_confirm").val(),
        }


        console.log(datos);


        if(nombre == "" || apellidos == "" || fecha_nac == "" || telefono == "" || civil == "0" || pais == "0" ||
           correo == "" || usuario == "" || pass == "" || pass_confirm == "" 
        ){
            console.log("ayuda");

            Swal.fire({
                title: "¡¡¡ ERROR DE DATOS !!!",
                text: "Faltan campos por llenar, favor de verificar informacion.",
                icon: "error"
            });

            $("#span_nombre").text("El campo Nombre no puede ir vacio");
            $("#span_apellidos").text("El campo Apellidos no puede ir vacio");
            $("#span_fecha").text("El campo Fecha Nacimiento no puede ir vacio");
            $("#span_tel").text("El campo Telefono no puede ir vacio");
            $("#span_civil").text("El campo Estado Civil no puede ir vacio");
            $("#span_pais").text("El campo Pais no puede ir vacio");
            $("#span_postal").text("El campo Codigo Postal no puede ir vacio");
            $("#span_colonias").text("El campo Colonias no puede ir vacio");
            $("#span_estados").text("El campo Estado no puede ir vacio");
            $("#span_municipios").text("El campo Municipio no puede ir vacio");
            $("#span_correo").text("El campo Correo no puede ir vacio");
            $("#span_usuario").text("El campo Usuario no puede ir vacio");
            $("#span_pass").text("El campo Contraseña no puede ir vacio");
            $("#span_pass_confirm").text("El campo Contraseña no puede ir vacio");



        }else{
            $("#span_nombre").text("");
            $("#span_apellidos").text("");
            $("#span_fecha").text("");
            $("#span_tel").text("");
            $("#span_civil").text("");
            $("#span_pais").text("");
            $("#span_postal").text("");
            $("#span_colonias").text("");
            $("#span_estados").text("");
            $("#span_municipios").text("");
            $("#span_correo").text("");
            $("#span_usuario").text("");
            $("#span_pass").text("");
            $("#span_pass_confirm").text("");
        }
    });














});