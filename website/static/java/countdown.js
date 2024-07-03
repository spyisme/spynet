function startCountdown() {
    // List of countdown dates
    var countdownDates = [
        new Date("July 2, 2024 08:00:00 GMT+0200").getTime(),
        new Date("July 6, 2024 08:00:00 GMT+0200").getTime(),
        new Date("July 10, 2024 08:00:00 GMT+0200").getTime(),
        new Date("July 13, 2024 08:00:00 GMT+0200").getTime(),
        new Date("July 17, 2024 08:00:00 GMT+0200").getTime(),
        new Date("July 20, 2024 08:00:00 GMT+0200").getTime()
    ];

    // Index to keep track of the current countdown date
    var currentIndex = 0;

    // Initial call to update countdown
    updateCountdown();

    // Set interval to update countdown every second
    var x = setInterval(updateCountdown, 1000);

    function updateCountdown() {
        var countDownDate = countdownDates[currentIndex];

        // Get the current date and time
        var now = new Date().getTime();

        // Calculate the distance between now and the countdown date
        var distance = countDownDate - now;

        // Calculate days, hours, minutes, and seconds
        var days = Math.floor(distance / (1000 * 60 * 60 * 24));
        var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((distance % (1000 * 60)) / 1000);

        // Output the result in an element with id="countdown"
        document.getElementById("countdown").innerHTML = "Days till exams: " + days + "d " + hours + "h " + minutes + "m " + seconds + "s ";

        // Update the date element
        var currentTargetDate = new Date(countDownDate);
        var options = { year: 'numeric', month: 'long', day: 'numeric' };
        document.getElementById("date").innerHTML = currentTargetDate.toLocaleDateString(undefined, options);


        // If the countdown is over, move to the next date or display a message
        if (distance < 0) {
            currentIndex++;
            if (currentIndex < countdownDates.length) {
                countDownDate = countdownDates[currentIndex];
            } else {
                clearInterval(x);
                document.getElementById("countdown").innerHTML = "EXPIRED";
            }
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
