import socket
import json

server = socket.gethostbyname(socket.gethostname())
with open("./static/config.json", "r") as jsonFile:
    data = json.load(jsonFile)

data["server"] = server

with open("./static/config.json", "w") as jsonFile:
    json.dump(data, jsonFile)