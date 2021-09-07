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
            // NProgress.done();
        }
    })

}


function closeModal(modal){
    modal = modal == undefined ? $('#modal') : modal;
    $(modal).modal('hide')
    $(modal).find('.modal-content').html('')
    
}

function fnProgressBarLoading() {
    NProgress.start();
    window.addEventListener("load", function (event) {
        NProgress.done();
    });
}


function beforeSend(data) {
    NProgress.start()
    console.log(data)
}

function afterSend(data) {
    NProgress.done()
    console.log(data)
}

function postSuccess(data){
    if(data == 'ok') {
        toastr.success('Operação concuída com sucesso');
        NProgress.done();
        closeModal()
    }
}

function postError(data){
    console.error(data)
    toastr.error('Verifique os campos ou contate a equipe de desenvolvimento');
    toastr.error('Ocorreu um problema no envio do formulário');
    NProgress.done();
}

function postForm(event){
    event.preventDefault();
    console.log(event)
    let url = `/${controller}/${action}/`
    // $.ajax({
    //     type: 'POST',
    //     data: data,
    //     success: postSuccess,
    //     error: postError,

    // })
}
