// to get current year
function getYear() {
    var currentDate = new Date();
    var currentYear = currentDate.getFullYear();
    document.querySelector("#displayYear").innerHTML = currentYear;
}

getYear();

// client section owl carousel (only for index.html)
if (window.location.pathname === '/index.html') {
    $(".client_owl-carousel").owlCarousel({
        loop: true,
        margin: 20,
        dots: false,
        nav: true,
        navText: [],
        autoplay: true,
        autoplayHoverPause: true,
        navText: [
            '<i class="fa fa-angle-left" aria-hidden="true"></i>',
            '<i class="fa fa-angle-right" aria-hidden="true"></i>'
        ],
        responsive: {
            0: {
                items: 1
            },
            600: {
                items: 2
            },
            1000: {
                items: 2
            }
        }
    });
}

// Scroll animation for slider section (only for index.html)
if (window.location.pathname === '/index.html') {
    $(window).on('load scroll', function() {
        const detailBox = $('.detail-box');
        const imgBox = $('.img-box');
        const scrollPosition = $(window).scrollTop();
        const windowHeight = $(window).height();
        
        if (scrollPosition < windowHeight) {
            detailBox.css('transform', `translateY(${scrollPosition * 0.5}px)`);
            imgBox.css('transform', `translateY(${scrollPosition * 0.1}px)`);
        }
    });
}

/** google_map js **/
function myMap() {
    var mapProp = {
        center: new google.maps.LatLng(40.712775, -74.005973),
        zoom: 18,
    };
    var map = new google.maps.Map(document.getElementById("googleMap"), mapProp);
}