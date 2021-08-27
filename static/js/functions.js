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