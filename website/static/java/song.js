// Song.js
document.addEventListener("DOMContentLoaded", function () {
    var audio = document.getElementById("backgroundAudio");

    // Check if the audio element exists on the page
    if (audio) {
        // Load the music state from local storage
        var musicOn = localStorage.getItem("musicOn");

        if (musicOn === "true") {
            // Play the audio if music is on
            audio.volume = 0.5;
            audio.play();
        }

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

        // Add an event listener for the "ended" event
        audio.addEventListener("ended", function () {
            // Refresh the src to play a new song or restart the same one
            audio.src = "/random_song.mp3";
            audio.load();
            audio.play();
        });
    }

    function toggleMusic() {
        if (audio) {
            var musicOn = localStorage.getItem("musicOn");

            if (musicOn === "playing already") {
                // Turn off the music
                audio.pause();
                localStorage.setItem("musicOn", "false");
            } else {
                // Turn on the music
                audio.volume = 0.5;
                audio.play();
                localStorage.setItem("musicOn", "playing already");

                // Save the current time when leaving the page
                window.addEventListener("beforeunload", function () {
                    localStorage.setItem("audioTime", audio.currentTime);
                });
            }
        }
    }

    // Add an event listener for the button click to toggle music
    var toggleButton = document.getElementById("toggleButton");
    if (toggleButton) {
        toggleButton.addEventListener("click", function (event) {
            // Prevent the click event from propagating to the document
            event.stopPropagation();
            toggleMusic();
        });
    }
});
