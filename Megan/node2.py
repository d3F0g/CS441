import socket

#creating the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostbyname('localhost'), 1235))

#input to be sent (src, dst, datalength, data)

while True:
    #message-receiving component
    full_msg = ''
    while True:
        msg = s.recv(8)
        if len(msg) <= 0:
            break
        full_msg += msg.decode("utf-8")

        if len(full_msg) > 0:
          if full_msg[2:4] != "N2":
            break

    print(full_msg[5:])

    #message-sending component
    destnode = input("Which node are you sending to? Please Enter N1 or N3")
    if destnode == "N1":
      destroute = "R1"
    elif destnode == "N3":
      destroute = "R2"
    else:
      print("Incorrect input.")
    #for nodes 2 and 3, if they send to each other, they don't need to go through router
    messageinput = input("Please enter your message.")
    fullmsg = destroute + destnode + messageinput