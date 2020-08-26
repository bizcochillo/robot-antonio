$(document).ready(function() {
    var server = $.getJSON('config.json', function(data) {
        //HERE YOu need to get the name server
        return data.server;
    }).done(data => connectToSocket(data.server));
});

function connectToSocket(server) {
    var socket = io.connect('http://' + server + ':5000', { 'forceNew': true });

    socket.on('message', function(data) {
        console.log('JavaScript client connected');
        console.log(data);
    });

    socket.send('message', "information from JavaScript");
}