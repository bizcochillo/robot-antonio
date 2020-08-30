Python Server (Flask with SocketIO) and JavaScript client based on VirtualJoystick (credits to https://github.com/jeromeetienne/virtualjoystick.js) and jQuery. 
Chassis (credits to  http://www.penguintutor.com/electronics/dcmotor-control) with two engines managed by a python server running on a Raspberry PI. 

The server raises and endpoint on http://server_address:5000/static/index.html which is JS based. The JS client collects motion orders by providing a JS joystick  and sends them to the server via a WebSocket channel.

Modification to start Antonio-Z automatically. File /etc/rc.local in Raspberry PI.  
(sleep 10;cd /home/pi/robot;python init.py)
