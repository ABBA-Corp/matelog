let h = document.documentElement.clientHeight;
let hh = parseInt($('.top-nav-scrl').css('height'));

function scrl() {
    var top = $(window).scrollTop();
    console.log(h, hh)
    if (top > ((h + hh) / 3)) {
        $('.top-scroller').removeClass('header-body')
        $('.top-scroller').addClass('scrolled-top-nav')
    } else {
        $('.top-scroller').removeClass('scrolled-top-nav')
        $('.top-scroller').addClass('header-body')
    }
}



$(window).on("scroll", () => {
    scrl()
})
