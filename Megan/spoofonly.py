#IP Spoofing
from scapy.all import send, IP, ICMP
spoofed_IPsource='N3' #spoofed source IP address: we are N2 pretending to be N3 so as to send to N1
IPdestination = '127.0.0.1' #destination IP address
sourceport = 65432
destinationport = 65431
payload = "this is a message"
# spoofed_packet = IP(src=spoofed_IPsource, dst=sys.argv[1]) / TCP(sport=sourceport, dport=destinationport) / payload
spoofed_packet2 = IP(src=spoofed_IPsource, dst='N1') / ICMP() /payload
answer = send(spoofed_packet2)

if answer:
    answer.show()
    
#reference: https://stackoverflow.com/questions/27448905/send-packet-and-change-its-source-ip
#reference 2: https://github.com/balle/python-network-hacks/blob/master/ip-spoofing.py
#reference 3: https://stackoverflow.com/questions/38555263/spoofing-ip-address-without-any-external-module-via-python
#ARP spoofing/poisoning: https://www.tutorialspoint.com/python_penetration_testing/python_penetration_testing_arp_spoofing.htm
