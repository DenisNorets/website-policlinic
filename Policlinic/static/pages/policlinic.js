let was_here = 0;
let done = 0;

try {
    was_here = localStorage.getItem("was_here");
    done = localStorage.getItem("done");
} catch {}

$(document).ready ( function(){
if (was_here) {
    if (done == 0) {
        console.log("Работа не выполнена")
        $('.js-overlay').fadeIn();
        $('main').css('filter','blur(5px)'); 
    } else {
        console.log("Работа выполнена")
    }
} else {
    was_here = 1;
    localStorage.setItem("was_here", was_here);
}

$('.js-close').click(function() {
    $('.js-overlay').fadeOut();
    $('main').css('filter', 'none');
});

});

$('.btn-restart').click(function() {
    window.location = 'test.html';
});
