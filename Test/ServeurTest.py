'''
Created on 20 mars 2015

@author: NATHAN
'''

import socket

host = ''
port = 12800

main_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
main_connection.bind((host, port))
main_connection.listen(5)

print("Server is now listenning to port {}".format(port))

connection_with_client, connection_info = main_connection.accept()

received_msg = b""

while received_msg != b"fin":
    received_msg = connection_with_client.recv(1024)
    print(received_msg.decode())
    connection_with_client.send(b"5 / 5")

print("Closing connections")
connection_with_client.close()
main_connection.close()