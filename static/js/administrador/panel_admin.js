// variable para nuestro boton del toggle
const hamburgesa = document.querySelector(".toggle-btn");
// variable para nuestro icono de toggle
const toggler = document.querySelector("#icon-toggle");

// creamos funcion de evento click para que cuando se le de al boton expanda el toggle
hamburgesa.addEventListener("click",function(){
    //aqui decimos que al div con id sidebar se le agregara la clase toggle con el evento expand
    document.querySelector("#sidebar").classList.toggle("expand");
    // decimos que en el icono de toggler cambie las clases de right a left 
    toggler.classList.toggle("fa-chevron-right");
    toggler.classList.toggle("fa-chevron-left");
});


$(document).ready(function () {
    $('.cmn-divfloat').click(function(){
		$('body, html').animate({
			scrollTop: '0px'
		}, 200);
	});

	$(window).scroll(function(){
		if( $(this).scrollTop() > 0 ){
			$('.cmn-divfloat').slideDown(200);
		} else {
			$('.cmn-divfloat').slideUp(200);
		}
	});

});


