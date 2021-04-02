import socket
import struct

def addr_to_bytes(addr):
    return socket.inet_aton(addr[0]) + struct.pack('H', addr[1])

def bytes_to_addr(addr):
    return (socket.inet_ntoa(addr[:4]), struct.unpack('H', addr[4:])[0])

def udp_server(addr):
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soc.bind(addr)

    _, client_a = soc.recvfrom(0)
    _, client_b = soc.recvfrom(0)
    soc.sendto(addr_to_bytes(client_b), client_a)
    soc.sendto(addr_to_bytes(client_a), client_b)

addr = ('0.0.0.0', 4000)
udp_server(addr)