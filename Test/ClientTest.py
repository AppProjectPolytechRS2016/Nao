'''
Created on 20 mars 2015

@author: NATHAN
'''

import socket

host = "193.48.125.68"
port = 6030

connection_with_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection_with_server.connect((host, port))

print("Client connected to Server on port {}".format(port))

msg_to_send = b""

while msg_to_send != b"fin":
    msg_to_send = input("> ")
    msg_to_send = msg_to_send.encode()
    connection_with_server.send(msg_to_send)
    msg_received = connection_with_server.recv(1024)
    print(msg_received.decode())
    
print("Closing connection")
connection_with_server.close()