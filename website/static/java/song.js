// static/java/song.js
document.addEventListener("DOMContentLoaded", function () {
    var audio = document.getElementById("backgroundAudio");
    var startButton = document.getElementById("startButton");
    var stopButton = document.getElementById("stopButton");
    var restartButton = document.getElementById("restartButton");

    // Check if the audio element and buttons exist on the page
    if (audio && startButton && stopButton && restartButton) {
        // Play the audio when the "Start Music" button is clicked
        startButton.addEventListener("click", function () {
            audio.play();
        });

        // Pause the audio when the "Stop Music" button is clicked
        stopButton.addEventListener("click", function () {
            audio.pause();
        });

        // Restart the audio from the beginning when the "Restart Music" button is clicked
        restartButton.addEventListener("click", function () {
            audio.currentTime = 0;
            audio.play();
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
            } else {
                // Play the audio on page load
                audio.play();
            }
        });
    }
});
