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
    let url = `/${controller}/${acctions}`
    // requisição feita em js
    $.ajax({
        method: 'GET',
        url: url,
        success: function(data){
            $('#modalConteudo').html(data)
            $('#modal').modal('show')
        }
    })

}


function closeModal(modal){
    $(modal).modal('hide')
    $(modal).find('.modal-content').html('')
    
}



function pizza_QtdChange(el, preco) {
    
}

function carrinho_removeItem(item){

}