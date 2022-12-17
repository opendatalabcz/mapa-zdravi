// console.log('I am running')

$(document).ready(function() {
    $( "#setHeight" ).on('load', function() { 
        var mydiv = $(this).contents().find("div");
        var h = mydiv.height();
        $(this).height(h);
    });
});