#!/usr/bin/python

from scapy.all import *
import socket
import datetime
import os
import argparse
from geoip import geolite2
import time

def network_monitoring_for_visualization_version(pkt):
	time=datetime.datetime.now()
		#classifying packets into TCP
	if pkt.haslayer(IP):
		if "127.0.0.1" == pkt[IP].dst or "127.0.0.1" == pkt[IP].src :
			print(str("[")+str(time)+str("]")+"    "+"SRC-MAC:" +str(pkt.src)+"    "+ "DST-MAC:"+str(pkt.dst)+"    "+ "SRC-PORT:"+str(pkt.sport)+"    "+"DST-PORT:"+str(pkt.dport)+"    "+"SRC-IP:"+str(pkt[IP].src  )+"    "+"DST-IP:"+str(pkt[IP].dst  ))
	if pkt.haslayer(TCP):
		# print("start")
		# print(pkt[IP].dst)
		# print(pkt[IP].src)
		# print(socket.gethostbyname(socket.gethostname()))
		# classyfying packets into TCP Incoming packets
		if "127.0.0.1" == pkt[IP].dst:
		#print(str("[")+str(time)+str("]")+"  "+"TCP-IN:{}".format(len(pkt[TCP]))+" Bytes"+"    "+"SRC-MAC:" +str(pkt.src)+"    "+ "DST-MAC:"+str(pkt.dst)+"    "+ "SRC-PORT:"+str(pkt.sport)+"    "+"DST-PORT:"+str(pkt.dport)+"    "+"SRC-IP:"+str(pkt[IP].src  )+"    "+"DST-IP:"+str(pkt[IP].dst  )+"  " +"Location:" +geolite2.lookup(pkt[IP].src).timezone)
			print(str("[")+str(time)+str("]")+"  "+"TCP-IN:{}".format(len(pkt[TCP]))+" Bytes"+"    "+"SRC-MAC:" +str(pkt.src)+"    "+ "DST-MAC:"+str(pkt.dst)+"    "+ "SRC-PORT:"+str(pkt.sport)+"    "+"DST-PORT:"+str(pkt.dport)+"    "+"SRC-IP:"+str(pkt[IP].src  )+"    "+"DST-IP:"+str(pkt[IP].dst  ))
	
		if "127.0.0.1"==pkt[IP].src:
			print(str("[")+str(time)+str("]")+"  "+"TCP-OUT:{}".format(len(pkt[TCP]))+" Bytes"+"    "+"SRC-MAC:" +str(pkt.src)+"    "+ "DST-MAC:"+str(pkt.dst)+"    "+ "SRC-PORT:"+str(pkt.sport)+"    "+"DST-PORT:"+str(pkt.dport)+"    "+"SRC-IP:"+str(pkt[IP].src)+"    "+"DST-IP:"+str(pkt[IP].dst))
	#classifying packets into UDP	
	if pkt.haslayer(UDP):
		if socket.gethostbyname(socket.gethostname())==pkt[IP].src:
			# classyfying packets into UDP Outgoing packets
			print(str("[")+str(time)+str("]")+"  "+"UDP-OUT:{}".format(len(pkt[UDP]))+" Bytes "+"    "+"SRC-MAC:" +str(pkt.src)+"    "+"DST-MAC:"+ str(pkt.dst)+"    "+"SRC-PORT:"+ str(pkt.sport) +"    "+"DST-PORT:"+ str(pkt.dport)+"    "+"SRC-IP:"+ str(pkt[IP].src)+"    "+"DST-IP:"+ str(pkt[IP].dst))
	
		if socket.gethostbyname(socket.gethostname())==pkt[IP].dst:
			# classyfying packets into UDP Incoming packets
			print(str("[")+str(time)+str("]")+"  "+"UDP-IN:{}".format(len(pkt[UDP]))+" Bytes "+"    "+"SRC-MAC:" +str(pkt.src)+"    "+"DST-MAC:"+ str(pkt.dst)+"    "+"SRC-PORT:"+ str(pkt.sport) +"    "+"DST-PORT:"+ str(pkt.dport)+"    "+"SRC-IP:"+ str(pkt[IP].src)+"    "+"DST-IP:"+ str(pkt[IP].dst))
		#classifying packets into ICMP
	if pkt.haslayer(ICMP):
		# classyfying packets into UDP Incoming packets
		if socket.gethostbyname(socket.gethostname())==pkt[IP].src:
			print(str("[")+str(time)+str("]")+"  "+"ICMP-OUT:{}".format(len(pkt[ICMP]))+" Bytes"+"    "+"IP-Version:"+str(pkt[IP].version) +"    "*1+" SRC-MAC:"+str(pkt.src)+"    "+"DST-MAC:"+str(pkt.dst)+"    "+"SRC-IP: "+str(pkt[IP].src)+ "    "+"DST-IP:  "+str(pkt[IP].dst))	
							
		if socket.gethostbyname(socket.gethostname())==pkt[IP].dst:
			print(str("[")+str(time)+str("]")+"  "+"ICMP-IN:{}".format(len(pkt[ICMP]))+" Bytes"+"    "+"IP-Version:"+str(pkt[IP].version)+"    "*1+"	 SRC-MAC:"+str(pkt.src)+"    "+"DST-MAC:"+str(pkt.dst)+"    "+"SRC-IP: "+str(pkt[IP].src)+ "    "+"DST-IP:  "+str(pkt[IP].dst))	

# def get_interface():
#     parser = argparse.ArgumentParser()
#     parser.add_argument("-i", "--interface", dest="interface", help="Specify interface on which to sniff packets")
#     arguments = parser.parse_args()
#     return arguments.interface

# def sniffing(iface):
#     sniff(iface=iface, store=False, prn=network_monitoring_for_visualization_version)

# iface = get_interface()
# sniffing(iface)

if __name__ == '__main__':
	sniff(store=False, prn=network_monitoring_for_visualization_version)