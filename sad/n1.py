import socket 
import argparse

parser = argparse.ArgumentParser(description = "This is the client for the multi threaded socket server!")
parser.add_argument('--host', metavar = 'host', type = str, nargs = '?', default = socket.gethostbyname('localhost'))
parser.add_argument('--port', metavar = 'port', type = int, nargs = '?', default = 9999)
args = parser.parse_args()

print(f"Connecting to server: {args.host} on port: {args.port}")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sck:
	sck.bind(('127.0.0.1', 65431))
	try:
		sck.connect((args.host, args.port))
	except Exception as e:
		raise SystemExit(f"We have failed to connect to host: {args.host} on port: {args.port}, because: {e}")

	while True:
		dest = input("Which node are you sending to...? ")
		# protocol = int(input("What protocol is this? [0,1,2] "))
		msg = input("What msg do you want to send to "+dest +"?: ")+'|'+dest
		sck.sendall(msg.encode('utf-8'))
		if msg =='exit':
			print("Client is saying goodbye!")
			break
		data = sck.recv(1024)
		print(f"Router receipt: {data.decode()}")