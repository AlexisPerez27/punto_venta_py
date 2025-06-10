$(document).ready(function () {

    $("#success-alert").fadeTo(5000, 500).slideUp(500, function(){
        $("#success-alert").slideUp(500);
    });

    $("#validar").click(function (e) {
        var codigo = $("#codigo").val();

        $("#success-alert").fadeTo(5000, 500).slideUp(500, function(){
            $("#success-alert").slideDown(500);
        });

        

        $.post("../busca_correo/", { codigo: codigo, 'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val() }, function (data) {

            console.log(data)

            if(data == 5){
                $("#msj").prop("hidden",false);
                $("#mjs_txt").html("<h4>El codigo proprocionado <strong> "+codigo+" </strong> es incorrecto<h4>");
            }else{
                $("#datos_admin").html(data)
            }            
            
        });

        /* $.post("busca_codigo/", { codigo: codigo, 'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val() }, function (data) {

            if(data == 5){
                $("#msj").prop("hidden",false);
                $("#mjs_txt").html("<h4>El codigo proprocionado <strong> "+codigo+" </strong> es incorrecto<h4>");
            }else{
                $("#datos_admin").html(data)
            }            
            
        }); */
    });


    /* $(document).on("click","#ingresar",function (e) {
        var correo = $("#correo").val();

        $.post("busca_correo/", { correo: correo, 'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val() }, function (data) {

            console.log(data)

            if(data == 5){
                $("#msj").prop("hidden",false);
                $("#mjs_txt").html("<h4>El Correo proprocionado <strong> "+correo+" </strong> no se encuentra en la base de datos<h4>");
            }else{
                $("#datos_admin").html(data)
            }            
            
        });
    }); */
});