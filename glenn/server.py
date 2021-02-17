import socket
client1_ip = "0x1A"
client2_ip = "0x2A"
client3_ip = "0x2B"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 8005))
server.listen(2)
server_ip = "92.10.10.10"
server_mac = "00:00:0A:BB:28:FC"
router_mac = "05:10:0A:CB:24:EF"
print("server.py")
print(server_ip)
print(server_mac)
while True:
    routerConnection, address = server.accept()
    if(routerConnection != None):
        print(routerConnection)
        break
while True:
    ethernet_header = ""
    IP_header = ""
    protocol = ""
    datalength = ""
    
    message = input("\nEnter the text message to send: ")
    destination_ip = input("Enter the IP of the clients to send the message to:\n1. " + client1_ip +"\n2. " + client2_ip +"\n3. " + client3_ip +"\n")
    protocol = input("So what you want to do with this message? ")
    if(destination_ip == "0x1A" or destination_ip == "0x2A" or destination_ip == "0x2B"):
        source_ip = server_ip
        IP_header = IP_header + "|" + source_ip + "|" + destination_ip
        
        source_mac = server_mac
        destination_mac = router_mac 
        ethernet_header = ethernet_header + "|" + source_mac + "|" + destination_mac
        
        # packet = ethernet_header + IP_header + message
        datalength = len(message)

        packet = ethernet_header + IP_header +"|" + protocol +"|" + str(datalength) +"|" + message
        print(packet)
        routerConnection.send(bytes(packet, "utf-8"))  
    else:
        print("Wrong client IP inputted")