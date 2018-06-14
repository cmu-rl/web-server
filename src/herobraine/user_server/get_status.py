import sys
import json
import time
import socket
import hashlib

HOST, PORT = "18.206.147.166", 9999
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(2)

# get_status returns a dictionary
'''
typical response of get_status
{"timestamp": "06_08_18_15_09", "banned": false, "awesome": true, 
 "queue_position": 120, "message": "...", "error": false}
'''
def get_status(username):
    data = {}
    data['cmd'] = 'get_status'
    data['uid'] = username
    sock.sendto(bytes(json.dumps(data), "utf-8"), (HOST, PORT))
    received = str(sock.recv(1024), "utf-8")
    print("Sent:     {}".format(data))
    print("Received: {}".format(received))
    status = json.loads(received) 
return status
