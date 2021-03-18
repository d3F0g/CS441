# first of all import the socket library  
import socket              
  
# next create a socket object  
s = socket.socket()          
print ("Router 1 successfully created") 
  
# reserve a port on your computer in our  
# case it is 12345 but it can be anything  
port = 12345                
  
# Next bind to the port  
# we have not typed any ip in the ip field  
# instead we have inputted an empty string  
# this makes the server listen to requests  
# coming from other computers on the network  
s.bind(('127.0.0.1', port))          
print ("Router 1 binded to %s" %(port))  
  
# put the socket into listening mode  
s.listen(5)      
print ("Router 1 is listening") 

  
# a forever loop until we interrupt it or  
# an error occurs  
while True:  
  
    # Establish connection with client.  
    c, addr = s.accept()      
    print ('Got connection from', addr ) 
    
    # send a thank you message to the client.  
    c.send(b'Thank you for connecting, message sent!, R1')
    data = c.recv(261)

    #if data has been sent to this router
    if data: 
        print(data)

    # Close the connection with the client  
    c.close() 