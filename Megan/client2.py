import socket
import time
from scapy.all import *

client2_ip = "92.10.10.20"
client2_mac = "10:AF:CB:EF:19:CF"
router = ("localhost", 8200)
client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
time.sleep(1)
client2.connect(router)

#for our project, we want node 2 to pretend to be node 3 so as to ping node 1
spoofed_ip = '92.10.10.25' #this is node 3's ip, the spoofed address
#the ip and mac below are node 1's, which is the destination address 
destination_ip = '92.10.10.15'
destination_mac = "32:04:0A:EF:19:CF"

# while True:
#     received_message = client2.recv(1024)
#     received_message = received_message.decode("utf-8")
#     source_mac = received_message[0:17]
#     destination_mac = received_message[17:34]
#     source_ip = received_message[34:45]
#     destination_ip =  received_message[45:56]
#     message = received_message[56:]
#     print("\nPacket integrity:\ndestination MAC address matches client 2 MAC address: {mac}".format(mac=(client2_mac == destination_mac)))
#     print("\ndestination IP address matches client 2 IP address: {mac}".format(mac=(client2_ip == destination_ip)))
#     print("\nThe packed received:\n Source MAC address: {source_mac}, Destination MAC address: {destination_mac}".format(source_mac=source_mac, destination_mac=destination_mac))
#     print("\nSource IP address: {source_ip}, Destination IP address: {destination_ip}".format(source_ip=source_ip, destination_ip=destination_ip))
#     print("\nMessage: " + message)

while True:
    routerConnection, address = client2.accept()
    if(routerConnection != None):
        print(routerConnection)
        break

#hardcoded for now
while True:
    ethernet_header = ""
    IP_header = ""
    
    message = input("\nEnter the text message to send: ")
    destination_ip = "92.10.10.15"
    if(destination_ip == "92.10.10.15"):
        source_ip = client2_ip
        IP_header = IP_header + source_ip + destination_ip
        
        source_mac = client2_mac
        destination_mac = destination_mac 
        ethernet_header = ethernet_header + source_mac + destination_mac
        
        packet = ethernet_header + IP_header + message
        
        routerConnection.send(bytes(packet, "utf-8"))  
    else:
        print("That's not Client 1!")