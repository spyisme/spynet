const lecturesData = {{ lectures|tojson }};  // Pass the lectures data from Flask to JS

    function loadlec() {
        const selectedLectureId = document.getElementById('dropdown').value;
        const resultsContainer = document.getElementById('results');
        cleariframe();  // Hide iframe before new selection

        // Show loading message while processing
        resultsContainer.innerHTML = 'Loading...';

        // Find the selected lecture by ID
        const selectedLecture = lecturesData.find(lecture => lecture.lecture_id == selectedLectureId);

        if (selectedLecture) {
            displayResults(selectedLecture.units);
        } else {
            alert("Lecture not found!");
            resultsContainer.innerHTML = '';  // Clear loading message if no lecture found
        }
    }

    function displayResults(units) {
        const resultsContainer = document.getElementById('results');
        resultsContainer.innerHTML = '';  // Clear existing results

        // Iterate over units and generate links
        units.forEach(item => {
            const [id, description, type] = item;
            const url = `/subjects/english/theleader/session/${type}/${id}`;

            // Create a clickable link
            const itemDiv = document.createElement('div');
            itemDiv.className = 'result-item';
            itemDiv.innerHTML = type === "video"
              ? `<a href="javascript:void(0);" onclick="updateIframe('${url}', 'video')"><strong>${description}</strong> (${type})</a>`
              : `<a href="${url}" target="_blank"><strong>${description}</strong> (${type})</a>`;

            resultsContainer.appendChild(itemDiv);
        });

        cleariframe();  // Keep the iframe hidden until a video is selected
    }

    function updateIframe(url, type) {
    const iframeContainer = document.getElementById('iframeContainer');
    let contentFrame = document.getElementById('contentFrame');

    console.log("Updating iframe with URL:", url); // Log the URL

    if (!contentFrame) {
        contentFrame = document.createElement('iframe');
        contentFrame.id = 'contentFrame';
        contentFrame.allowFullscreen = true;
        contentFrame.style.width = '100%';
        contentFrame.style.height = '600px';
        contentFrame.style.border = '1px solid #ddd';
        contentFrame.style.borderRadius = '5px';
        iframeContainer.appendChild(contentFrame);  
    }

    // Set the iframe source
    contentFrame.src = url;  // This sets the source of the iframe
    console.log("Iframe src set to:", contentFrame.src); // Log the iframe src

    // Optionally listen for iframe load event
    contentFrame.onload = function() {
        console.log("Iframe content loaded");
        hideLoadingMessage(iframeContainer); // Hide loading message when loaded
    };

    iframeContainer.style.display = 'block';  
}


    function showLoadingMessage(container, message, color = 'gray') {
        container.innerHTML = '';  // Clear previous content
        const loadingMessage = document.createElement('div');
        loadingMessage.style.fontSize = '24px';
        loadingMessage.style.color = color;
        loadingMessage.style.textAlign = 'center';
        loadingMessage.style.padding = '50px';
        loadingMessage.innerText = message;
        container.appendChild(loadingMessage);
    }

    function cleariframe() {
        // Remove existing iframe if it exists
        const existingIframe = document.getElementById('contentFrame');
        if (existingIframe) {
            iframeContainer.removeChild(existingIframe);
        }
    }