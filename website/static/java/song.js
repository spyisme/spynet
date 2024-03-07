var audio = document.getElementById("backgroundAudio");



var musicOn = localStorage.getItem("musicOn");



function toggle(){
    console.log("ss")
    if (musicOn === "true") {
        localStorage.setItem("musicOn", "false");
        location.reload();
    }
    if (musicOn === "false") {
        localStorage.setItem("musicOn", "true");
        location.reload();
    }

}

if (musicOn === "true") {
        // Check if the audio element exists on the page
        if (audio) {
            // Play the audio as soon as the script loads
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

            // Add an event listener for the "ended" event
            audio.addEventListener("ended", function () {
                // Refresh the src to play a new song or restart the same one
                audio.src = "/random_song";
                audio.load();
                audio.play();
            });
        }

        function playAudio() {
            if (audio) {
                audio.volume = 0.5;
                audio.play();

                // Save the current time when leaving the page
                window.addEventListener("beforeunload", function () {
                    localStorage.setItem("audioTime", audio.currentTime);
                });
            }
        }

        document.addEventListener("click", function () {
            playAudio();
            // Remove the click event listener after playing the audio
            document.removeEventListener("click", playAudio);
        });
}