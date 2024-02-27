import socket as  s
def server():
    host = s.gethostname()
    print(host)
    port =9000
    socketobj = s.socket()
    socketobj.bind((host,port))
    socketobj.listen(2)
    c,address = socketobj.accept()
    print(f"conntected to :{address}")
    while True:
        data = c.recv(1024).decode()
        if not data:
            break 
        print(f"Recieved from client: {data}")

        responce  = input("ENTER A DATA TO send")
        c.send(responce.encode())
        c.close()
if __name__ == '__main__':
    server()