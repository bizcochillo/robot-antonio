class Robot:
    def __init__(self):
        try:
            import RPi.GPIO as GPIO
        except RuntimeError:
            print("Error importing RPi.GPIO!  This must be run as root using sudo")
        self.GPIO = GPIO
        self.GPIO.setmode(GPIO.BCM)
        #I-B: Iquierda para detras
        self.GPIO.setup(17, GPIO.OUT)
        #I-F. Iquierda para adelante
        self.GPIO.setup(18, GPIO.OUT)
        #D-B Derecha para atras
        self.GPIO.setup(22, GPIO.OUT)
        #D-F
        self.GPIO.setup(23, GPIO.OUT)


    def up(self):
        self.GPIO.output(17, False)
        self.GPIO.output(18, True)
        self.GPIO.output(22, False)
        self.GPIO.output(23, True)


    def down(self):
        self.GPIO.output(17, True)
        self.GPIO.output(18, False)
        self.GPIO.output(22, True)
        self.GPIO.output(23, False)

    def left(self):
        self.GPIO.output(17, False)
        self.GPIO.output(18, True)
        self.GPIO.output(22, False)
        self.GPIO.output(23, False)

    def right(self):
        self.GPIO.output(17, False)
        self.GPIO.output(18, False)
        self.GPIO.output(22, False)
        self.GPIO.output(23, True)


    def stop(self):
        self.GPIO.output(17, False)
        self.GPIO.output(18, False)
        self.GPIO.output(22, False)
        self.GPIO.output(23, False)
    def getch(self):
        import sys, tty, termios
        old_settings = termios.tcgetattr(0)
        new_settings = old_settings[:]
        new_settings[3] &= ~termios.ICANON
        try:
            termios.tcsetattr(0, termios.TCSANOW, new_settings)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(0, termios.TCSANOW, old_settings)
        return ch
    def action(self, order):
        print("Robot> " + order)
        method = getattr(self, order, lambda:'Invalid')
        return method()

class RobotFake(Robot):
    def __init__(self):
        print("Init fake Robot class")
     
    def up(self):
        print("Robot> UP")

    def back(self):
        print("Robot> BACK")

    def left(self):
        print("Robot> LEFT")

    def right(self):
        print("Robot> RIGHT")


    def stop(self):
        print("Robot> STOP")

    def getch(self):
        print("Robot> GETCH")


from flask import Flask
from flask_socketio import SocketIO

try:
    import commands 
    server = commands.getoutput('hostname -I').strip()
    robot = Robot()
except ImportError:
    server = "127.0.0.1"
    robot = RobotFake()

import json

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)

@socketio.on('message')
def test_message(message, payload):
    print("Handler> " + payload)
    robot.action(payload)

@socketio.on('connect')
def test_connect():
    print('++++ User connected ++++')
    socketio.emit('message', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print('---- User disconnected ----')

if __name__ == '__main__':    
    with open("./static/config.json", "r") as jsonFile:
        data = json.load(jsonFile)

    data["server"] = server

    with open("./static/config.json", "w") as jsonFile:
        json.dump(data, jsonFile)
    print("Endpoint: http://" + server + ":5000/static/index.html")
    socketio.run(app, host='0.0.0.0')