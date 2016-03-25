/* Project specific Javascript goes here. */
$(document).ready(function() {
        var parallaxItem = $('.myElement');
        $(window).scroll(function () {
            //Position in the page
            scrollPos = $(this).scrollTop();

            //Scroll the image's background at half the speed of the rest of the page
            //Change -0.5 to any other value depending on the desired effect
            parallaxItem.css({
                'background-position': "center " + (scrollPos * -0.5) + "px",
            });
        });
    })
