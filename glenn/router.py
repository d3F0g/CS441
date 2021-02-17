import socket
import time

router = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
router.bind(("localhost", 8100))

router_send = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
router_send.bind(("localhost", 8200))

router_mac = "05:10:0A:CB:24:EF"

server = ("localhost", 8005)

client1_ip = "0x1A"
client1_mac = "32:04:0A:EF:19:CF"
client2_ip = "0x1B"
client2_mac = "10:AF:CB:EF:19:CF"
client3_ip = "0x2B"
client3_mac = "AF:04:67:EF:19:DA"
router_send.listen(4)
client1 = None
client2 = None
client3 = None
while (client1 == None or client2 == None or client3 == None):
    client, address = router_send.accept()
    
    if(client1 == None):
        client1 = client
        print("Client 1 is online")
    
    elif(client2 == None):
        client2 = client
        print("Client 2 is online")
    else:
        client3 = client
        print("Client 3 is online")
arp_table_socket = {client1_ip : client1, client2_ip : client2, client3_ip : client3}
arp_table_mac = {client1_ip : client1_mac, client2_ip : client2_mac, client3_ip : client3_mac}
router.connect(server)
print("router.py")
print(router_mac)
while True:
    received_message = router.recv(1024)
    received_message =  received_message.decode("utf-8")
    # print(received_message)

    fragments = received_message.split("|")
    
    print("fragments 0 is: " + fragments[0])
    print("source mac is: " + fragments[1])
    print("destimation mac is: " + fragments[2])
    print("source ip is: " + fragments[3])
    print("destination ip is: " + fragments[4])
    print("protocol is: " + fragments[5])
    print("datalength is: " + fragments[6])
    print("message is: " + fragments[7])

    # source_ip = ""
    # source_mac = ""
    # destination_ip = ""
    # destination_mac = ""

    source_mac = fragments[1]
    destination_mac = fragments[2]
    source_ip = fragments[3]
    destination_ip =  fragments[4]
    protocol = fragments[5]
    datalength = fragments[6]
    message = fragments[7]
    
    print("The packed received:\n Source MAC address: {source_mac}, Destination MAC address: {destination_mac}".format(source_mac=source_mac, destination_mac=destination_mac))
    print("\nSource IP address: {source_ip}, Destination IP address: {destination_ip}".format(source_ip=source_ip, destination_ip=destination_ip))
    print("\nMessage: " + message)
    print()
    
    ethernet_header = router_mac + "|" + arp_table_mac[destination_ip]
    print("ethernet header: " + ethernet_header)
    IP_header = source_ip + "|" + destination_ip
    print("ip header: " + IP_header)
    packet = ethernet_header + "|" + IP_header + "|" + protocol + "|" +  datalength + "|" +  message
    
    
    print("packet: " + packet)
    
    destination_socket = arp_table_socket[destination_ip]
    
    print("destination_socket: " + destination_ip)
    
    destination_socket.send(bytes(packet, "utf-8"))
    time.sleep(2)