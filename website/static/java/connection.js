var socket = io.connect('https://' + document.domain + ':' + location.port);

socket.on('refresh', function () {
    console.log('Received refresh signal. Reloading page...');
    location.reload();
});