(function($) {
    $.fn.rotator = function(options) {

        var rotatorIndex = 0;
        var rotatorVisibleItems = options.visibleItems;

        var rotatorWidth = parseInt(this.find('.rotator-item').width()) + parseInt(this.find('.rotator-item').css('margin-right'));
        var rotatorCount = this.find('.rotator-item').length;

        var rotatorWindow = this.find('.rotator-window');
        var prevButton = this.find('.prev');
        var nextButton = this.find('.next');

        var animating = false;

        if (rotatorCount > rotatorVisibleItems) {
            nextButton.addClass('active');
        }

        nextButton.click(function() {
            if (rotatorIndex < rotatorCount - rotatorVisibleItems) {
                if (!animating) {
                    mleft = rotatorWindow.css('margin-left').replace('px', '');
                    newMleft = new String(parseInt(mleft) - rotatorWidth);
                    rotatorWindow.animate({
                        'margin-left': newMleft + 'px'
                    }, 1000, function() {
                        animating = false;
                    });
                    rotatorIndex++;
                    animating = true;
                }
            }
            if (rotatorIndex == rotatorCount - rotatorVisibleItems) {
                if ($(this).hasClass('active')) {
                    $(this).removeClass('active');
                }
            }
            if (!prevButton.hasClass('active')) {
                prevButton.addClass('active');
            }
            return false;
        });

        prevButton.click(function() {
            if (rotatorIndex > 0) {
                if (!animating) {
                    mleft = rotatorWindow.css('margin-left').replace('px', '');
                    newMleft = new String(parseInt(mleft) + rotatorWidth);
                    rotatorWindow.animate({
                        'margin-left': newMleft + 'px'
                    }, 1000, function() {
                        animating = false;
                    });
                    rotatorIndex--;
                    animating = true;
                }
            }
            if (rotatorIndex == 0) {
                if ($(this).hasClass('active')) {
                    $(this).removeClass('active');
                }
            }
            if (!nextButton.hasClass('active')) {
                nextButton.addClass('active');
            }
            return false;
        });
    };

})(jQuery);

(function($) {
    $.fn.fadeRotator = function() {

        var fadeRotator = this;

        var rotatorIndex = 0;
        var currentItem = null;
        var rotatorCount = fadeRotator.find('.rotator-item').length;

        var prevButton = fadeRotator.find('.prev');
        var nextButton = fadeRotator.find('.next');

        fadeRotator.find('.rotator-item').css('display', 'none');

        currentItem = fadeRotator.find('.rotator-item:first-child');

        currentItem.fadeIn();

        nextButton.click(function() {

            if ((rotatorIndex + 1) < rotatorCount) {

                rotatorIndex++;

                var nextItem = fadeRotator.find('.rotator-item:nth-child(' + (rotatorIndex + 1) + ')');

                currentItem.fadeOut(300, function() {
                    nextItem.fadeIn(300);
                });

                currentItem = nextItem;

            }
            if (rotatorIndex == rotatorCount) {
                if ($(this).hasClass('active')) {
                    $(this).removeClass('active');
                }
            }
            if (!prevButton.hasClass('active')) {
                prevButton.addClass('active');
            }
            return false;
        });

        prevButton.click(function() {
            if (rotatorIndex > 0) {
                rotatorIndex--;

                var nextItem = fadeRotator.find('.rotator-item:nth-child(' + (rotatorIndex + 1) + ')');

                currentItem.fadeOut(300, function() {
                    nextItem.fadeIn(300);
                });

                currentItem = nextItem;
            }
            if (rotatorIndex == 0) {
                if ($(this).hasClass('active')) {
                    $(this).removeClass('active');
                }
            }
            if (!nextButton.hasClass('active')) {
                nextButton.addClass('active');
            }
            return false;
        });
    };

})(jQuery);



(function($) {
    $.fn.testimonials = function() {
        this.find(".testimonial-rotator").children().first().show();
        var words_all = new Array();
        $('.testimonial-quote').each(function(){
            var words = $(this).text().split(' ').length;
            var time = Math.ceil(words/3.3);
            words_all.push(time);
        });

        console.log(words_all);

        var setTestimonialInterval;
        var showNextTestimonial = function() {
            var currentItem = $('.testimonial:visible').first();

            currentItem.fadeOut('slow', function() {
                var nextItem = currentItem.next();
                if (nextItem.length == 0) {
                    nextItem = $('.testimonial').first();
                }
                nextItem.fadeIn('slow');
                nextItem.jScrollPane({
                    autoReinitialise: true
                });
            });
        }

        if ($('.testimonial').length > 1) {
            setTestimonialInterval = setInterval(showNextTestimonial, words_all[0]);
        }
    };

})(jQuery);

