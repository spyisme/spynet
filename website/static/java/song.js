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

// Add an event listener for the "ended" event to reset music state
audio.addEventListener("ended", function () {
    localStorage.setItem("musicOn", "false");
});

// Add an event listener for the "click" event to toggle music
document.addEventListener("click", function () {
    toggleMusic();
});
