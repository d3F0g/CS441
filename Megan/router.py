# this is the brain that decides the network line
import socket

r1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
r1.bind((socket.gethostbyname('localhost'), 1234))
r1.listen(1)

r2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
r2.bind((socket.gethostbyname('localhost'), 1235))
r2.listen(2)

while True:
    # now our endpoint knows about the OTHER endpoint.
    clientsocket, address = r1.accept()
    clientsocket, address = r2.accept()
    print(f"Connection from {address} has been established.")

    r1nodes = ['N1']
    r2nodes = ['N2', 'N3']

    msg = "R1N25Hello"
    
    if msg[:2]=="R1":
        #check for nodes inside r1nodes
        if msg[2:4] in r1nodes:
            clientsocket.send(bytes(msg,"utf-8"))
        else:
            print("Node does not exist on this route")

    elif msg[:2]=="R2":
        #check for nodes inside r2nodes
        if msg[2:4] in r2nodes:
            clientsocket.send(bytes(msg,"utf-8"))
        else:
            print("Node does not exist on this route")
    else:
        print("This is not a registered route")
    
    clientsocket.close()