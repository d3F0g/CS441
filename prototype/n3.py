import socket
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
HOST='127.0.0.1'
PORT=7773
client.connect((HOST,PORT))
msg=client.recv(1024)
msg=msg.decode('utf-8')
print(msg)
while True:
 msg=input("Enter your message:")
 msg=msg.encode("utf-8")
 client.send(msg)