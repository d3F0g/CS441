import json
from collections import OrderedDict
from datetime import datetime


def whoIsWho(n):
    if n == 10101:
        return "N1"
    elif n == 10102:
        return "N2"
    elif n == 10103:
        return "N3"


def node_to_IP(node):
    if node == "N1":
        return "0x1A"
    elif node == "N2":
        return "0x2A"
    elif node == "N3":
        return "0x2B"


def frame(whoami, IPwhoami, router_dest, node_dest, protocol, msg):
    final_frame = {
        "source": whoami,
        "ethernet_dest": router_dest,
        #refers to the length of the IP Frame
        "ethernet_datalength": len(IPwhoami)+len(node_dest)+len(protocol)+len(str(len(msg)))+len(msg),

        # START of IP Frame
        "IPsource": IPwhoami,
        "IPdest": node_to_IP(node_dest),
        "Protocol": protocol,
        "Datalength": len(msg)-1,
        "Data": msg.replace('\n', '')
        #END of IP Frame
    }
    
    return json.dumps(final_frame, indent=4, sort_keys=True)+'\n'

def logger(filename, msg):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    f = open(filename, "a")
    f.write(dt_string + "\n" + msg + "\n")
    f.close()


# shouldnt be having this since the router transforms it automatically
def router_left(dct):
    dct["source"] = "R2"
    dct["ethernet_dest"] = "R1"
    print json.dumps(dct, indent=4) 
    logger("router.txt", json.dumps(dct))

def router_right(dct):
    dct["source"] = "R1"
    dct["ethernet_dest"] = "R2"
    print json.dumps(dct, indent=4)
    logger("router.txt", json.dumps(dct))