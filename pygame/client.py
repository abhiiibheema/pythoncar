import socket as s 
def client():
    host='192.168.2.7'
    port = 3000
    client_socket  = s.socket()
    client_socket.connect((host,port))
    message = input("Enter some message")
    while True:
        client_socket.send(message.encode())
        data=client_socket.recv(1024).decode()
        print(f"message from the server {data}")
        message = input("enter a message")
    client_socket.close()
if __name__ == "__main__":
    client()