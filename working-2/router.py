import sys
import socket
import select
import helpers
import json
from collections import OrderedDict

HOST = '' 
SOCKET_LIST = []
RECV_BUFFER = 4096 
PORT = 9009

def chat_server():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)
 
    # add server socket object to the list of readable connections
    SOCKET_LIST.append(server_socket)
 
    print("Router started on port " + str(PORT))
 
    while 1:

        # get the list sockets which are ready to be read through select
        # 4th arg, time_out  = 0 : poll and never block
        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)
      
        for sock in ready_to_read:
            # a new connection request recieved
            if sock == server_socket: 
                sockfd, addr = server_socket.accept()
                SOCKET_LIST.append(sockfd)
                print helpers.whoIsWho(addr[1])+" connected" 
                 
                broadcast(server_socket, sockfd, helpers.whoIsWho(addr[1])+" is online\n")
             
            # a message from a client, not a new connection
            else:
                # process data recieved from client, 
                try:
                    # receiving data from the socket.
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        # there is something in the socket
                        
                        #check protocol first 
                        if json.loads(data)["Protocol"] == "0":
                            #if going to N1
                            if json.loads(data)["IPdest"] == "0x1A":
                                #print data that arrived
                                spoofed = json.loads(data, object_pairs_hook=OrderedDict)
                                spoofed["source"] = "N3"
                                spoofed["IPsource"] = "0x2B"
                                print json.dumps(spoofed, indent=4)
                                helpers.logger("router.txt", json.dumps(spoofed))
                                #print router forwarded packet
                                new = json.loads(data, object_pairs_hook=OrderedDict)
                                new["source"] = "R2"
                                new["ethernet_dest"] = "R1"
                                new["IPsource"] = "0x2B"
                                print json.dumps(new, indent=4)
                                helpers.logger("router.txt", json.dumps(new))
                                #print the sent out packet
                                new["source"] = "R1"
                                new["ethernet_dest"] = "N1"
                                print json.dumps(new, indent=4)
                                helpers.logger("router.txt", json.dumps(new))
                                #send the packet to N1
                                converted = json.loads(data, object_pairs_hook=OrderedDict)
                                converted["source"] = "R1"
                                converted["ethernet_dest"] = "N1"
                                converted["IPsource"] = "0x2B"
                                targeted(server_socket, sock, "\r" + '[' + helpers.whoIsWho(sock.getpeername()[1]) + '] ' + json.dumps(converted, indent=4)+'\n', 1)
                                #print reply packet
                                reply = json.loads(data, object_pairs_hook=OrderedDict)
                                reply["IPsource"] = "0x1A"
                                reply["IPdest"] = "0x2B"
                                reply["source"] = "N1"
                                reply["ethernet_dest"] = "R1"
                                print json.dumps(reply, indent=4)
                                helpers.logger("router.txt", json.dumps(reply))
                                #print router forwarded reply packet
                                reply_forwarded = json.loads(data, object_pairs_hook=OrderedDict)
                                reply_forwarded["IPsource"] = "0x1A"
                                reply_forwarded["IPdest"] = "0x2B"
                                reply_forwarded["source"] = "R1"
                                reply_forwarded["ethernet_dest"] = "R2"
                                print json.dumps(reply_forwarded, indent=4)
                                helpers.logger("router.txt", json.dumps(reply_forwarded))
                                #print sent out reply
                                reply_forwarded["source"] = "R2"
                                reply_forwarded["ethernet_dest"] = "N3"
                                targeted(server_socket, sock, "\r" + '[' + 'reply' + '] ' + json.dumps(reply_forwarded, indent=4)+'\n', 3)
                                print json.dumps(reply_forwarded, indent=4)
                                helpers.logger("router.txt", json.dumps(reply_forwarded))
                            
                            #if going to N2
                            elif json.loads(data)["IPdest"] == "0x2A":
                                #if it came from N1
                                if json.loads(data)["source"] == "N1":
                                    #print data that arrived
                                    print data
                                    formatted_str = json.loads(data, object_pairs_hook=OrderedDict)
                                    helpers.logger("router.txt", json.dumps(formatted_str))
                                    #print router forwarded packet
                                    new = json.loads(data, object_pairs_hook=OrderedDict)
                                    new["source"] = "R1"
                                    new["ethernet_dest"] = "R2"
                                    print json.dumps(new, indent=4)
                                    helpers.logger("router.txt", json.dumps(new))
                                    #print the sent out packet
                                    new["source"] = "R2"
                                    new["ethernet_dest"] = "N2"
                                    print json.dumps(new, indent=4)
                                    helpers.logger("router.txt", json.dumps(new))
                                    #send the packet to N2
                                    converted = json.loads(data, object_pairs_hook=OrderedDict)
                                    converted["source"] = "R2"
                                    converted["ethernet_dest"] = "N2"
                                    targeted(server_socket, sock, "\r" + '[' + helpers.whoIsWho(sock.getpeername()[1]) + '] ' + json.dumps(converted, indent=4)+'\n', 2)
                                    #print reply packet
                                    reply = json.loads(data, object_pairs_hook=OrderedDict)
                                    reply["IPsource"], reply["IPdest"] = reply["IPdest"], reply["IPsource"] #swap the IPsource and IPdest values
                                    reply["source"] = "N2"
                                    reply["ethernet_dest"] = "R2"
                                    print json.dumps(reply, indent=4)
                                    helpers.logger("router.txt", json.dumps(reply))
                                    #print router forwarded reply packet
                                    reply_forwarded = json.loads(data, object_pairs_hook=OrderedDict)
                                    reply_forwarded["IPsource"], reply_forwarded["IPdest"] = reply_forwarded["IPdest"], reply_forwarded["IPsource"] #swap the IPsource and IPdest values
                                    reply_forwarded["source"] = "R2"
                                    reply_forwarded["ethernet_dest"] = "R1"
                                    print json.dumps(reply_forwarded, indent=4)
                                    helpers.logger("router.txt", json.dumps(reply_forwarded))
                                    #print sent out reply
                                    reply_forwarded["source"] = "R1"
                                    reply_forwarded["ethernet_dest"] = "N1"
                                    print json.dumps(reply_forwarded, indent=4)
                                    helpers.logger("router.txt", json.dumps(reply_forwarded))
                                #if it came from N3
                                elif json.loads(data)["source"] == "N3":
                                    targeted(server_socket, sock, "\r" + '[' + helpers.whoIsWho(sock.getpeername()[1]) + '] ' + data, 2)
                            
                            #if going to N3
                            elif json.loads(data)["IPdest"] == "0x2B":
                                #if it came from N1
                                if json.loads(data)["source"] == "N1":
                                    #print data that arrived
                                    print data
                                    formatted_str = json.loads(data, object_pairs_hook=OrderedDict)
                                    helpers.logger("router.txt", json.dumps(formatted_str))
                                    #print router forwarded packet
                                    new = json.loads(data, object_pairs_hook=OrderedDict)
                                    new["source"] = "R1"
                                    new["ethernet_dest"] = "R2"
                                    print json.dumps(new, indent=4)
                                    helpers.logger("router.txt", json.dumps(new))
                                    #print the sent out packet
                                    new["source"] = "R2"
                                    new["ethernet_dest"] = "N3"
                                    print json.dumps(new, indent=4)
                                    helpers.logger("router.txt", json.dumps(new))
                                    #send the packet to N3
                                    converted = json.loads(data, object_pairs_hook=OrderedDict)
                                    converted["source"] = "R2"
                                    converted["ethernet_dest"] = "N3"
                                    targeted(server_socket, sock, "\r" + '[' + helpers.whoIsWho(sock.getpeername()[1]) + '] ' + json.dumps(converted, indent=4)+'\n', 3)
                                    #print reply packet
                                    reply = json.loads(data, object_pairs_hook=OrderedDict)
                                    reply["IPsource"], reply["IPdest"] = reply["IPdest"], reply["IPsource"] #swap the IPsource and IPdest values
                                    reply["source"] = "N3"
                                    reply["ethernet_dest"] = "R2"
                                    print json.dumps(reply, indent=4)
                                    helpers.logger("router.txt", json.dumps(reply))
                                    #print router forwarded reply packet
                                    reply_forwarded = json.loads(data, object_pairs_hook=OrderedDict)
                                    reply_forwarded["IPsource"], reply_forwarded["IPdest"] = reply_forwarded["IPdest"], reply_forwarded["IPsource"] #swap the IPsource and IPdest values
                                    reply_forwarded["source"] = "R2"
                                    reply_forwarded["ethernet_dest"] = "R1"
                                    print json.dumps(reply_forwarded, indent=4)
                                    helpers.logger("router.txt", json.dumps(reply_forwarded))
                                    #print sent out reply
                                    reply_forwarded["source"] = "R1"
                                    reply_forwarded["ethernet_dest"] = "N1"
                                    print json.dumps(reply_forwarded, indent=4)
                                    helpers.logger("router.txt", json.dumps(reply_forwarded))
                                #if it came from N2
                                    if json.loads(data)["source"] == "N2":
                                        pass #N3 firewall against N2



                    else:
                        # remove the socket that's broken    
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)

                        # at this stage, no data means probably the connection has been broken
                        broadcast(server_socket, sock, helpers.whoIsWho(addr[1])+" is offline\n") 

                # exception 
                except:
                    broadcast(server_socket, sock, helpers.whoIsWho(addr[1])+" is offline\n")
                    continue

    server_socket.close()
    
# broadcast chat messages to all connected clients
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

    sys.exit(chat_server())  