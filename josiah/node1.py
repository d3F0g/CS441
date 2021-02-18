import socket

#creating the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostbyname('localhost'), 1234))

#input to be sent (src, dst, datalength, data)


while True:
    full_msg = ''
    while True:
        msg = s.recv(8)
        if len(msg) <= 0:
            break
        full_msg += msg.decode("utf-8")

    if len(full_msg) > 0:
        print(full_msg[5:])