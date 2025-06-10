$(document).ready(function () {

    $('#pais').select2({
        theme: "bootstrap-5",
        placeholder: $(this).data('placeholder'),
    });

    // var cp = $("#cod_postal").val();

    /* if(cp == null){
        $("#div_estado").prop("hidden", false);
        $("#div_mun").prop("hidden", false);
        $("#div_cp").prop("hidden", true);
        $("#datos_api").prop("hidden", true);
        $(".cp_api").remove();
        pais = $("#pais").val();

        $("#div_estado").find('option:contains("Seleccionar")').prop('selected', true);
        $("#div_mun").find('option:contains("Seleccionar")').prop('selected', true);

        var data = { id_pais: pais, 'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val() }


        $.post("../consulta_estados_editar/", data, function (res) {
            console.log(res)
            $("#div_estado").html(res)
        });

    }else{
        if (cp.length == 5) {
            $.post("../consulta_cp_editar/", {cp:cp, 'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val(), tipo: 1}, function (res) {
                console.log(res)       
                
                if(res != 5){
                    $("#datos_api").prop("hidden", false);
                    $(".cp_api").remove();
                    $("#datos_api").replaceWith(res);
                    $("#div_cp").prop("hidden", true);
                    $("#sin_api").prop("hidden", true);
                }else{
                    $("#sin_api").prop("hidden", false);
                    $("#sin_api").html("<h1>"+ res +"</h1>")
                }
                    
            });
        }
    } */

    $("#pais").change(function (e) {
        var pais = $(this).val();
        if (pais == 108) {
            console.log("es mexico");
            $("#div_cp_api").prop("hidden", false);
            $("#div_estado_api").prop("hidden", false);
            $("#div_mun_api").prop("hidden", false);
            $("#div_colonia_api").prop("hidden", false);
            $("#div_estado").prop("hidden", true);
            $("#div_mun").prop("hidden", true);
        } else {
            $("#div_estado").prop("hidden", false);
            $("#div_mun").prop("hidden", false);
            $("#div_cp_api").prop("hidden", true);
            $("#datos_api").prop("hidden", true);
            $(".cp_api").hide();

            $("#div_estado").find('option:contains("Seleccionar")').prop('selected', true);
            $("#div_mun").find('option:contains("Seleccionar")').prop('selected', true);

            var data = { id_pais: pais, 'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val() }


            $.post("../consulta_estados_editar/", data, function (res) {
                console.log(res)
                $("#div_estado").html(res)
            });
        }
    });


    $(document).on("change", "#estado_select", function (e) {
        var estado = $(this).val();

        var data = { id_estado: estado, 'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val() }


        $.post("../consulta_municipios_editar/", data, function (res) {
            console.log(res)
            $("#div_mun").html(res);
            $("#muni_modal").val('');
        });
    });

    $("#guardar_mod_estado").click(function (e) {
        var id_pais = $("#pais").val();
        var estado = $("#estado_mod").val();


        var data = { id_pais: id_pais, estado: estado, 'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val() }


        $.post("../alta_estado_mod_editar/", data, function (res) {
            console.log(res)
            $("#div_estado").html(res);
            $("#estado_mod").val('');
        });
    });


    $("#guardar_mod_municipio").click(function (e) {
        var id_estado = $("#estado_select").val();
        var municipio = $("#muni_modal").val();


        var data = { id_estado: id_estado, municipio: municipio, 'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val() }


        $.post("../alta_municipio_mod_editar/", data, function (res) {
            console.log(res)
            $("#div_mun").html(res);
            $("#muni_modal").val('');
        });
    });

    $(document).on('focusout','#cod_postal',function () {
        var cp = $("#cod_postal").val();

        if (cp.length == 5) {
            $.post("../consulta_cp_editar/", {cp:cp, 'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val(),tipo: 2}, function (res) {
                console.log(res)       
                
                if(res != 5){
                    $("#datos_api").prop("hidden", false);
                    // $("#datos_api").html(res);
                    $(".cp_api").remove();
                    $("#datos_api").replaceWith(res);
                    $("#div_cp").prop("hidden", true);
                    $("#sin_api").prop("hidden", true);
                }else{
                    $("#sin_api").prop("hidden", false);
                    $("#sin_api").html("<h4 style='color:red;'>Sin datos del codigo postal, favor de escribir uno diferente</h4>")
                }
            });
        }
    
    });



    // cuando se le de click al boton de archivo orden compra realiza lo siguiente
    $("#foto").click(function(){
        
        // cuando el documento cambie realice la funcion
        document.getElementById('foto').onchange = function () {

            pdffile=document.getElementById("foto").files[0];// obtenemos el documento seleccionado
            pdffile_url=URL.createObjectURL(pdffile); // ponemos la url del archivo             
            foc = document.getElementById('foto').files[0].name;   // obtenernos el nombre del archivo subido

            // funcion para saber que extension tiene el documento.
            function getFileExtension2(filename) {
                return (/[.]/.exec(filename)) ? /[^.]+$/.exec(filename)[0] : undefined;
            }

            // obtenemos el valor de la extension del archivo
            var d_oc  = getFileExtension2(foc);

            console.log(d_oc);

            //condicion de que si el archivo es pdf de la oc se muestre en el iframe
            if (d_oc == 'pdf' || d_oc== 'PDF' || d_oc== 'JPG' || d_oc== 'jpg' || d_oc== 'PNG' || d_oc== 'png'){
                /// para colocar la url en nuestro iframe
                $('#foto_img').attr('src',pdffile_url);  
            }

        }   // fin funcion cuando el archivo cambie
            
    }); /// fin click al boton archivo orden compra
   


});