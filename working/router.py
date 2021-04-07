#! python2
import sys
import socket
import select

HOST = '' 
SOCKET_LIST = []
RECV_BUFFER = 4096 
PORT = 9009

def onlySeeMsg(data):
    return data.split('|')[2]

def whoIsWho(portNumber):
    if portNumber==10101:
        return "N1"
    elif portNumber==10102:
        return "N2"
    elif portNumber==10103:
        return "N3"


def router_on():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)
 
    # add server socket object to the list of readable connections
    SOCKET_LIST.append(server_socket)
 
    print "Router started on port " + str(PORT)
 
    while 1:

        # get the list sockets which are ready to be read through select
        # 4th arg, time_out  = 0 : poll and never block
        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)
      
        for sock in ready_to_read:
            # a new connection request recieved
            if sock == server_socket: 
                sockfd, addr = server_socket.accept()
                SOCKET_LIST.append(sockfd)
                print whoIsWho(addr[1]) +" connected"
                 
                broadcast(server_socket, sockfd, whoIsWho(addr[1])+" is online\n")
             
            # a message from a client, not a new connection
            else:
                # process data recieved from client, 
                try:
                    # receiving data from the socket.
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        # there is something in the socket
                        if data.split('|')[1][4]=="0": #if the protocol is ping
                            if data.split('|')[1][2:4]=="N1": #if the intended recipient is N1
                                #then send only to N1
                                if data.split('|')[1][:2]=="N3": # N2 sniffs N3 communications
                                    broadcast(server_socket, sock, "\r" + '[' + whoIsWho(sock.getpeername()[1]) + '] ' + data)
                                else:
                                    targeted(server_socket, sock, "\r" + '[' + whoIsWho(sock.getpeername()[1]) + '] ' + data, 1)
                            elif data.split('|')[1][2:4]=="N2": #if the intended recipient is N2
                                #then send only to N2
                                targeted(server_socket, sock, "\r" + '[' + whoIsWho(sock.getpeername()[1]) + '] ' + data, 2)
                                # broadcast(server_socket, sock, "\r" + '[' + whoIsWho(sock.getpeername()[1]) + '] ' + data)  
                            elif data.split('|')[1][2:4]=="N3": #if the intended recipient is N3
                                #then send only to N3
                                if data.split('|')[1][:2]=="N2": # N3 packet filter
                                    pass #N3 does not accept N2 packets with ping protocol
                                else:
                                    # targeted(server_socket, sock, "\r" + '[' + whoIsWho(sock.getpeername()[1]) + '] ' + data, 3)
                                    broadcast(server_socket, sock, "\r" + '[' + whoIsWho(sock.getpeername()[1]) + '] ' + data) #N2 sniffs N3 comms 

                        elif data.split('|')[1][4]=="2": #if the protocol is kill
                            if data.split('|')[1][2:4]=="N1": #if the intended recipient is N1
                                killconnection(server_socket, sock, 1)
                                print "Connection to N1 closed"
                            elif data.split('|')[1][2:4]=="N2": #if the intended recipient is N2
                                killconnection(server_socket, sock, 2)
                                print "Connection to N2 closed"
                            elif data.split('|')[1][2:4]=="N3": #if the intended recipient is N3
                                pass #N3 does not accept kill packets from N1 and N2
                            
                        
                    else:
                        # remove the socket that's broken    
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)

                        # at this stage, no data means probably the connection has been broken
                        broadcast(server_socket, sock, whoIsWho(addr[1]) +" is offline\n") 

                # exception 
                except:
                    broadcast(server_socket, sock, whoIsWho(addr[1]) +" is offline\n")
                    continue

    server_socket.close()
    
# broadcast messages to all connected nodes
# this should only be for N1
def broadcast (server_socket, sock, message):
    for socket in SOCKET_LIST:
        # send the message only to peer
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)

def targeted (server_socket, sock, message, clientNumber):
    # send the message only to a specific client
    socket = SOCKET_LIST[clientNumber]
    if socket != server_socket and socket != sock :
        try :
            socket.send(message)
        except :
            # broken socket connection
            socket.close()
            # broken socket, remove it
            if socket in SOCKET_LIST:
                SOCKET_LIST.remove(socket)

def killconnection(server_socket, sock, clientNumber):
    socket = SOCKET_LIST[clientNumber]
    if socket != server_socket and socket != sock :
        if socket in SOCKET_LIST:
            SOCKET_LIST.remove(socket)
            socket.close()

 
if __name__ == "__main__":

    sys.exit(router_on())  