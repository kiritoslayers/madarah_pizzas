$(window).on('load', function () {
    $('.banner__slider').slick({
        infinite: true,
        slidesToShow: 1,
        slidesToScroll: 1,
        speed: 300,
        dots: true,
        arrows: true,
    })
    $('body').on('click', '.close', function() {
        closeModal($(this).parents('.modal'))
    });

    toastr.options = {
        "closeButton": true,
        "debug": false,
        "newestOnTop": true,
        "progressBar": true,
        "positionClass": "toast-top-right",
        "preventDuplicates": false,
        "onclick": null,
        "showDuration": "300",
        "timeOut": "5000",
        "extendedTimeOut": "1000",
        "showEasing": "swing",
        "hideEasing": "linear",
        "showMethod": "fadeIn",
        "hideMethod": "fadeOut"
    }
    
    $.ajaxSetup({
        beforeSend: beforeSend,
        complete: afterSend,
    });

    $('body').on('click', '.btn-submit', function(event){
        event.preventDefault();
        postForm(event)

    })

    carregaCarrinho()
})
fnProgressBarLoading();