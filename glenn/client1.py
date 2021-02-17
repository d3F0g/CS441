import socket
import time 
client1_ip = "0x1A"
client1_mac = "32:04:0A:EF:19:CF"
router = ("localhost", 8200)
client1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
time.sleep(1)
client1.connect(router)
print("client1.py")
print(client1_ip)
print(client1_mac)
while True:
    received_message = client1.recv(1024)
    received_message = received_message.decode("utf-8")
    print("rc: " + received_message)
    fragments = received_message.split("|")
    print(*fragments)
    print()
    print("fragments 0 is: " + fragments[0])
    print("source mac is: " + fragments[0])
    print("destimation mac is: " + fragments[1])
    print("source ip is: " + fragments[2])
    print("destination ip is: " + fragments[3])
    print("protocol is: " + fragments[4])
    print("datalength is: " + fragments[5])
    print("message is: " + fragments[6])
    source_mac = fragments[0]
    destination_mac = fragments[1]
    source_ip = fragments[2]
    destination_ip =  fragments[3]
    protocol = fragments[4]
    datalength = fragments[5]
    message = fragments[6]

    source_mac = ""
    source_ip = ""
    destination_mac = ""
    destination_ip = ""
    message = ""

    print("\nPacket integrity:\ndestination MAC address matches client 1 MAC address: {mac}".format(mac=(client1_mac == destination_mac)))
    print("\ndestination IP address matches client 1 IP address: {mac}".format(mac=(client1_ip == destination_ip)))
    print("\nThe packed received:\n Source MAC address: {source_mac}, Destination MAC address: {destination_mac}".format(source_mac=source_mac, destination_mac=destination_mac))
 
    print("\nSource IP address: {source_ip}, Destination IP address: {destination_ip}".format(source_ip=source_ip, destination_ip=destination_ip))
 
    print("\nMessage: " + message)