import socket

ClientMultiSocket = socket.socket()
ClientMultiSocket.bind(('127.0.0.1', 65432))
host = '127.0.0.1'
port = 2004

print('Waiting for connection response')
try:
    ClientMultiSocket.connect((host, port))
except socket.error as e:
    print(str(e))

res = ClientMultiSocket.recv(1024)
while True:
    msg = input('msg: ')
    ClientMultiSocket.send(str.encode(msg))
    res = ClientMultiSocket.recv(1024)
    print(res.decode('utf-8'))

ClientMultiSocket.close()