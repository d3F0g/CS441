#! python2
import sys
import socket
import select
from datetime import datetime

def logger(filename, msg):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    f = open(filename, "a")
    f.write(dt_string + "\n" + msg)
    f.close()


def frame(whoami, whereto, protocol, msg):
    ### START of Ethernet Frame
    source = whoami
    destination = 'R1'
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
 
def chat_client():
    if(len(sys.argv) < 3) :
        print 'Usage : python chat_client.py hostname port'
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 10101))
    s.settimeout(2)
     
    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print 'Unable to connect'
        sys.exit()
     
    print 'Connected to router. You are N1.\n<dest> <protocol> <message>'
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
                s.send(frame('N1', msg.split(' ')[0], msg.split(' ')[1], msg.split(' ')[2]))
                if msg.split(' ')[1]=="0":
                    sys.stdout.write('[reply] '+msg.split(' ')[2]); sys.stdout.flush() 
                elif msg.split(' ')[1]=="1":
                    if msg.split(' ')[0]=="N3": #N2 receives log packet to N3 as well
                        logger('N2.txt', frame('N1', msg.split(' ')[0], msg.split(' ')[1], msg.split(' ')[2]))
                    logger(msg.split(' ')[0]+'.txt', frame('N1', msg.split(' ')[0], msg.split(' ')[1], msg.split(' ')[2]))
                sys.stdout.write('[Me] '); sys.stdout.flush() 

if __name__ == "__main__":

    sys.exit(chat_client())