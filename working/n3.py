#! python2
import sys
import socket
import select
from datetime import datetime
from helpers import encryptor, decryptor
import random
import string

def random_string(n): #number of characters for that random string
    chars = string.ascii_letters
    return ''.join(random.choice(chars) for i in range(n))

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
        print 'Usage : python n3.py hostname port'
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 10103))
    s.settimeout(2)
     
    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print 'Unable to connect'
        sys.exit()
     
    print 'Connected to router. You are N3.\n<dest> <protocol> <message>'
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
                if msg.split(' ')[0]=="N2": #if intended to send to N2 then must be without router dest
                    s.send(peerframe('N3', msg.split(' ')[0], msg.split(' ')[1], encryptor(msg.split(' ')[2])))
                else:
                    s.send(frame('N3', msg.split(' ')[0], msg.split(' ')[1], encryptor(msg.split(' ')[2])))
                if msg.split(' ')[1]=="0":
                    if msg.split(' ')[0]=="N2":
                        pass
                    else:
                        sys.stdout.write('[reply] '+encryptor(msg.split(' ')[2])); sys.stdout.flush() 
                elif msg.split(' ')[1]=="1":
                    if msg.split(' ')[0]=="N1": #N2 receives log packet to N1 as well 
                        logger('sniffed.txt', frame('N3', msg.split(' ')[0], msg.split(' ')[1], msg.split(' ')[2]))
                        logger('N1.txt', frame('N3', msg.split(' ')[0], msg.split(' ')[1], msg.split(' ')[2]))
                        logger('router.txt', frame('N3', msg.split(' ')[0], msg.split(' ')[1], msg.split(' ')[2]))
                        # logger(msg.split(' ')[0]+'.txt', frame('N3', msg.split(' ')[0], msg.split(' ')[1], (random_string(3)+msg.split(' ')[2]+random_string(5)).replace("\n", "")))
                    elif msg.split(' ')[0]=="N2":
                        logger('N2.txt', frame('N3', msg.split(' ')[0], msg.split(' ')[1], msg.split(' ')[2]))
                    
                sys.stdout.write('[Me] '); sys.stdout.flush() 

if __name__ == "__main__":

    sys.exit(node_start())