(function($) {

    $.fn.getDirections = function(latitude, longitude) {

        $("#origin").unbind('keypress').on('keypress', function(event) {

            if (event.which == 13) {

                event.preventDefault();

                getDirections(latitude, longitude);
            }

        });

        $('#submitButton').unbind('click').on('click', function(event) {

            getDirections(latitude, longitude);

        });

    }

})(jQuery);

(function($) {

    $.fn.iconRotator = function(options) {

        var rotator = $(this);

        if (rotator.find('.rotator-item').length != 0) {
            var rotatorFirstItem = rotator.find('.rotator-item').first();
            var arrowFirst = rotator.find('.rotator-prev').first();

            var itemWidth = parseInt(rotatorFirstItem.width()) + parseInt(rotatorFirstItem.css('margin-left')) + parseInt(rotatorFirstItem.css('margin-right'));
            var arrowWidth = parseInt(arrowFirst.width()) + parseInt(arrowFirst.css('margin-left')) + parseInt(arrowFirst.css('margin-right'));

            var totalItems = rotator.find('.rotator-item').length
            var allItemWidth = (totalItems * itemWidth);

            var visibleItems = 0;

            if (allItemWidth <= rotator.width()) {
                //we dont need arrows
                rotator.css('width', allItemWidth);
                rotator.css('margin-left', 'auto');
                rotator.css('margin-right', 'auto');
                rotator.find('.rotator-prev').css('display', 'none');
                rotator.find('.rotator-next').css('display', 'none');
                rotator.find('.rotator-items').css('width', '100%');

                visibleItems = totalItems;
            } else {
                var allocatedWidth = arrowWidth * 2;

                do {
                    visibleItems++;

                    allocatedWidth += itemWidth;

                } while (allocatedWidth < rotator.width())

                if (allocatedWidth > rotator.width() && visibleItems) {
                    visibleItems--;

                    allocatedWidth -= itemWidth;

                    var leftOverSpace = rotator.width() - allocatedWidth;
                    var itemMarginRight = leftOverSpace / visibleItems;

                    rotator.find('.rotator-item').css('margin-left', itemMarginRight);

                    itemWidth = parseInt(rotatorFirstItem.width()) + parseInt(rotatorFirstItem.css('margin-left')) + parseInt(rotatorFirstItem.css('margin-right'));
                }

            }

            var prevButton = rotator.find('.prev');
            var nextButton = rotator.find('.next');
            var rotatorWindow = rotator.find('.rotator-window');
            var rotatorAnimating = false;

            prevButton.on('click', function() {

                if (!rotatorAnimating) {
                    rotatorAnimating = true;

                    var currentOffset = parseInt(rotatorWindow.css('margin-left'));

                    if (currentOffset < 0) {
                        currentOffset += itemWidth;

                        rotatorWindow.animate({
                            'margin-left': currentOffset + 'px'
                        }, 300, function() {

                            rotatorAnimating = false;

                            if (currentOffset >= 0) {
                                rotator.find('.rotator-prev').removeClass('active');
                            }

                        });
                    } else {
                        rotatorAnimating = false;
                    }

                }

            });

            nextButton.on('click', function() {

                if (!rotatorAnimating) {
                    rotatorAnimating = true;

                    var currentOffset = parseInt(rotatorWindow.css('margin-left'));

                    var visibleItemOffset = visibleItems * itemWidth;

                    if (currentOffset + (totalItems * itemWidth) >= rotator.width()) {
                        currentOffset -= itemWidth;

                        rotatorWindow.animate({
                            'margin-left': currentOffset + 'px'
                        }, 300, function() {

                            rotatorAnimating = false;

                            if ((currentOffset * -1) + visibleItemOffset >= allItemWidth) {
                                rotator.find('.rotator-prev').removeClass('active');
                            }

                        });

                    } else {
                        rotatorAnimating = false;
                    }
                }

            });

        } else {
            rotator.css('height', '0px');
            rotator.find('.rotator-prev').css('display', 'none');
            rotator.find('.rotator-next').css('display', 'none');
        }

    }

})(jQuery);

function getDirections(latitude, longitude) {
    var origin = $('#origin').val();
    if ($('#destination').length > 0) {
        var destination = $('#destination').val();
    } else {
        var destination = new google.maps.LatLng(latitude, longitude);
    }
    var container = $('#directionsRenderer');

    var service = new google.maps.DirectionsService();
    var renderer = new google.maps.DirectionsRenderer();

    var request = {
        origin: origin,
        destination: destination,
        travelMode: google.maps.DirectionsTravelMode.DRIVING
    }

    container.empty();

    $('.print-directions').remove();

    renderer.setPanel(container.get(0));

    service.route(request, function(response, status) {

        if (status == google.maps.DirectionsStatus.OK) {

            renderer.setDirections(response);

            $('#directionsPage .print').css('display', 'block');

        } else {

            container.html('<p><em>Directions not available for the specified address.</em></p>');

        }

    });
}