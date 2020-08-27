const MOTION_THREESHOLD = 20
let socket;

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
    var isListening = false;
    var lastOrder = 'stop';
    var order = undefined;
    $(document).bind('touchstart mousedown', function() {
        isListening = true;
        console.log('start listening');
    });

    $(document).bind('touchend mouseup', function() {
        isListening = false;
        sendNewOrder('stop');
        lastOrder = 'stop';
        console.log('stop listening');
    });


    setInterval(function() {
        if (!isListening) return; // not listening for events. 
        let deltaX = joystick.deltaX();
        let deltaY = joystick.deltaY();
        if (!orderTriggered(deltaX, deltaY)) {
            // motion does not hit threeshold. 
            order = "stop";
        } else {
            if (Math.abs(deltaX) > Math.abs(deltaY)) {
                // right or left
                order = deltaX > 0 ? "right" : "left";
            } else {
                // up or down
                order = deltaY > 0 ? "down" : "up";
            }
        }
        if (order !== lastOrder) {
            sendNewOrder(order)
            lastOrder = order;
        }

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

function orderTriggered(x, y) {
    return (Math.abs(x) > MOTION_THREESHOLD) || (Math.abs(y) > MOTION_THREESHOLD);
}

function sendNewOrder(o) {
    console.log("--> new order: " + o);
    socket.send('message', o);
}

function connectToSocket(server) {
    socket = io.connect('http://' + server + ':5000', { 'forceNew': true });

    socket.on('message', function(data) {
        console.log('JavaScript client connected');
        console.log(data);
    });

    socket.send('message', "information from JavaScript");
}