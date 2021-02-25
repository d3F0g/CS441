# this is the brain that decides the network line
import socket

r1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
r1.bind((socket.gethostbyname('localhost'), 1234))
r1.listen(1)

r2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
r2.bind((socket.gethostbyname('localhost'), 1235))
r2.listen(2)

router_mac = "05:10:0A:CB:24:EF"
node1_ip = "0x1A"
node1_mac = "32:04:0A:EF:19:CF"
node2_ip = "0x1B"
node2_mac = "10:AF:CB:EF:19:CF"
node3_ip = "0x2B"
node3_mac = "AF:04:67:EF:19:DA"

while True:
    #router needs a message receiving component
    #need to pack as ip packet, and THEN pack into ethernet frame
    #ip packet looks like source-dest-protocol-datalength-data
    #ethernet packet looks like source-dest-datalength-data

    # incomingmsg = destroute + sourcenode + destnode + protocol + messagelength + '|' +  messageinput
    incomingmsg = "R2N1N205HELLO"

    #ip packet
    ip_source = incomingmsg[2:4]
    ip_dest = incomingmsg[4:6]
    ip_prot = incomingmsg[7]
    symbol_position = incomingmsg.find("|")
    ip_length = incomingmsg[8:symbol_position]
    ip_msg = incomingmsg[incomingmsg+1:]

    full_ip = ip_source + ip_dest + ip_prot + ip_length + ip_msg
    
    #ethernetpacket
    if ip_dest == 'N1':
        eth_source = 'R1'
    else:
        eth_source = 'R2'
    eth_dest = incomingmsg[:2]
    eth_length = len(full_ip)
    
    full_eth = eth_source + eth_dest + eth_length + full_ip

    #message sending component
    clientsocket, address = r1.accept()
    clientsocket, address = r2.accept()
    print(f"Connection from {address} has been established.")

    r1nodes = ['N1']
    r2nodes = ['N2', 'N3']
    
    if eth_dest=="R1":
        #check for nodes inside r1nodes
        if ip_dest in r1nodes:
            clientsocket.send(bytes(full_eth,"utf-8"))
        else:
            print("Node does not exist on this route")

    elif eth_dest=="R2":
        #check for nodes inside r2nodes
        if ip_dest in r2nodes:
            clientsocket.send(bytes(full_eth,"utf-8"))
        else:
            print("Node does not exist on this route")
    else:
        print("This is not a registered route")

    clientsocket.close()