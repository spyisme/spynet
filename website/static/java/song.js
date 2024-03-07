// Song.js
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
        audio.src = "/random_song";
        audio.load();
        audio.play();
    });
}

function toggleMusic() {
    if (audio) {
        var musicOn = localStorage.getItem("musicOn");

        if (musicOn === "true") {
            // Turn off the music
            audio.pause();
            localStorage.setItem("musicOn", "false");
        } else {
            // Turn on the music
            audio.volume = 0.5;
            audio.play();
            localStorage.setItem("musicOn", "true");
        }

        // Save the current time when leaving the page
        window.addEventListener("beforeunload", function () {
            localStorage.setItem("audioTime", audio.currentTime);
        });
    }
}

// Add an event listener for the "click" event to toggle music
document.addEventListener("click", function () {
    toggleMusic();
    // Remove the click event listener after toggling music
    document.removeEventListener("click", toggleMusic);
});
