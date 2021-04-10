def whoIsWho(n):
    if n == 10101:
        return "N1"
    elif n == 10102:
        return "N2"
    elif n == 10103:
        return "N3"



def frame(whoami, router_dest, node_dest, protocol, msg):
    final_frame = {
        "source": whoami,
        "r_dest": router_dest,
        "ethernet_datalength": len(router_dest)+len(node_dest)+len(protocol)+len(len(msg))+len(msg)

        # START of IP Frame
        "IPsource": whoami,
        "IPdest": node_dest,
        "Protocol": protocol,
        "Datalength": len(msg),
        "Data": msg
        #END of IP Frame
    }

    return final_frame

