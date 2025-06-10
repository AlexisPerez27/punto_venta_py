$(document).ready(function () {

    // ========================================= para el modal de seccion ====================================
    $("#div_modal_seccion").load("../carga_modal_seccion/");

    $("#add_seccion_prod").click(function(){
        $(".seccion").modal("show");
    });

    $(document).on("click","#guarda_seccion_modal",function (e) {
        $.post("../guarda_modal_seccion/", $("#form_seccion_modal").serialize(), function(data){
            console.log(data);
            $("#seccion_prod").html(data);
        });
    });



    // ========================================= para el modal de tipo ====================================
    $("#div_modal_tipo").load("../carga_modal_tipo/");

    $("#add_tipo_prod").click(function(){
        $(".tipo").modal("show");
    });

    $(document).on("click","#guarda_tipo_modal",function (e) {
        $.post("../guarda_modal_tipo/", $("#form_tipo_modal").serialize(), function(data){
            console.log(data);
            $("#tipo_prod").html(data);
        });
    });



    // ================================== combos dinamicos ================================================
    $("#tipo_prod").change(function(){
        var datos = {
            tipo : $(this).val(),
            'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
        }

        $.post("../busca_color/", datos,function (data) {
            console.log(data);
            $("#color").html(data)
        });
    });


    $("#color").change(function(){
        var datos_talla = {            
            tipo : $("#tipo_prod option:selected").val(),
            color : $(this).val(),
            'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
        }

        $.post("../busca_talla/", datos_talla,function (data) {
            console.log(data);
            $("#talla").html(data)
        });
    });


    $("#color_mod").change(function(){
        var datos_talla = {
            tipo : $("#tipo_prod option:selected").val(),
            color : $("#color_mod option:selected").text(),
            'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
        }

        $.post("../busca_talla_mod/", datos_talla,function (data) {
            console.log(data);
            $("#talla").html(data);
        });
    });



    $(document).on('click','input[name=tipo_talla]',function (e){
        if($(this).is(":checked")){
            var radio = $(this).val();

            console.log(radio);

            if(radio =="calzado"){
                $("#tamaño_vestimenta").prop("hidden",true);
                $("#tamaño_calzado").prop("hidden",false);
            }else{
                $("#tamaño_vestimenta").prop("hidden",false);
                $("#tamaño_calzado").prop("hidden",true);
            }
        }
    });


    $(document).on("click",".elim_img",function(e){

        var datos_img = {
            id_img : $(this).parent("div").find("input[name=id_img]").val(),
            id_prod : $("#id_prod").val(),
            uuid_prod : $("#uuid_prod").val(),
            'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val(),
        }

        $.post("../elimina_img/", datos_img,function (data) {
            console.log(data)            
            $("#galeria").html(data)
        });
        
        
    });
});