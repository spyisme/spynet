// Function to generate a random 8-digit id
function generateRandomId() {
    return Math.floor(10000000 + Math.random() * 90000000).toString();
}

// Function to get or create a device ID
function getDeviceId() {
    let deviceId = localStorage.getItem('deviceId');
    if (!deviceId) {
        deviceId = generateRandomId();
        localStorage.setItem('deviceId', deviceId);
    }
    return deviceId;
}

// Get the device ID
var deviceId = getDeviceId();

var socket = io.connect('https://' + document.domain + ':' + location.port);

socket.on('connect', function() {
    socket.emit('register', { user: deviceId });
});

socket.on('refresh', function () {
    console.log('Received refresh signal. Reloading page...');
    location.reload();
});

socket.on('login', function(data) {
    console.log('Received login signal. Reloading page with token...');
    window.location.replace(`/loginfromqr?token=${data.token}&username=${data.username}`);
});


socket.on('msg', function(data) {
    alert(`Recived ${data}`)
});



// Function to check username
function checkUsername() {
    const storedUsername = localStorage.getItem('username');

    // Send a request to the server with the stored username
    fetch('/check_username', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username: storedUsername })
    })
    .then(response => response.json())
    .then(data => {
        if (data.logout) {
            // If server suggests logout, clear cookies and redirect to login
            console.log('Username mismatch. Logging out...');
            document.cookie.split(";").forEach(function(c) {
                document.cookie = c.trim().split("=")[0] + '=;expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
            });
            localStorage.clear();
            window.location.replace('/login');
        }
    });
}

// Check username every refresh
checkUsername()