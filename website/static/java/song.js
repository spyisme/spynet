// static/java/song.js
document.addEventListener("DOMContentLoaded", function () {
    var audio = document.getElementById("backgroundAudio");
    var startButton = document.getElementById("startButton");
    var stopButton = document.getElementById("stopButton");

    // Check if the audio element and buttons exist on the page
    if (audio && startButton && stopButton) {
        // Play the audio when the "Start Music" button is clicked
        startButton.addEventListener("click", function () {
            audio.play();
        });

        // Pause the audio when the "Stop Music" button is clicked
        stopButton.addEventListener("click", function () {
            audio.pause();
        });

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
