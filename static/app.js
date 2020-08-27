$(document).ready(function() {
    $.getJSON('config.json', function(data) {
        //HERE YOu need to get the name server
        return data.server;
    }).done(data => connectToSocket(data.server));

    console.log("touchscreen is", VirtualJoystick.touchScreenAvailable() ? "available" : "not available");

    var joystick = new VirtualJoystick({
        container: document.getElementById('container'),
        mouseSupport: true,
    });
    joystick.addEventListener('touchStart', function() {
        console.log('down')
    })
    joystick.addEventListener('touchEnd', function() {
        console.log('up')
    })

    setInterval(function() {
        var outputEl = document.getElementById('result');
        outputEl.innerHTML = '<b>Result:</b> ' +
            ' dx:' + joystick.deltaX() +
            ' dy:' + joystick.deltaY() +
            (joystick.right() ? ' right' : '') +
            (joystick.up() ? ' up' : '') +
            (joystick.left() ? ' left' : '') +
            (joystick.down() ? ' down' : '')
    }, 1 / 30 * 1000);
});

function connectToSocket(server) {
    var socket = io.connect('http://' + server + ':5000', { 'forceNew': true });

    socket.on('message', function(data) {
        console.log('JavaScript client connected');
        console.log(data);
    });

    socket.send('message', "information from JavaScript");
}