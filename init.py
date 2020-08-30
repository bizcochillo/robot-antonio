class Robot:
    MOVE_LEFT_AHEAD = 22
    MOVE_LEFT_BACK = 23
    MOVE_RIGHT_AHEAD = 18 
    MOVE_RIGHT_BACK = 17 

    def __init__(self):
        try:
            import RPi.GPIO as GPIO
        except RuntimeError:
            print("Error importing RPi.GPIO!  This must be run as root using sudo")
        self.GPIO = GPIO
        self.GPIO.setmode(GPIO.BCM)
        #I-B: Left back
        self.GPIO.setup(17, GPIO.OUT)
        #I-F. Left ahead
        self.GPIO.setup(18, GPIO.OUT)
        #D-B. Right back
        self.GPIO.setup(22, GPIO.OUT)
        #D-F. Right ahead
        self.GPIO.setup(23, GPIO.OUT)


    def up(self):
        self.GPIO.output(Robot.MOVE_RIGHT_AHEAD, True)        
        self.GPIO.output(Robot.MOVE_LEFT_BACK, False)        
        self.GPIO.output(Robot.MOVE_RIGHT_BACK, False)
        self.GPIO.output(Robot.MOVE_LEFT_AHEAD, True)

    def down(self):
        self.GPIO.output(Robot.MOVE_LEFT_BACK, True)
        self.GPIO.output(Robot.MOVE_LEFT_AHEAD, False)        
        self.GPIO.output(Robot.MOVE_RIGHT_AHEAD, False)
        self.GPIO.output(Robot.MOVE_RIGHT_BACK, True)

    def left(self):
        self.GPIO.output(Robot.MOVE_LEFT_AHEAD, False)
        self.GPIO.output(Robot.MOVE_LEFT_BACK, False)
        self.GPIO.output(Robot.MOVE_RIGHT_AHEAD, True)
        self.GPIO.output(Robot.MOVE_RIGHT_BACK, False)

    def right(self):
        self.GPIO.output(Robot.MOVE_LEFT_AHEAD, True)
        self.GPIO.output(Robot.MOVE_LEFT_BACK, False)
        self.GPIO.output(Robot.MOVE_RIGHT_AHEAD, False)
        self.GPIO.output(Robot.MOVE_RIGHT_BACK, False)

    def stop(self):
        self.GPIO.output(Robot.MOVE_LEFT_AHEAD, False)
        self.GPIO.output(Robot.MOVE_LEFT_BACK, False)
        self.GPIO.output(Robot.MOVE_RIGHT_AHEAD, False)
        self.GPIO.output(Robot.MOVE_RIGHT_BACK, False)

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

    def down(self):
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