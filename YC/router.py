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

    # ping from N1 to N2
    eth_frame = "N1R111[N1N205HELLO]" # Ethernet frame should be [source|dest|data length|(source|destination|protocol|5|HELLO)]

    start = False 
    ip_packet = ""

    if eth_frame[2:4]=="R1":

        #check for nodes inside r1nodes
        if eth_frame[:2] in r1nodes:

            for char in eth_frame: #extracts the ip packet from the eth frame
                if char == "]":
                    start = False # end of "ip packet"
                if start:
                    ip_packet += char
                if char == "[":
                    start = True #check for start of the "ip packet"

            if ip_packet[2:4] in r2nodes: #if the destination is valid

                eth_frame = "R2" + ip_packet[2:4] + eth_frame[4:] #replaces source to r2, dest to n2
                # print(eth_frame)
                # print(ip_packet)
                clientsocket.send(bytes(eth_frame,"utf-8"))
            else:
                print("This is not a registered route1")

        else:
            print("Node does not exist on this route")

    elif eth_frame[2:4]=="R2":
        #check for nodes inside r2nodes
        
        if eth_frame[:2] in r2nodes:

            for char in eth_frame:
                if char == "[":
                    start = True 
                elif char == "]":
                    start = False 
                if start:
                    ip_packet += char

            if ip_packet[2:4] in r1nodes: 
                eth_frame = eth_frame.replace(eth_frame[:2], "R1") 
                eth_frame = eth_frame.replace(eth_frame[2:4], ip_packet[2:4])
                clientsocket.send(bytes(eth_frame,"utf-8"))
            else:
                print("This is not a registered route")

        else:
            print("Node does not exist on this route")

    else:
        print("This is not a registered port")
    
    clientsocket.close()