const MOTION_THREESHOLD = 20
let socket;

$(document).ready(function() {
    $.getJSON('config.json', function(data) {
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

    socket.on('message', function(received) {
        $("robot_status")
        console.log("Received from server>");
        if (received.data == "Connected") {
            $("#robot_status").removeClass("status-offline")
            $("#robot_status").addClass("status-online")
            $("#robot_status").text("online");
        }
    });

    socket.onerror = function(event) {
        $("#robot_status").removeClass("status-online")
        $("#robot_status").addClass("status-offline")
        $("#robot_status").text("offline");
    };

}