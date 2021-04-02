import socket 
import argparse

parser = argparse.ArgumentParser(description = "This is the client for the multi threaded socket server.")
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
		try:
			dest = input("Which node are you sending to...? ")
		except:
			if dest != 'N1' or dest !='N3':
				print("Please enter either 'N1' or 'N3'. Other inputs are not accepted.")
				continue
		try:
			protocol = int(input("What protocol is this? 0: ping, 1: log, 2: kill [0,1,2] "))
		except:
			if protocol not in [0, 1, 2]:
				print("Please enter a valid protocol. [0,1,2]")
				continue
		msg = input("What message do you want to send to "+dest +"?: ")+'|'+dest+protocol
		sck.sendall(msg.encode('utf-8'))
		if msg =='exit':
			print("Client is saying goodbye!")
			break
		data = sck.recv(1024)
		print(f"Router receipt: {data.decode()}")