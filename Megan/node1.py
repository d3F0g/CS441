import socket

#creating the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostbyname('localhost'), 1234))

#input to be sent (src, dst, datalength, data)
node1_ip = "0x1A"
node1_mac = "32:04:0A:EF:19:CF"

while True:
    #message-receiving component
    full_msg = ''
    while True:
        msg = s.recv(8)
        if len(msg) <= 0:
            break
        full_msg += msg.decode("utf-8")

    if len(full_msg) > 0:
        #prints only the message, not who it came from
        print(full_msg[5:])
    
    #message-sending component
    sourcenode = 'N1'
    destroute = 'R2'
    destnode = input("Which node are you sending to? Please Enter N2 or N3")
    protocol = input("What would you like to do with the message? 0 to ping, 1 to log and 2 to kill.")
    messageinput = input("Please enter your message.")
    messagelength = len(messageinput)
    fullmsg = destroute + sourcenode + destnode + protocol + messagelength + '|' + messageinput

    #need to send this to router