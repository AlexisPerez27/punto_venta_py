
$(document).ready(function () {
    $(document).on("click",".select_prod", function () {
        var id_prod = $(this).parents("tr").find("td:eq(0)").text();
        var csrfmiddlewaretoken =  $("input[name=csrfmiddlewaretoken]").val()

        $.post("../carga_datos_list/", {id_prod:id_prod, csrfmiddlewaretoken:csrfmiddlewaretoken}, function (data) {
            console.log(data);
            $("#datos_det").html(data);
        });
    });

    $(document).on("click",".boton_acordeon", function () {
        

        if($(this).find("#icon_boton_acordeon").hasClass("fa-chevron-down")){

            $(this).find("#icon_boton_acordeon").removeClass("fa-chevron-down");
            $(this).find("#icon_boton_acordeon").addClass("fa-chevron-up");
            
        }else{
            
            $(this).find("#icon_boton_acordeon").removeClass("fa-chevron-up");
            $(this).find("#icon_boton_acordeon").addClass("fa-chevron-down");
        }
        
    });


    $(document).on("focusout","input[name=cantidad]", function () {
        if($(this).val() > 1000){
            $(this).val("1000")
        }
    });


    $("#guarda_inventario").click(function (e) { 
        $(".datos_cantidad tr").each(function (index, element) {

            var cantidad2 = $(this).find("input[name=cantidad]").val();

            if(cantidad2 > 0){
                var datos = {
                    id_det_prod :$(this).find("td:eq(0)").text(),
                    cantidad : $(this).find("input[name=cantidad]").val(),
                    tipo_inv : $(this).find("input[name=tipo_inv]").val(),
                    csrfmiddlewaretoken :  $("input[name=csrfmiddlewaretoken]").val(),
                }

                console.log(datos)
                
                $.post("../guarda_inventario/", datos,function (data) {
                    console.log(data)
                });

            }else{
                var datos = {
                    id_det_prod :$(this).find("td:eq(0)").text(),
                    cantidad : $(this).find("input[name=cantidad]").val(),
                    tipo_inv : $(this).find("input[name=tipo_inv]").val(),
                    csrfmiddlewaretoken :  $("input[name=csrfmiddlewaretoken]").val(),
                }

                console.log(datos)
                
                $.post("../guarda_inventario/", datos,function (data) {
                    console.log(data)
                });
                console.log("no se modifico cantidad")
            }
                        
        });


        // desabilitamos boton de publicar 
        $("#guarda_inventario").prop("disabled",true);

        // cargamos el modal de proreso
        $("#modal_progre").load("../carga_modal_progre/");

        // colocamos que espere dos segundos para ejecutar funcion modal_agrega_ord
        setTimeout(modal_progres, 500);

        function modal_progres(){
            console.log("ayuda")
            $('#modal_progreso').modal("show");// mostramos la ventana modal
        }
        
    });




    $("#buscar").keyup(function() {
        var rex = new RegExp($(this).val(), 'i');
        $(".productos_det tr").hide();
        $(".productos_det tr").filter(function() {
            return rex.test($(this).text());
        }).show();
    });
});