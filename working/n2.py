#! python2
import sys
import socket
import select
from datetime import datetime
from helpers import encryptor, decryptor

def logger(filename, msg):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    f = open(filename, "a")
    f.write(dt_string + "\n" + msg)
    f.close()

def peerframe(whoami, whereto, protocol, msg):
    ### START of Ethernet Frame
    source = whoami
    destination = whereto
    ## START of IP frame
    IPsource = whoami
    IPdestination = whereto
    IPprotocol = protocol
    IPdata = msg
    IPdatalength = str(len(IPdata))
    IPframe = IPsource + IPdestination + IPprotocol + IPdatalength + '|' + IPdata
    ## END of IP frame
    datalength = str(len(IPframe)-1)

    #combine them to form the ethernet frame
    ethernet_frame = source + destination + datalength + '|' + IPframe
    ### END of ethernet frame
    return ethernet_frame

def frame(whoami, whereto, protocol, msg):
    ### START of Ethernet Frame
    source = whoami
    destination = 'R2'
    ## START of IP frame
    IPsource = whoami
    IPdestination = whereto
    IPprotocol = protocol
    IPdata = msg
    IPdatalength = str(len(IPdata))
    IPframe = IPsource + IPdestination + IPprotocol + IPdatalength + '|' + IPdata
    ## END of IP frame
    datalength = str(len(IPframe)-1)

    #combine them to form the ethernet frame
    ethernet_frame = source + destination + datalength + '|' + IPframe
    ### END of ethernet frame
    return ethernet_frame
 
 
def node_start():
    if(len(sys.argv) < 3) :
        print 'Usage : python n2.py hostname port'
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 10102))
    s.settimeout(2)
     
    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print 'Unable to connect'
        sys.exit()
     
    print 'Connected to router. You are N2.\n<dest> <protocol> <message>'
    sys.stdout.write('[Me] '); sys.stdout.flush()
     
    while 1:
        socket_list = [sys.stdin, s]
         
        # Get the list sockets which are readable
        ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])
         
        for sock in ready_to_read:             
            if sock == s:
                # incoming message from router, s
                data = sock.recv(4096)
                if not data :
                    print '\nDisconnected from router'
                    sys.exit()
                else :
                    #print data
                    sys.stdout.write(data)
                    sys.stdout.write('[Me] '); sys.stdout.flush()   
            
            else :
                # user entered a message
                msg = sys.stdin.readline()
                if msg.split(' ')[0]=="N1": #this will be N2 impersonating N3 everytime msg is sent to N1
                    s.send(frame('N3', msg.split(' ')[0], msg.split(' ')[1], encryptor(msg.split(' ')[2]))) 
                else:
                    s.send(peerframe('N2', msg.split(' ')[0], msg.split(' ')[1], encryptor(msg.split(' ')[2])))
                if msg.split(' ')[1]=="0":
                    if msg.split(' ')[0]=="N3":
                        pass
                    elif msg.split(' ')[0]=="N1":
                        # sys.stdout.write('[N1] '+ frame('N1', 'N3', '0', msg.split(' ')[2])); sys.stdout.flush() 
                        pass
                    else:
                        sys.stdout.write('[reply] '+encryptor(msg.split(' ')[2])); sys.stdout.flush() 
                elif msg.split(' ')[1]=="1":
                    if msg.split(' ')[0]=="N3":
                        pass
                    else:
                        logger('router.txt', frame('N2', msg.split(' ')[0], msg.split(' ')[1], msg.split(' ')[2]))
                        logger(msg.split(' ')[0]+'.txt', frame('N2', msg.split(' ')[0], msg.split(' ')[1], msg.split(' ')[2]))
                sys.stdout.write('[Me] '); sys.stdout.flush() 

if __name__ == "__main__":

    sys.exit(node_start())