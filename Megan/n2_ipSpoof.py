import sys
# Import socket module  
import socket              
  
# Create a socket object  
s = socket.socket() 
socket_port = 65432
s.bind(('127.0.0.1', socket_port))         

if len(sys.argv) != 4:
    print("usage: python3", sys.argv[0], "<dest> <protocol> <message>")
    sys.exit(1)

# Define the port on which you want to connect  
port = 12346                 
# connect to r2
s.connect(('127.0.0.1', port))  
  
### START of Ethernet Frame
source = 'N2'
spoofed_source='N3'
destination = 'R2'
## START of IP frame
IPsource = 'N2'
spoofed_IPsource='N3'

IPdestination = sys.argv[1]
IPprotocol = sys.argv[2]
IPdata = sys.argv[3]
IPdatalength = str(len(IPdata))

if IPdestination == 'N1':
    IPframe = spoofed_IPsource + IPdestination + IPprotocol + IPdatalength + '|' + IPdata
else:
    IPframe = IPsource + IPdestination + IPprotocol + IPdatalength + '|' + IPdata
## END of IP frame
datalength = str(len(IPframe)-1)

#combine them to form the ethernet frame
if IPdestination =='N1':
    ethernet_frame = spoofed_source + destination + datalength + '|' + IPframe
else:
    ethernet_frame = source + destination + datalength + '|' + IPframe
### END of ethernet frame

s.send(bytes(ethernet_frame, encoding='utf8'))
# receive data from r2  
print (s.recv(1024) ) 
# close the connection  
s.close()    