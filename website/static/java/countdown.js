function startCountdown() {
    // List of countdown dates with titles
    var countdownDates = [
        { date: new Date("January 4, 2025 12:00:00 GMT+0200").getTime(), title: "Calculus 1" },
        { date: new Date("January 6, 2025 12:00:00 GMT+0200").getTime(), title: "English" },
        { date: new Date("January 11, 2025 12:00:00 GMT+0200").getTime(), title: "Statics" },
        { date: new Date("January 15, 2025 12:00:00 GMT+0200").getTime(), title: "Computer" },
        { date: new Date("January 18, 2025 12:00:00 GMT+0200").getTime(), title: "Physics" },
        { date: new Date("January 22, 2025 12:00:00 GMT+0200").getTime(), title: "Chinese" }
    ];

    // Index to keep track of the current countdown date
    var currentIndex = 0;

    // Initial call to update countdown
    updateCountdown();

    // Set interval to update countdown every second
    var x = setInterval(updateCountdown, 1000);

    function updateCountdown() {
        var now = new Date().getTime();

        // Move to the next countdown date if the current one has expired
        while (currentIndex < countdownDates.length && countdownDates[currentIndex].date <= now) {
            currentIndex++;
        }

        // If no more countdown dates, display "EXPIRED" message
        if (currentIndex >= countdownDates.length) {
            clearInterval(x);
            document.getElementById("countdown").innerHTML = "&copy; 2025 Sanawya sessions (Sc : amrayman_n)";
            document.getElementById("date").innerHTML = "";
            return;
        }

        var countDownDate = countdownDates[currentIndex].date;

        // Calculate the distance between now and the countdown date
        var distance = countDownDate - now;

        // Calculate days, hours, minutes, and seconds
        var days = Math.floor(distance / (1000 * 60 * 60 * 24));
        var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((distance % (1000 * 60)) / 1000);

        // Output the result in an element with id="countdown"
        document.getElementById("countdown").innerHTML = "Days till next exam: " + days + "d " + hours + "h " + minutes + "m " + seconds + "s ";

        // Update the date element with title
        var currentTargetDate = new Date(countDownDate);
        var options = { year: 'numeric', month: 'long', day: 'numeric' };
        try {
        document.getElementById("date").innerHTML = countdownDates[currentIndex].title + " on " + currentTargetDate.toLocaleDateString(undefined, options);
        throw new TypeError("oops");
    } catch ({ name, message }) {
      console.log(name); // "TypeError"
      console.log(message); // "oops"
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
