import sys
# Import socket module  
import socket              
  
# Create a socket object  
s = socket.socket() 
socket_port = 65433
s.bind(('127.0.0.1', socket_port))    

if len(sys.argv) != 4:
    print("usage: python3", sys.argv[0], "<dest> <protocol> <message>")
    sys.exit(1)
  

# Define the port on which you want to connect  
port = 12346               
# connect to r2 
s.connect(('127.0.0.1', port))  
  
### START of Ethernet Frame
source = 'N3'
destination = 'R2'
## START of IP frame
IPsource = 'N3'
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
# receive data from r2  
print (s.recv(1024) ) 
# close the connection  
s.close()    


# This will recreate the socket object to send to R1 as well
s = socket.socket() 
socket_port = 65432
s.bind(('127.0.0.1', socket_port))
# connect to r1
s.connect(('127.0.0.1', 12345)) 
s.send(bytes(ethernet_frame, encoding='utf8'))
# receive data from r2  
print (s.recv(1024) ) 
# close the connection  
s.close()  