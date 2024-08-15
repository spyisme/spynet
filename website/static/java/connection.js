// Function to generate a random 8-digit ID
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