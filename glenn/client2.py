import socket
import time
client2_ip = "0x1B"
client2_mac = "10:AF:CB:EF:19:CF"
router = ("localhost", 8200)
client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
time.sleep(1)
client2.connect(router)
print("client2.py")
print(client2_ip)
print(client2_mac)
while True:
    received_message = client2.recv(1024)
    received_message = received_message.decode("utf-8")
    # print(received_message)
    # source_mac = received_message[0:1]
    # destination_mac = received_message[1:2]
    # source_ip = received_message[2:3]
    # destination_ip =  received_message[3:4]
    # message = received_message[4:]

    fragments = received_message.split("|")
    
    # print("fragments 0 is: " + fragments[0])
    print("source mac is: " + fragments[1])
    print("destimation mac is: " + fragments[2])
    print("source ip is: " + fragments[3])
    print("destination ip is: " + fragments[4])
    # print("protocol is: " + fragments[5])
    # print("datalength is: " + fragments[6])
    # print("message is: " + fragments[7])
    source_mac = fragments[1]
    destination_mac = fragments[2]
    source_ip = fragments[3]
    destination_ip =  fragments[4]
    # protocol = fragments[5]
    # datalength = fragments[6]
    # message = fragments[7]
    message = ""


    print("\nPacket integrity:\ndestination MAC address matches client 2 MAC address: {mac}".format(mac=(client2_mac == destination_mac)))
    print("\ndestination IP address matches client 2 IP address: {mac}".format(mac=(client2_ip == destination_ip)))
    print("\nThe packed received:\n Source MAC address: {source_mac}, Destination MAC address: {destination_mac}".format(source_mac=source_mac, destination_mac=destination_mac))
    print("\nSource IP address: {source_ip}, Destination IP address: {destination_ip}".format(source_ip=source_ip, destination_ip=destination_ip))
    print("\nMessage: " + message)