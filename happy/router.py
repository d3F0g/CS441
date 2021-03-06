import socket
import argparse
import threading 

def sendMsg(msg):
# This will recreate the socket object to send to R1 as well
	s = socket.socket() 
	# connect to r1
	s.connect(('127.0.0.1', 65431)) 
	s.sendall(msg, encoding='utf8')
	# receive data from r2  
	print (s.recv(1024) ) 
	# close the connection  
	s.close()  


parser = argparse.ArgumentParser(description = "This is the server for the multithreaded socket demo!")
parser.add_argument('--host', metavar = 'host', type = str, nargs = '?', default = socket.gethostbyname('localhost'))
parser.add_argument('--port', metavar = 'port', type = int, nargs = '?', default = 9999)
args = parser.parse_args()

print(f"Running the server on: {args.host} and port: {args.port}")

sck = socket.socket()
sck.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try: 
	sck.bind((args.host, args.port))
	sck.listen(5)
except Exception as e:
	raise SystemExit(f"We could not bind the server on host: {args.host} to port: {args.port}, because: {e}")

def naming(portNumber):
	if (portNumber==65431):
		return "N1"
	elif (portNumber==65432):
		return "N2"
	elif (portNumber==65433):
		return "N3"


def on_new_client(client, connection):
	ip = connection[0]
	port = connection[1]
	print(f"THe new connection was made from IP: {ip}, and port: {port}!")
	while True:
		msg = client.recv(1024)
		if msg.decode() == 'exit':
			break
		print(naming(port) +" sending packet to "+msg.decode().split('|')[1][2:4])
		
		# router logic
		if msg.decode().split('|')[1][2:4] == 'N1':
			#send to N1 the message
			sendMsg(msg.decode().split('|')[2])
		# elif msg.decode().split('|')[1][2:4] == 'N2':

		# elif msg.decode().split('|')[1] == 'N1':


		reply = msg.decode()
		client.sendall(reply.encode('utf-8'))
	print(f"The client from ip: {ip}, and port: {port}, has gracefully diconnected!")
	client.close()

while True:
	try: 
		client, ip = sck.accept()
		threading._start_new_thread(on_new_client,(client, ip))
	except KeyboardInterrupt:
		print(f"Shutting down the router!")
	except Exception as e:
		print(f"Well I did not anticipate this: {e}")

sck.close()
