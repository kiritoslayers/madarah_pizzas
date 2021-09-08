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
    })
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

    $('body').on('click', '.btn-submit[type=submit]', function (event) {
        event.preventDefault();
        postForm(event)
    });
    // $('body').unbind('change', '.togglePassword')
    $('body').on('change', '.togglePassword', function () {
        let checked = $(this).prop('checked')
        if (checked) {
            $(this).siblings('label').html('Esconder senha');
            $(this).parents('.password-container').find('.password').attr('type', 'text')
        } else {
            $(this).siblings('label').html('Exibir senha');
            $(this).parents('.password-container').find('.password').attr('type', 'password')

        }
    });

    jQuery.extend(jQuery.validator.messages, {
        required: "Esse campo é obrigatório.",
        remote: "Corrija esse campo.",
        email: "Insira um endereço de e-mail válido.",
        url: "Insira uma URL válida.",
        date: "INsira uma data válida.",
        dateISO: "Insira uma data válida.",
        number: "Insira um número válido.",
        digits: "Insira apenas numeros.",
        creditcard: "Insira um numero de cartão de crédito válido.",
        equalTo: "Insira o valor novamente.",
        accept: "A extnsão não é válida.",
        maxlength: jQuery.validator.format("A quantidade de caracteres não pode ser maior que {0}."),
        minlength: jQuery.validator.format("Insira no mínimo {0} caracteres."),
        rangelength: jQuery.validator.format("Insira um valor entre {0} e {1} caracteres."),
        range: jQuery.validator.format("Insira um valor entre {0} e {1}."),
        max: jQuery.validator.format("Insira um valor menor ou igual a {0}."),
        min: jQuery.validator.format("Insira um valor maior ou igual a {0}.")
    });
    $('body').on('change', 'form input, form select, form textarea', function(e){
        oi(e.target)
    })

})
fnProgressBarLoading()

function oi(el){
    console.log($(el))
    console.log($(el).val())
    console.log($(el).validator)
    console.log($(el).parents('form'))

}