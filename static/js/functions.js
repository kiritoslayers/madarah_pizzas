function toggleMenuMobile() {
    let isMobile = $(window).width() < 600;
    if(isMobile) {
        $('.btn-toggleMenu').toggleClass('active')
        $('.navbar-nav').toggleClass('active')
    } else {
        $('.btn-toggleMenu').removeClass('active')
        $('.navbar-nav').removeClass('active')
    }
}

function toggleCarrinho(){
    $('.carrinho').toggleClass('active')
    $('.btn-carrinho').toggleClass('active')
}


function carregaModal(controller, acctions){
    // NProgress.start();
    let url = `/${controller}/${acctions}`;
    
    // requisição feita em js
    $.ajax({
        method: 'GET',
        url: url,
        success: function(data){
            $('#modalConteudo').html(data)
            $('#modal').modal('show')
        },
        error: function(data) {
            console.error(data)
            toastr.error('Contate a equipe de desenvolvimento')
            toastr.error('Houve um erro na requisição')
        }
    })

}


function closeModal(modal){
    modal = modal == undefined ? $('#modal') : modal;
    $(modal).modal('hide')
    $(modal).find('.modal-content').html('')
    $(modal).find('.modal-dialog').removeAttr('style')
    
}

function fnProgressBarLoading() {
    NProgress.start();
    $('.loading').css({
        'opacity': '1',
        'visibility': 'visible'
    })
    window.addEventListener("load", function (event) {
        NProgress.done();
        $('.loading').css({
            'opacity': '0',
            'visibility': 'hidden'
        })
    });
}


function beforeSend(data) {
    NProgress.start()
    $('.loading').css({
        'opacity': '1',
        'visibility': 'visible'
    });
}
function afterSend(data) {
    NProgress.done()
    $('.loading').css({
        'opacity': '0',
        'visibility': 'hidden'
    });
}

function postSuccess(url){
    toastr.success('Operação concuída com sucesso');
    NProgress.done();
    closeModal();
    window.location.href = url;
    $('.loading').css({
        'opacity': '1',
        'visibility': 'hidden'
    })
}

function postError(data){
    console.error(data)
    toastr.error('Verifique os campos ou contate a equipe de desenvolvimento');
    toastr.error('Ocorreu um problema no envio do formulário');
    NProgress.done();
    $('.loading').css({
        'opacity': '1',
        'visibility': 'hidden'
    })
}

// function postForm(event){
//     event.preventDefault();
//     let url = `${event.currentTarget.form.action}`;
//     // $(event.target.form).find('.decimal').each(function(){
//     //     let newValue = $(this).val().replace
//     // })
//     $.ajax({
//         type: 'POST',
//         url: url,
//         data: $(event.target.form).serialize(),
//         success: postSuccess,
//         error: postError,
//     });
// }

function postForm(event){
    event.preventDefault();
    $('.loading').css({
        'opacity': '1',
        'visibility': 'visible'
    })
    let url = event.target.form.action;
    let data
    $.ajax({
        type: 'POST',
        url: url,
        data: $(event.target.form).serialize(),
        success: postSuccess,
        error: postError,
    });
}
