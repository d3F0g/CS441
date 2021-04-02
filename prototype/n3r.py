import socket
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
HOST='127.0.0.1'
PORT=7773
server.bind((HOST,PORT))
server.listen(1)
print("socket is waiting for client......")
connection,address=server.accept()
print(address," got connected.")
msg="Welcome"
msg=msg.encode('utf-8')
connection.send(msg)
while True:
    request=connection.recv(1024)
    request=request.decode('utf-8')
    print(request)