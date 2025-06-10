$(document).ready(function () {
    $(document).on("click", ".eliminar", function (e) {
        if (confirm("¿Estas seguro que quieres eliminar registro?")) {
            console.log("Has pulsado aceptar");
        } else {
            console.log("Has pulsado cancelar");
            e.preventDefault();
        }
    });
    /* $(document).on("click", ".eliminar", function (e) {        
        
        Swal.fire({
            title: "¿Estas seguro que quieres eliminar registro?",
            showDenyButton: true,
            // showCancelButton: true,
            confirmButtonText: "Guardar",
            denyButtonText: `Cancelar`
        }).then((result) => {
            if (result.isConfirmed) {                

                Swal.fire("Saved!", "", "success");
                e.preventDefault();

                location.reload();
                


            } else if (result.isDenied) {
                Swal.fire("Changes are not saved", "", "info");
                e.preventDefault();
            }
        });
    }); */
});