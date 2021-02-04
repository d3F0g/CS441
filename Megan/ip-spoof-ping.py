#here we are pretending to be node 2, who is ip spoofing as node 3 to ping node 1
from scapy.all import *

iface = "en0"
fake_ip = '92.10.10.25' #this is node 3's ip, the spoofed address
destination_ip = '92.10.10.15' #this is node 1, the destination address
router_mac = "05:10:0A:CB:24:EF" #this is node 1, the destination mac

destination_ip_test= '10.124.20.36'
    
def original_ping(source, destination, iface):
    pkt = IP(src=source,dst=destination)/ICMP()
    srloop(IP(src=source,dst=destination)/ICMP(), iface=iface)
    #iface: interface or list of interfaces (default: None for sniffing on all interfaces). 
    #this one, en0 means ethernet interface

def ping(source,destination):
    #srloop to loop through the packets and check % of hits
    #https://0xbharath.github.io/art-of-packet-crafting-with-scapy/scapy/sending_recieving/index.html#srloop
    srloop(IP(src=source, dst=destination)/ICMP()/"test message from ip spoof")

try:
    print ("Starting Ping")
    # original_ping(fake_ip,destination_ip_test,iface)
    ping(fake_ip, destination_ip_test)
    print("Message sent.")
except:
    KeyboardInterrupt:print("Exiting... ")
    sys.exit(0)