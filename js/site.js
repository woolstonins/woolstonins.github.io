jQuery(document).ready(function ($) {
    // $('.testimonials').testimonials();
    // if ($('.testimonial').length > 0) {
    //     $('.testimonial').jScrollPane({autoReinitialise: true});
    // } else {
    //     $('.testimonials').find('h2').remove();
    // }
    $('.banner').backstretch("img/SaltLakeCity.jpg");

    var window_width = $(window).width();
    if (window_width <= 420) {
        $('.testimonial-rotator').addClass('swipe');

        window.mySwipe = new Swipe(document.getElementById('slider'), {
            startSlide: 2,
            speed: 1000,
            auto: 10000,
            continuous: true,
            disableScroll: false,
            stopPropagation: false,
            callback: function(index, elem) {},
            transitionEnd: function(index, elem) {}
          });
    }
});

// When the user scrolls the page, execute myFunction 
window.onscroll = function() {stickyheader()};

// Get the header
var header = document.getElementById("top_nav");
var home_page = document.getElementById("home-page");

// Get the offset position of the navbar
var sticky = header.offsetTop;

// Add the sticky class to the header when you reach its scroll position. Remove "sticky" when you leave the scroll position
function stickyheader() {
  if (window.pageYOffset >= sticky) {
    header.classList.add("sticky");
    home_page.classList.add("stickied");
  } else {
    header.classList.remove("sticky");
    home_page.classList.remove("stickied");
  }
}

// This example displays an address form, using the autocomplete feature
// of the Google Places API to help users fill in the information.

var geolocation = null;
var circle = null;

var placeSearch, autocomplete;
var componentForm = {
    street_number: 'short_name',
    route: 'long_name',
    locality: 'long_name',
    administrative_area_level_1: 'short_name',
    country: 'long_name',
    postal_code: 'short_name'
};

function initAutocomplete() {
    console.log('initAutocomplete');
    // Create the autocomplete object, restricting the search to geographical
    // location types.
    autocomplete = new google.maps.places.Autocomplete(
    /** @type {!HTMLInputElement} */(document.getElementById('autocomplete')),
    {types: ['geocode']});

    // When the user selects an address from the dropdown, populate the address
    // fields in the form.
    autocomplete.addListener('place_changed', fillInAddress);
}

function fillInAddress() {
    // Get the place details from the autocomplete object.
    var place = autocomplete.getPlace();

    for (var component in componentForm) {
        document.getElementById(component).value = '';
        document.getElementById(component).disabled = false;
    }

    // Get each component of the address from the place details
    // and fill the corresponding field on the form.
    for (var i = 0; i < place.address_components.length; i++) {
        var addressType = place.address_components[i].types[0];
        if (componentForm[addressType]) {
        var val = place.address_components[i][componentForm[addressType]];
        document.getElementById(addressType).value = val;
        }
    }
}

// Bias the autocomplete object to the user's geographical location,
// as supplied by the browser's 'navigator.geolocation' object.
function geolocate() {
    initAutocomplete();

    //var l =  autocomplete.geometry.viewport;
    if (geolocation == null) {
        if (circle == null) {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(function(position) {
                    geolocation = {
                        lat: position.coords.latitude,
                        lng: position.coords.longitude
                    };
                    circle = new google.maps.Circle({
                        center: geolocation,
                        radius: position.coords.accuracy
                    });
                    autocomplete.setBounds(circle.getBounds());
                });
            }

        }
    }
}
