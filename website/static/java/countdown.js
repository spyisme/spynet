function startCountdown() {
    // Initial call to update countdown
    updateCountdown();

    // Set interval to update countdown every second
    var x = setInterval(updateCountdown, 1000);

    function updateCountdown() {
        var countDownDate = new Date("June 10, 2024 08:00:00 GMT+0200").getTime();

        // Get the current date and time
        var now = new Date().getTime();

        // Calculate the distance between now and the countdown date
        var distance = countDownDate - now;

        // Calculate days, hours, minutes and seconds
        var days = Math.floor(distance / (1000 * 60 * 60 * 24));
        var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((distance % (1000 * 60)) / 1000);

        // Output the result in an element with id="countdown"
        document.getElementById("countdown").innerHTML = "Days till exams: " + days + "d " + hours + "h " + minutes + "m " + seconds + "s ";

        // If the countdown is over, display a message
        if (distance < 0) {
            clearInterval(x);
            document.getElementById("countdown").innerHTML = "EXPIRED";
        }
    }
}

// JavaScript code to adjust content padding to prevent it from overlapping with the fixed footer
function adjustContentPadding() {
    var content = document.querySelector('.content');
    var footer = document.querySelector('.footer');
    var footerHeight = footer.offsetHeight;
    content.style.paddingBottom = footerHeight + 'px';
}

// Call the adjustContentPadding function initially and whenever the window is resized
adjustContentPadding();
window.addEventListener('resize', adjustContentPadding);