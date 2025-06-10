$(document).ready(function () {
    $("input[name=talla_radio]").click(function(){
        if($(this).val() == "v"){
            $(".vestimenta").prop("hidden",false);
            $(".calzado").prop("hidden",true);
        }else{
            $(".vestimenta").prop("hidden",true);
            $(".calzado").prop("hidden",false);
        }
    });

    $("#add_prod").click(function (e) { 
        var cod_prod = $("#cod_prod").val();
        var producto = $("#nom_prod").val();
        var descripcion = $("#descripcion").val();
        var precio = $("#precio").val();
        var id_seccion = $("#seccion").val();
        var seccion = $("#seccion :selected").text();
        var id_tipo = $("#tipo").val();
        var tipo = $("#tipo :selected").text();
        var id_color = $("#color").val();
        var color = $("#color :selected").text();

        var id_tallas = []
        var tallas = []
        $("input[type=checkbox]:checked").each(function() {
            var id_talla = $(this).val();
            var talla = $(this).parent(".div_check").find(".check_label").text();

            id_tallas.push(id_talla)

            tallas.push(talla)
        });


        if(producto == "" || descripcion == "" || precio == "" || id_seccion == 0 || id_tipo == 0 || id_color == 0 || id_tallas == ""){
            Swal.fire({
                title: "Campos Vacios",
                text: "Favor de completar los campos",
                icon: "error"
            });
        }else{
            var _color = "";
            var count_color = 0;
            $("#datos_prod tr").each(function () {
                _color  = $(this).find("td:eq(9)").text();

                if(_color == color){
                    count_color += 1;
                }
            });

            console.log(count_color);

            if(count_color == 0){
                $("#datos_prod").append("<tr><td>"+cod_prod+"</td><td>"+producto+"</td><td>"+descripcion+"</td><td>"+precio+"</td>"+
                "<td hidden>"+id_seccion+"</td><td>"+seccion+"</td><td hidden>"+id_tipo+"</td><td>"+tipo+"</td><td hidden>"+id_color+"</td><td>"+color+"</td>"+
                "<td hidden>"+id_tallas+"</td><td>"+tallas+"</td><td><div class='input-group mb-3'><span class='input-group-text'><i class='fa-solid fa-images'></i></span>"+
                "<input type='file' name='images' id='images' class='form-control' multiple></div></td><td><button class='btn btn-danger eli_prod'>Eliminar</button></td></tr>");
            }else{
                Swal.fire({
                    title: "Colores Iguales",
                    text: "No se puede agregar producto ya que el color ya se encuentra en la tabla, favor de seleccionar otro.",
                    icon: "error"
                });
            }            
        }        
    });
    
    $(document).on("click",".eli_prod", function () {
        $(this).parents("tr").remove();
    });

    $("#guardar_prod").click(function (e) {
        $("#datos_prod tr").each(function () {
            var cod_prod    = $(this).find("td:eq(0)").text();
            var producto    = $(this).find("td:eq(1)").text();
            var descripcion = $(this).find("td:eq(2)").text();
            var precio      = $(this).find("td:eq(3)").text();
            var id_seccion  = $(this).find("td:eq(4)").text();
            var seccion     = $(this).find("td:eq(5)").text();
            var id_tipo     = $(this).find("td:eq(6)").text();
            var tipo        = $(this).find("td:eq(7)").text();
            var id_color    = $(this).find("td:eq(8)").text();
            var color       = $(this).find("td:eq(9)").text();
            var id_tallas   = $(this).find("td:eq(10)").text();
            var tallas      = $(this).find("td:eq(11)").text();
            var images      = $(this).find("[name=images]")[0].files; // para archivos multiples
            var csrfmiddlewaretoken =  $("input[name=csrfmiddlewaretoken]").val()


            var formData = new FormData();
            formData.append('cod_prod', cod_prod);
            formData.append('producto', producto);
            formData.append('descripcion', descripcion);
            formData.append('precio', precio);
            formData.append('id_seccion', id_seccion);
            formData.append('seccion', seccion);
            formData.append('id_tipo', id_tipo);
            formData.append('tipo', tipo);
            formData.append('id_color', id_color);
            formData.append('color', color);
            formData.append('id_tallas', id_tallas);
            formData.append('tallas', tallas);            
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
                url: '../guarda_productos/',
                cache: false,
                contentType: false,
                processData: false,
                success: function (data) {
                    //console.log(formData.get("partida"));
                    console.log(data);
                }
            });
        });


        location.href = "../";
    });



    

    
});