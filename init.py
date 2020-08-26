from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)

@socketio.on('message')
def test_message(message, payload):
    print(payload)   

@socketio.on('connect')
def test_connect():
    print('++++ User connected ++++')
    socketio.emit('message', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print('---- User disconnected ----')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')