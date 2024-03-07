// static/script.js
document.addEventListener("DOMContentLoaded", function () {
    var audio = document.getElementById("backgroundAudio");

    // Check if the audio element exists on the page
    if (audio) {
        // Play the audio as soon as the page loads
        audio.volume = 0.5;

        audio.play();

        // Save the current time when leaving the page
        window.addEventListener("beforeunload", function () {
            localStorage.setItem("audioTime", audio.currentTime);
        });

        // Load the saved time when entering the page
        window.addEventListener("load", function () {
            var savedTime = localStorage.getItem("audioTime");
            if (savedTime) {

                audio.currentTime = parseFloat(savedTime);
            }
        });
    }
});
