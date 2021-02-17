import socket
import time
client3_ip = "0x2B"
client3_mac = "AF:04:67:EF:19:DA"
router = ("localhost", 8200)
client3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
time.sleep(1)
client3.connect(router)
print("client3.py")
print(client3_ip)
print(client3_mac)
while True:
    received_message = client3.recv(1024)
    # ethernet_frame = "0x1A|0x2A|0|5|HELLO"
    
    # ethernet_frame_components = ethernet_frame.split('|')
    # source = ethernet_frame_components[0]
    # dest = ethernet_frame_components[1]
    # protocol = ethernet_frame_components[2]
    # data_length = ethernet_frame_components[3]
    # data = ethernet_frame_components[4]

    received_message = received_message.decode("utf-8")
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

    print("\nPacket integrity:\ndestination MAC address matches client 3 MAC address: {mac}".format(mac=(client3_mac == destination_mac)))
    
    print("\ndestination IP address matches client 3 IP address: {mac}".format(mac=(client3_ip == destination_ip)))
    
    print("\nThe packed received:\n Source MAC address: {source_mac}, Destination MAC address: {destination_mac}".format(source_mac=source_mac, destination_mac=destination_mac))
    print("\nSource IP address: {source_ip}, Destination IP address: {destination_ip}".format(source_ip=source_ip, destination_ip=destination_ip))
    print("\nMessage: " + message)