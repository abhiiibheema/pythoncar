import socket as  s
def server():
    host ='192.168.2.2' 
    port =3000
    socketobj = s.socket(s.AF_INET,s.SOCK_STREAM)
    socketobj.bind((host,port))
    socketobj.listen(2)
    c,address = socketobj.accept()
    print(f"conntected to :{address}")
    while True:
        data = c.recv(1024).decode()
        if not data:
            break 
        print(f"Recieved from client: {data}")

        responce  = input("ENTER A DATA TO send ")
        c.send(responce.encode())
    c.close()
if __name__ == '__main__':
    server()