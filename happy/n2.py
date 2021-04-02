import socket 
import argparse

parser = argparse.ArgumentParser(description = "This is the client for the multi threaded socket server!")
parser.add_argument('--host', metavar = 'host', type = str, nargs = '?', default = socket.gethostbyname('localhost'))
parser.add_argument('--port', metavar = 'port', type = int, nargs = '?', default = 9999)
args = parser.parse_args()

print(f"Connecting to server: {args.host} on port: {args.port}")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sck:
	sck.bind(('127.0.0.1', 65432))
	try:
		sck.connect((args.host, args.port))
	except Exception as e:
		raise SystemExit(f"We have failed to connect to host: {args.host} on port: {args.port}, because: {e}")

	while True:

		### START of Ethernet Frame
		source = 'N2'
		destination = 'R2'
		## START of IP frame
		IPsource = 'N2'
		IPdestination = input("Which node do you want to send this to? [N1/N3] ")
		IPprotocol = input("Which protocol would you like to use? [0:ping | 1:log | 2:kill] ")
		IPdata = input("What is the message you would like to send?: ")
		IPdatalength = str(len(IPdata))
		IPframe = IPsource + IPdestination + IPprotocol + IPdatalength + '|' + IPdata
		## END of IP frame
		datalength = str(len(IPframe)-1)

		#combine them to form the ethernet frame
		ethernet_frame = source + destination + datalength + '|' + IPframe
		### END of ethernet frame


		sck.sendall(ethernet_frame.encode('utf-8'))
		if ethernet_frame =='exit':
			print("Client is saying goodbye!")
			break
		data = sck.recv(1024)
		print(f"Router receipt: {data.decode().split('|')[2]}")