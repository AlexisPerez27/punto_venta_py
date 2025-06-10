$(document).ready(function () {

    $(document).on("click", ".eli_tareas", function (e) {
        var id = $(this).parents("tr").find("td:eq(0)").text();

        var data = {id_tarea : id, 'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()}

        // console.log(data);

        // $.ajax({
        //     type: "POST",
        //     url: "../elimina_tarea/",
        //     data: data,
        //     success: function (res) {
        //         console.log(res)
        //         // $('#message').html("<h2>Contact Form Submitted!</h2>")
        //     }
        // });


        Swal.fire({
            title: "¿Estas seguro que quieres eliminar registro?",
            showDenyButton: true,
            // showCancelButton: true,
            confirmButtonText: "Guardar",
            denyButtonText: "Cancelar",
             icon: "question"
        }).then((result) => {
            if (result.isConfirmed) {     
                
                $.post("../elimina_tarea/", data,function (res) {
                    console.log(res)
                    $("#datos_tar").html(res);
                    Swal.fire("Saved!", "", "success");
                    e.preventDefault();
                });               


            } else if (result.isDenied) {
                Swal.fire("Se ha cancelado la operacion", "", "info");
                e.preventDefault();
            }
        });

        
    });



    $(document).on("click", ".eli_tar_com", function (e) {
        var id = $(this).parents("tr").find("td:eq(0)").text();

        var data = {id_tarea : id, 'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()}

                
        $.post("../elimina_tarea_com/", data,function (res) {
            console.log(res)
            $("#datos_comp").html(res);
            Swal.fire({
                title: "Eliminacion",
                text: "Se elimino registro de manera exitosa",
                icon: "success"
            });
        });               


        
    });
});