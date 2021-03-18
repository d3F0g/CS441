import sys
# Import socket module  
import socket              
  
# Create a socket object  
s = socket.socket() 
socket_port = 65431
s.bind(('127.0.0.1', socket_port))         
  
if len(sys.argv) != 4:
    print("usage: python3", sys.argv[0], "<dest> <protocol> <message>")
    sys.exit(1)

                 
# connect to r1 
s.connect(('127.0.0.1', 12345))  

### START of Ethernet Frame
source = 'N1'
destination = 'R1'
## START of IP frame
IPsource = 'N1'
IPdestination = sys.argv[1]
IPprotocol = sys.argv[2]
IPdata = sys.argv[3]
IPdatalength = str(len(IPdata))
IPframe = IPsource + IPdestination + IPprotocol + IPdatalength + '|' + IPdata
## END of IP frame
datalength = str(len(IPframe)-1)

#combine them to form the ethernet frame
ethernet_frame = source + destination + datalength + '|' + IPframe
### END of ethernet frame

s.send(bytes(ethernet_frame, encoding='utf8'))
# receive data from r1  
print (s.recv(1024) ) 
# close the connection  
s.close()   


# This will recreate the socket object to send to both R1 and R2 
s = socket.socket() 
socket_port = 65431
s.bind(('127.0.0.1', socket_port))
# connect to r2
s.connect(('127.0.0.1', 12346)) 
s.send(bytes(ethernet_frame, encoding='utf8'))
# receive data from r2  
print (s.recv(1024) ) 
# close the connection  
s.close()   