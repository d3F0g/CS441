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
destination = 'R2'
## START of IP frame
IPsource = 'N2'

#IP Spoofing
from scapy.all import send, IP, ICMP
spoofed_IPsource='N3' #spoofed source IP address: we are N2 pretending to be N3 so as to send to N1
IPdestination = sys.argv[1] #destination IP address
sourceport = 12346
destinationport = 65431
payload = "this is a message"
# spoofed_packet = IP(src=spoofed_IPsource, dst=sys.argv[1]) / TCP(sport=sourceport, dport=destinationport) / payload
spoofed_packet2 = IP(src=spoofed_IPsource, dst=sys.argv[1]) / ICMP() /payload
answer = send(spoofed_packet2)

if answer:
    answer.show()

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


#reference: https://stackoverflow.com/questions/27448905/send-packet-and-change-its-source-ip
#reference 2: https://github.com/balle/python-network-hacks/blob/master/ip-spoofing.py