$(document).ready(function(){
    $(".ver_prod").click(function (e) {         
        var url = $(this).data('url');
        location.href = url;
    });

    
});