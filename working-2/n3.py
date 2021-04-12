import sys
import socket
import select
import helpers
 
def chat_client():
    if(len(sys.argv) < 3) :
        print('Usage : python n3.py hostname port')
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
        print('Unable to connect')
        sys.exit()
     
    print 'Connected to router. You are N3.\n<dest> <protocol> <message>'
    sys.stdout.write('[Me] '); sys.stdout.flush()
     
    while 1:
        socket_list = [sys.stdin, s]
         
        # Get the list sockets which are readable
        ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])
         
        for sock in ready_to_read:             
            if sock == s:
                # incoming message from remote server, s
                data = sock.recv(4096)
                if not data :
                    print('\nDisconnected from router')
                    sys.exit()
                else :
                    #print data
                    sys.stdout.write(data)
                    sys.stdout.write('[Me] '); sys.stdout.flush()     
            
            else :
                # user entered a message
                msg = sys.stdin.readline()
                dest = msg.split(' ')[0]
                protocol = msg.split(' ')[1]
                message = msg.split(' ')[2]
                if dest == 'N1':
                    s.send(helpers.frame('N3', '0x2B', 'R2', dest, protocol, message)) 
                    helpers.logger('sniff_logs.txt', helpers.frame('N3', '0x2B', 'R2', dest, protocol, message))
                    if protocol == "0":
                        print '[reply] '+helpers.frame('R2', helpers.node_to_IP(dest), 'N3', "N3", protocol, message)
                else:
                    #basically if its being sent to N2
                   s.send(helpers.frame('N3', '0x2B', 'N2', dest, protocol, message)) 

                sys.stdout.write('[Me] '); sys.stdout.flush() 

if __name__ == "__main__":

    sys.exit(chat_client())