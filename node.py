import socket # Needed for creating and working with sockets
import struct # Multicast requires byte objects and struct package offers functions to achieve the same
import sys     # Required for exiting loops based on keyboard interrupt
import pickle # Needed as the data is being sent and recieved in the form json

MCAST_GRP = '224.1.1.1' # Multicast Group 
MCAST_PORT = 5007       # Port for Multicast receiving
IS_ALL_GROUPS = True    # Boolean value to check if the port needs to be bound to group or all kinds of broadcast
MULTICAST_TTL = 2       # Time to live for multicast

MCAST_PORT_2 = 5008     # Port for the relay of incoming data


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # seperate socket for UDP Multicasting
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Providing socket paramters to define socket behaviour

if IS_ALL_GROUPS:                   # Conditional binding of socket
    # on this port, receives ALL multicast groups
    sock.bind(('', MCAST_PORT))
else:
    # on this port, listen ONLY to MCAST_GRP
    sock.bind((MCAST_GRP, MCAST_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY) # Message request needed for the mulitcast recieving

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)     # Setting up socket behaviour - Boilerplate code 

sender_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # Relay socket for peer broadcasting
sender_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL) # Setting up socket behaviour


while True:
    try:
        data = pickle.loads(sock.recv(1024))        # Recieving data and loading it as json/dictionary using pickle
        title = data["title"]       # Destructuring of data
        level = data["level"]
        source = data["source"]
        print(f"Data from {source}: {title}:{level}") # Console message
        data["source"] = "Node-Reciever 1"  # Altering the source for further relay
        if data:
            sender_sock.sendto(pickle.dumps(data), (MCAST_GRP, MCAST_PORT_2)) # Using the UDP broadcasting socket to broadcast the recieved data
        
        
    except KeyboardInterrupt:   # Detect Keyboard event 
        sys.exit(0)             # Exit program

