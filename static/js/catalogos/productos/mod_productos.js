$(document).ready(function () {

    // ============================= para guardar nuevo prod en modificacion ==================================================================================
    $("#add_det_prod").click(function (e) { 
        if($("#add_det_prod").is(":checked")){
            $("#row_add_new_det").prop("hidden",false);
        }else{
            $("#row_add_new_det").prop("hidden",true);
        }
    });

    $("#guarda_mod_prod").click(function (e) { 
        var datos = {
            tipo_opcion : $("#tipo_opcion").val(),
            id_prod : $("#id_prod").val(),
            nom_prod : $("#nom_prod").val(),
            descripcion : $("#descripcion").val(),
            precio : $("#precio").val(),
            csrfmiddlewaretoken :  $("input[name=csrfmiddlewaretoken]").val(),
        }

        $.post("../guarda_mod_det_prod/", datos,function (data) {
            console.log(data)
            location.href = "/../productos/"
        });


        
    });

    $("#add_det_prod_mod").click(function (e) { 


        var id_seccion_val = $("#seccion").val();
        var id_tipo_val = $("#tipo").val();
        var id_color_val = $("#color").val();

        var id_tallas = [];

        $("input[name=talla]:checked").each(function() {
            var id_talla = $(this).val();
            id_tallas.push(id_talla)
        });

        if(id_seccion_val == 0 || id_tipo_val == 0 || id_color_val == 0 || id_tallas == ""){

            Swal.fire({
                title: "Valor no seleccionado",
                text: "Favor de seleccionar los campos, ya que no pueden ir vacios",
                icon: "error"
            });

        }else{            
            
            var id_prod = $("#id_prod").val();
            var id_seccion = $("#seccion").val();
            var id_tipo = $("#tipo").val();
            var id_color = $("#color").val();
            var id_tallas = id_tallas;
            var images = $("[name=images]")[0].files;
            
            var tipo_opcion = 2;
            var csrfmiddlewaretoken =  $("input[name=csrfmiddlewaretoken]").val();


            var formData = new FormData();
            formData.append('id_prod', id_prod);
            formData.append('id_seccion', id_seccion);
            formData.append('id_tipo', id_tipo);
            formData.append('id_color', id_color);
            formData.append('id_tallas', id_tallas);     
            formData.append('tipo_opcion', tipo_opcion);      
            formData.append('csrfmiddlewaretoken', csrfmiddlewaretoken);

            // Agregar los archivos de un filemultiple a FormData
            $.each(images, function(i, images) {
                formData.append('images', images);
            });

            console.log(images)

            $.ajax({
                async: false,
                type: 'POST',
                data: formData,
                url: '../guarda_mod_det_prod/',
                cache: false,
                contentType: false,
                processData: false,
                success: function (data) {
                    //console.log(formData.get("partida"));
                    console.log(data);
                    $("#datos_prod").html(data)
                }
            });
        }

        
    });

    // ============================= para modificar y cancelar la edicion de la seccion ==================================================================================
    $(document).on("click",".mod_seccion",function (e) { 
        var dato = $(this).parent("td").text().trim();
        // variable donde guardo la ruta 
        var url = "../consulta_listas/1/"+dato;
        // codificamos la ruta para los espacios se coloquen como %20
        url = encodeURI(url);
        // cargamos ruta
        $(this).parent("td").load(url);
    });


    $(document).on("click",".cancelar_mod_seccion",function (e) { 
        var dato = $(this).parents("td").find("#dato").text();
        $(this).parents("td").replaceWith("<td>"+dato+" <a title='modificar' class='link-info mod_seccion'><i class='fa-solid fa-pen-to-square'></i></a></td>");
    });

    $(document).on("click",".guardar_mod_seccion",function (e) {
        var id_sec_selec = $(this).parents("td").find("#seccion :selected").val();

        if (id_sec_selec == 0){
            Swal.fire({
                title: "Valor no seleccionado",
                text: "Favor de seleccionar algun dato",
                icon: "error"
            });
        }else{
            var datos = {
                new_id_seccion  : $(this).parents("td").find("#seccion :selected").val(),
                uuid_prod       : $("#uuid_prod").val(),
                id_producto     : $(this).parents("tr").find("td:eq(0)").text(),
                id_seccion      : $(this).parents("tr").find("td:eq(5)").text(),
                id_tipo         : $(this).parents("tr").find("td:eq(7)").text(),
                id_color        : $(this).parents("tr").find("td:eq(9)").text(),
                tipo            : 1,
                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
            }
    
            $.post("../guarda_lista/", datos,function (data) {
                console.log(data)
                location.reload()
            });
        }
        
        
    });


    // ============================= para modificar y cancelar la edicion de la tipo ==================================================================================
    $(document).on("click",".mod_tipo",function (e) { 
        var dato = $(this).parent("td").text().trim();
        $(this).parent("td").load("../consulta_listas/2/"+dato);
    });

    $(document).on("click",".cancelar_mod_tipo",function (e) { 
        var dato = $(this).parents("td").find("#dato").text();
        $(this).parents("td").replaceWith("<td>"+dato+" <a title='modificar' class='link-info mod_tipo'><i class='fa-solid fa-pen-to-square'></i></a></td>");
    });


    $(document).on("click",".guardar_mod_tipo",function (e) {
        var id_tipo_selec = $(this).parents("td").find("#tipo :selected").val();

        if (id_tipo_selec == 0){
            Swal.fire({
                title: "Valor no seleccionado",
                text: "Favor de seleccionar algun dato",
                icon: "error"
            });
        }else{
            var datos = {
                new_id_tipo : $(this).parents("td").find("#tipo :selected").val(),
                uuid_prod       : $("#uuid_prod").val(),
                id_producto     : $(this).parents("tr").find("td:eq(0)").text(),
                id_seccion      : $(this).parents("tr").find("td:eq(5)").text(),
                id_tipo         : $(this).parents("tr").find("td:eq(7)").text(),
                id_color        : $(this).parents("tr").find("td:eq(9)").text(),
                tipo            : 2,
                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
            }
    
            $.post("../guarda_lista/", datos,function (data) {
                console.log(data)
                location.reload()
            });
        }
        
    });



    // ============================= para modificar y cancelar la edicion de la color ==================================================================================
    $(document).on("click",".mod_color",function (e) { 
        var dato = $(this).parent("td").text().trim();
        $(this).parent("td").load("../consulta_listas/3/"+dato);
    });

    $(document).on("click",".cancelar_mod_color",function (e) { 
        var dato = $(this).parents("td").find("#dato").text();
        $(this).parents("td").replaceWith("<td>"+dato+" <a title='modificar' class='link-info mod_color'><i class='fa-solid fa-pen-to-square'></i></a></td>");
    });

    $(document).on("click",".guardar_mod_color",function (e) {
        var id_color_selec = $(this).parents("td").find("#color :selected").val();

        if (id_color_selec == 0){
            Swal.fire({
                title: "Valor no seleccionado",
                text: "Favor de seleccionar algun dato",
                icon: "error"
            });
        }else{
            var datos = {
                new_id_color : $(this).parents("td").find("#color :selected").val(),
                uuid_prod       : $("#uuid_prod").val(),
                id_producto     : $(this).parents("tr").find("td:eq(0)").text(),
                id_seccion      : $(this).parents("tr").find("td:eq(5)").text(),
                id_tipo         : $(this).parents("tr").find("td:eq(7)").text(),
                id_color        : $(this).parents("tr").find("td:eq(9)").text(),
                tipo            : 3,
                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
            }
    
            $.post("../guarda_lista/", datos,function (data) {
                console.log(data)

                if(data == 1){
                    Swal.fire({
                        title: "Color ya existe en el producto",
                        text: "El color seleccionado ya existe en el producto.",
                        icon: "error"
                    });
                }else{
                    location.reload()
                }
                
            });
        }
        
    });


    // ========================================= para el modal de tallas ====================================
    

    $(document).on("click",".ver_tallas",function(){
        var datos = {
            uuid_prod: $("#uuid_prod").val(),
            id_seccion: $(this).parents("tr").find("td:eq(5)").text(),
            id_tipo: $(this).parents("tr").find("td:eq(7)").text(),
            id_color: $(this).parents("tr").find("td:eq(9)").text(),
            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
        }

        $.post("../modal_tallas/", datos,function (data) {
            console.log(data)
            $(".moda_body_tallas").html(data);  
            $(".mod_tallas").modal("show");  
        });

        
    });


    $(document).on("click","input[name=talla_radio]",function(){
        if($(this).val() == "v"){
            $(".vestimenta").prop("hidden",false);
            $(".calzado").prop("hidden",true);
        }else{
            $(".vestimenta").prop("hidden",true);
            $(".calzado").prop("hidden",false);
        }
    });

    $(document).on("click",".eli_talla", function () {
        var datos = {
            id_det_talla : $(this).parent("td").find("input[name=id_detalle]").val(),
            uuid_prod: $(this).parents("tr").find("td:eq(3)").text(),
            id_seccion: $(this).parents("tr").find("td:eq(4)").text(),
            id_tipo: $(this).parents("tr").find("td:eq(5)").text(),
            id_color: $(this).parents("tr").find("td:eq(6)").text(),
            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
        }
        console.log(datos);

        $.post("../elimina_det_talla/", datos,function (data) {
            console.log(data)
            $(".moda_body_tallas").html(data);  
            $(".mod_tallas").modal("show");  
        });
    });


    $(document).on("click","#add_modal_talla", function () {

        var tallas = []
        $("input[name=talla]:checked").each(function (index) {
            id_ta = $(this).val();

            tallas.push(id_ta)
        });

        var datos = {
            id_color : $(".datos_talla tr:first").find("td:eq(6)").text(),
            id_producto : $(".datos_talla tr:first").find("td:eq(2)").text(),
            uuid_prod : $(".datos_talla tr:first").find("td:eq(3)").text(),
            id_tipo : $(".datos_talla tr:first").find("td:eq(5)").text(),
            id_seccion : $(".datos_talla tr:first").find("td:eq(4)").text(),
            "id_talla[]" : tallas,
            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
        }
        console.log(datos);

        $.post("../agrega_mod_tallas/", datos,function (data) {
            console.log(data)
            $(".moda_body_tallas").html(data);  
            $(".mod_tallas").modal("show");  
        });



    });


    // ========================================= para el modal de imagenes ====================================
    $(document).on("click",".var_images",function(){
        var datos = {
            uuid_prod: $("#uuid_prod").val(),
            id_producto : $(this).parents("tr").find("td:eq(0)").text(),
            id_seccion: $(this).parents("tr").find("td:eq(5)").text(),
            id_tipo: $(this).parents("tr").find("td:eq(7)").text(),
            id_color: $(this).parents("tr").find("td:eq(9)").text(),
            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
        }

        console.log(datos)

        $.post("../modal_imagenes/", datos,function (data) {
            console.log(data)
            $(".modal_body_images").html(data);  
            $(".mod_images").modal("show");  
        });
    });


    $(document).on("click",".eli_images", function () {

        var datos = {
            id_galeria : $(this).parent("div").find("input[name='id_imagen']").val(),
            id_producto : $("#id_prod").val(),
            id_color : $("#id_color").val(),
            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
        }
        

        $.post("../elimina_images/", datos,function (data) {
            console.log(data)
            $(".modal_body_images").html(data);  
            $(".mod_images").modal("show");  
        });
        
    });


    $(document).on("click","#add_img_mod", function () {
        var id_producto  =  $("#id_prod").val();
        var id_color  =  $("#id_color").val();
        var images   =  $("input[name=images_modal]")[0].files; // para archivos multiple;
        var csrfmiddlewaretoken =  $("input[name=csrfmiddlewaretoken]").val();
        
        console.log(images);

        var formData = new FormData();
        formData.append('id_producto', id_producto);
        formData.append('id_color', id_color);
        formData.append('csrfmiddlewaretoken', csrfmiddlewaretoken);

        // Agregar los archivos de un filemultiple a FormData
        $.each(images, function(i, images) {
            formData.append('images', images);
        });


        $.ajax({
            async: false,
            type: 'POST',
            data: formData,
            url: '../agrega_imagen_modal/',
            cache: false,
            contentType: false,
            processData: false,
            success: function (data) {
                //console.log(formData.get("partida"));
                console.log(data);

                $(".modal_body_images").html(data);  
                $(".mod_images").modal("show");  
            }
        });
        
        
    });



    // ========================================= para eliminar producto ====================================
    $(document).on("click",".eli_prod_mod", function () {
        var datos = {
            id_producto     : $(this).parents("tr").find("td:eq(0)").text(),
            id_seccion      : $(this).parents("tr").find("td:eq(5)").text(),
            id_tipo         : $(this).parents("tr").find("td:eq(7)").text(),
            id_color        : $(this).parents("tr").find("td:eq(9)").text(),
            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
        }
        

        $.post("../elimina_mod_prod/", datos,function (data) {
            console.log(data) 
            location.reload()
        });
    });

});