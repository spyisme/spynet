document.addEventListener('DOMContentLoaded', loadLectures);

function loadLectures() {

    var xhr = new XMLHttpRequest();
    var url = "https://api.csacademyzone.com/lectures";

    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.setRequestHeader("sessionToken", "ss");

    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                // Parse JSON response
                var data = JSON.parse(xhr.responseText);

                // Initialize array for filtered lectures
                var filteredLectures = [];

                // Iterate over lectures in the response data
                data.lectures.forEach(function(lecture) {
                    var filteredLecture = {
                        "id": lecture.id,
                        "title": lecture.title
                    };

                    // Check for video parts using ASCII lowercase letters
                    for (var i = 0; i < 26; i++) {
                        var partKey = "part_" + String.fromCharCode(97 + i) + "_video";
                        if (lecture.hasOwnProperty(partKey) && lecture[partKey]) {
                            filteredLecture[partKey] = lecture[partKey];
                        }
                    }

                    // Check for PDF link
                    if (lecture.hasOwnProperty('pdf') && lecture.pdf) {
                        filteredLecture['pdf'] = lecture.pdf;
                    }

                    // Push filtered lecture into array
                    filteredLectures.push(filteredLecture);
                });

                // Sort lectures by ID in ascending order
                filteredLectures.sort((a, b) => a.id - b.id);

                // Prepare result object
                var lectures = {
                    "filtered_lectures": filteredLectures
                };
                console.log("Filtered Lectures:", lectures.filtered_lectures);

                populateLectureDropdown(lectures.filtered_lectures);
                populateParts(lectures.filtered_lectures[0]); // Initialize with the first lecture's parts

                if (lectures.filtered_lectures.length > 0) {
                    var lastLectureTitle = lectures.filtered_lectures[lectures.filtered_lectures.length - 1].title;
                    document.getElementById("lastLectureTitle").innerText = "Last lecture uploaded  : " + lastLectureTitle;
                }


            } else {
                console.error('Request failed. Status:', xhr.status);
            }
        }
    };

    xhr.send();

}

function populateLectureDropdown(filteredLectures) {
    var lectureDropdown = document.getElementById("lectureIdInput");
    if (!lectureDropdown) {
        console.error('Lecture dropdown element not found');
        return;
    }
    lectureDropdown.innerHTML = ''; // Clear any existing options

    filteredLectures.forEach((lecture) => {
        var option = document.createElement('option');
        option.value = lecture.id;
        option.textContent = "Lecture " + lecture.id + " : " + lecture.title;
        lectureDropdown.appendChild(option);
    });

    lectureDropdown.addEventListener('change', function() {
        const selectedLecture = filteredLectures.find(lecture => lecture.id === this.value);
        populateParts(selectedLecture);
    });
}

function populateParts(lecture) {
    var playButtonContainer = document.getElementById("playButtonContainer");
    var videoPlayer = document.getElementById("videoPlayer");
    if (!playButtonContainer || !videoPlayer) {
        console.error('Parts container or video player element not found');
        return;
    }
    playButtonContainer.innerHTML = ''; // Clear any existing parts

    Object.keys(lecture).forEach(key => {
        if (key.startsWith('part_') && key.endsWith('_video')) {
            var partLetter = key.charAt(5).toUpperCase();
            var playButton = document.createElement('button');
            playButton.className = 'play-btn';
            playButton.textContent = `Play Part ${partLetter}`;
            playButton.id = key;
            playButton.addEventListener('click', function() {
                loadVideo(lecture[key], key);
            });
            playButtonContainer.appendChild(playButton);
        }
    });

    if (lecture.pdf) {
        var pdfButton = document.createElement('button');
        pdfButton.className = 'pdf-btn';
        pdfButton.textContent = 'Open PDF';
        pdfButton.id = 'pdfButton';
        pdfButton.addEventListener('click', function() {
            window.open("https://csacademyzone-pdfs.s3.eu-central-1.amazonaws.com/" + lecture.pdf, '_blank');
        });
        playButtonContainer.appendChild(pdfButton);
    }

    document.querySelector('h3').innerText = `${lecture.title}`;
    document.querySelector('h1').innerText = 'Click a part to play!';
    document.getElementById('videoPlayer').src = '';
}

function loadVideo(videoId, partId) {
    var videoPlayer = document.getElementById("videoPlayer");

    var xhr = new XMLHttpRequest();
    var url = "https://api.csacademyzone.com/video/otp";

    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.setRequestHeader("Referer", "https://csacademyzone.com/");
    xhr.setRequestHeader("sec-fetch-dest", "empty");
    xhr.setRequestHeader("sec-fetch-mode", "cors");
    xhr.setRequestHeader("sessionToken", "ss");

    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            var response = JSON.parse(xhr.responseText);
            var otp = response.otp;
            var playbackInfo = response.playbackInfo;

            videoPlayer.src = `https://player.vdocipher.com/v2/?otp=${otp}&playbackInfo=${playbackInfo}`;
        }
    };

    var data = JSON.stringify({
        'student_name': '-',
        'video_id': videoId
    });

    xhr.send(data);

    var partLetter = partId.charAt(5).toUpperCase();
    document.querySelector('h1').innerText = `Lecture ${document.getElementById("lectureIdInput").value} Part ${partLetter}`;

    var allButtons = document.querySelectorAll(".play-btn");
    allButtons.forEach(button => {
        button.classList.remove("clicked");
    });

    var clickedButton = document.getElementById(partId);
    if (clickedButton) {
        clickedButton.classList.add("clicked");
    }
}
