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

function carregaModal(controller, acctions){
    let url = `/${controller}/${acctions}`;
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

function carregaCarrinho(){
    NProgress.start();
    return $.ajax({
        type: 'GET',
        url: '/carrinho/aside',
        success: function(data){
            $('#carrinho').html(data)
            NProgress.done();
        }
    })
}

function toggleCarrinho(){
    $('.carrinho').toggleClass('active')
    $('.btn-carrinho').toggleClass('active')
}


function plus(el){
    let input = $(el).siblings('.carrinho__item-qtd--text');
    let value = parseInt($(input).val()) + 1;
    if(value > 10) {
        $(el).attr('disabled', true)
        return;
    } else {
        $(el).siblings('.minus').attr('disabled', false)
        $(input).val(value);
        $(input).trigger("change");
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
        return;
    } else {
        $(el).siblings('.plus').attr('disabled', false)
        $(input).val(value);
        $(input).trigger("change");
        if(value == 1) {
            $(el).attr('disabled', true);
        }
    }
}

function value_change(el){
    let value = parseInt($(el).val());
    calcula_total();
    // $.ajax({
    //     type: 'POST',
    //     url: '',
    //     data: value,
    //     success: function(data){}, 
    //     error: function(data){} 
    // })
}

function remove_item(el, id_item) {
    $(el).parents('.carrinho__item').remove()
    // $.ajax({
    //     type: 'POST',
    //     url: '/' + id_item,
    //     success: function(data) {},
    //     error: function(data) {}
    // })
}


function calcula_total(){
    let total = 0;
    $('.carrinho').find('.carrinho__item').each(function(){
        var qtd = parseInt($(this).find('.carrinho__item-qtd--text').val());
        var valor = parseFloat($(this).find('#valor').html());
        total += valor * qtd;
    })
    total = total.toFixed(2);
    $('#valorTotal').html(total)
    return total;
}