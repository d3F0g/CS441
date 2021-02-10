from scapy.all import *
import socket
import datetime
import os
from geoip import geolite2
import time

if __name__ == '__main__':
	print(sniff(count=10,filter = "host 92.10.10.15"))