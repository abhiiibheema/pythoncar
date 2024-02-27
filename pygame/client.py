import socket as s 
def client(a,b):
    host='192.168.2.2'
    port = 3000
    client_socket  = s.socket()
    client_socket.connect((host,port))
    cords = (a,b)
    while True:
        client_socket.send(cords.encode())
        data=client_socket.recv(1024).decode()
    client_socket.close()