const imgs = document.querySelectorAll('.img-select a');
const imgBtns = [...imgs];
let imgId = 1;

imgBtns.forEach((imgItem) => {
    imgItem.addEventListener('click', (event) => {
        event.preventDefault();
        imgId = imgItem.dataset.id;
        slideImage();
    });
});

function get_correct_price(size) {
    window.location.href = window.location.href + `?size=${size}`
}

function get_price_color(color) {
    window.location.href = window.location.href + `?color=${color}`;
}

function slideImage() {
    const displayWidth = document.querySelector('.img-showcase img:first-child').clientWidth;

    document.querySelector('.img-showcase').style.transform = `translateX(${- (imgId - 1) * displayWidth}px)`;
}

window.addEventListener('resize', slideImage);


$(function () {
    $('.stars').stars();
});
$.fn.stars = function () {
    return $(this).each(function () {
        var rating = $(this).data("rating");
        var fullStar = new Array(Math.floor(rating + 1)).join('<i class="fas fa-star"></i>');
        var halfStar = ((rating % 1) !== 0) ? '<i class="fas fa-star-half-alt"></i>' : '';
        var noStar = new Array(Math.floor($(this).data("numStars") + 1 - rating)).join('<i class="far fa-star"></i>');
        $(this).html(fullStar + halfStar + noStar);
    });
}

$.fn.stars = function () {
    return $(this).each(function () {
        const rating = $(this).data("rating");
        const numStars = $(this).data("numStars");
        const fullStar = '<i class="fas fa-star"></i>'.repeat(Math.floor(rating));
        const halfStar = (rating % 1 !== 0) ? '<i class="fas fa-star-half-alt"></i>' : '';
        const noStar = '<i class="far fa-star"></i>'.repeat(Math.floor(numStars - rating));
        $(this).html(`${fullStar}${halfStar}${noStar}`);
    });
}