$(document).ready(function(){

    $(document).on("click",".carousel-control-prev",function (e) { 
        var alt = $(this).parents("div").find(".active").attr("alt");  
        
        var max_id_img = $("#max_id_img").val();
        var min_id_img = $("#min_id_img").val();

        alt = alt - 1;

        if(alt < min_id_img){
            alt = max_id_img;
        }

        console.log(alt)

        $(".prev-img").each(function () {

            var img = $(this);
            var new_alt = img.attr("alt");

            if(img.hasClass("img-active")){
                img.removeClass("img-active");
            }

            if( alt == new_alt){
                img.addClass("img-active");
            }
        });
        
    });


    $(document).on("click",".carousel-control-next",function (e) { 
        var alt = $(this).parents("div").find(".active").attr("alt");  
        
        var min_id_img = $("#min_id_img").val();
        var max_id_img = $("#max_id_img").val();

        alt = parseInt(alt) + 1;

        if(alt > max_id_img){
            alt = min_id_img;
        }

        console.log(alt)

        $(".prev-img").each(function () {

            var img = $(this);
            var new_alt = img.attr("alt");

            if(img.hasClass("img-active")){
                img.removeClass("img-active");
            }

            if( alt == new_alt){
                img.addClass("img-active");
            }
        });
        
    });

    $(document).on("click",".prev-img",function (e) { 
        var alt = $(this).attr("alt");

        if($(this).hasClass("img-active")){
            $(this).removeClass("img-active");
        }

        $(".prev-img").each(function () {
            var img = $(this);

            var new_alt = img.attr("alt");

            if(img.hasClass("img-active")){
                img.removeClass("img-active");
            }

            if( alt == new_alt){
                img.addClass("img-active");
            }
        });


        if($(".carousel-item").hasClass("active")){
            $(".carousel-item").removeClass("active");
        }

        $(".carousel-item").each(function () {
            var img = $(this);

            var new_alt = img.attr("alt");

            if(img.hasClass("active")){
                img.removeClass("active");
            }

            if( alt == new_alt){
                img.addClass("active");
            }
        });
    });



    $(document).on("click",".color_prod",function (e) {

        var datos = {
            id_producto : $(this).find("input[name='id_prod_txt']").val(),
            id_color : $(this).find("input[name='id_color_txt']").val(),
            csrfmiddlewaretoken :  $("input[name=csrfmiddlewaretoken]").val(),
        }
        

        $.post("../select_color/", datos,function (data) {
            // console.log(data)
            $(".paleta_colores").html(data);
        });


        $.post("../select_tallas/", datos,function (data) {
            // console.log(data);
            $(".paleta_tallas").html(data);
        });


        $.post("../select_images/", datos,function (data) {
            // console.log(data);
            $(".paleta_images").html(data);
        });
    });
    

    $(document).on("click",".tallas",function (e) {
        var id_det = $(this).find("input[name='id_det_prod']").val();
        
        // $(this).addClass("tallas_active");

        if($(".tallas").hasClass("tallas_active")){
            $(".tallas").removeClass("tallas_active");
        }

        $(".tallas").each(function () {
            var tallas = $(this);

            var new_id_det = tallas.find("input[name='id_det_prod']").val();

            if(tallas.hasClass("tallas_active")){
                tallas.removeClass("tallas_active");
            }

            if( id_det == new_id_det){
                tallas.addClass("tallas_active");
            }
        });

        console.log(id_det)
    });
    
});