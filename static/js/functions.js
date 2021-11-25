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

function carregaModal(controller, actions){
    let url = `/${controller}`;
    if(actions) {
        url += `/${actions}`
    }
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
    });

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
    NProgress.done();
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
        'opacity': '0',
        'visibility': 'hidden'
    })
}

function postError(data){
    console.error(data)
    toastr.error('Verifique os campos ou contate a equipe de desenvolvimento');
    toastr.error('Ocorreu um problema no envio do formulário');
    NProgress.done();
    $('.loading').css({
        'opacity': '0',
        'visibility': 'hidden'
    })
}

function postForm(event){
    event.preventDefault();
    $('.loading').css({
        'opacity': '1',
        'visibility': 'visible'
    })
    let url = event.target.form.action;
    $.ajax({
        type: 'POST',
        url: url,
        data: $(event.target.form).serialize(),
        success: postSuccess,
        error: postError,
    });
}

function pegarClienteId(){
    return document.getElementById('id_cliente').value
}

function carregaCarrinho(){
    NProgress.start();
    return $.ajax({
        type: 'GET',
        url: '/carrinho/aside/' + pegarClienteId(),
        success: function(data){
            $('#carrinho').html(data);
            NProgress.done();
        }
    })
}

function toggleCarrinho(){
    $('.carrinho').toggleClass('active')
    $('.btn-carrinho').toggleClass('active')
    localStorage.setItem('carrinho-open', $('.btn-carrinho').hasClass('active'))
}

function openCarrinho(){
    $('.carrinho').addClass('active')
    $('.btn-carrinho').addClass('active')
    localStorage.setItem('carrinho-open', true)
}

function pedir(el){
    let id = $(el).data('id');
    let cliente = $(el).data('cliente');
    NProgress.start();
    $.ajax({
        url: '/carrinho/adicionar/' + id + '/' + cliente,
        type: 'POST',
        success: function(data){
            if(data == 'ok') {
                carregaCarrinho().then(res =>{
                    openCarrinho();
                });
            }
        },
        error: function(data){
            postError(data)
        },
        finally: function(data) {
            console.log(data)
        }
    })
}

function plus(el){
    let input = $(el).siblings('.carrinho__item-qtd--text');
    let value = parseInt($(input).val()) + 1;
    if(value > 10) {
        $(el).attr('disabled', true)
        toastr.warning('Você não pode pedir mais que 10 pizzas por sabor!!')
        return;
    } else {
        $(el).siblings('.minus').attr('disabled', false)
        $(input).val(value);
        $(input).trigger("change");
        set_quantidade(input)
        if(value == 10) {
            $(el).attr('disabled', true);
        }
    }
}

function minus(el){
    let input = $(el).siblings('.carrinho__item-qtd--text');
    let value = parseInt($(input).val()) - 1;
    if(value < 1) {
        $(el).attr('disabled', true);
        remove_item(input)
        return;
    } else {
        $(el).siblings('.plus').attr('disabled', false)
        $(input).val(value);
        $(input).trigger("change");
        set_quantidade(input)
        if(value == 1) {
            $(el).attr('disabled', true);
        }
    }
}

function remove_item(el) {
    $(el).val(0)
    $(el).trigger("change");
    let qtd = $(el).val();
    let id = $(el).data('id');
    set_quantidade(el)
}

function set_quantidade(el) {
    let qtd = $(el).val();
    let id = $(el).data('id');
    NProgress.start();
    $.ajax({
        url: '/carrinho/set_quantidade/' + id + '/' + qtd,
        type: 'POST',
        success: function(data){
           if(data == 'ok') {
                carregaCarrinho().then(res =>{
                    openCarrinho();
                });
           }
        },
        error: function(data){
            postError(data)
        }
    })
}

function finalizar(){
    return $.ajax({
        type: 'POST',
        url: '/carrinho/finalizar',
        success: function(response){
        
        },
        error: function(response){
        
        }
    })
}
function statusPedido(el) {
    let id = $(el).data('id');
    let status = $(el).val();
    $.ajax({
        url: `/pedidos/status/` + id,
        method: 'POST',
        data: { status: status },
        success: function (data) {
            if(data == 'OK' ) {
                toastr.success('Status atualizado')
                $(el).val(status)
            }
        },
        error: function(data) {
            toastr.error('Houve um erro')
        }
    })
}