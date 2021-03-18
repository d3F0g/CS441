# Import socket module  
import socket              
  
# Create a socket object  
s = socket.socket() 
socket_port = 65433
s.bind(('127.0.0.1', socket_port))         
  

# Define the port on which you want to connect  
port = 12346               
# connect to r2 
s.connect(('127.0.0.1', port))  
  
# receive data from r1  
print (s.recv(1024) ) 
# close the connection  
s.close()    