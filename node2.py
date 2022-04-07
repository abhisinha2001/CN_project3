import socket # Needed for creating and working with sockets
import struct # Multicast requires byte objects and struct package offers functions to achieve the same
import sys     # Required for exiting loops based on keyboard interrupt
import pickle # Needed as the data is being sent and recieved in the form json
import time

MCAST_GRP = '224.1.1.1' # Multicast Group 
MCAST_PORT = 34001       # Port for Multicast receiving
IS_ALL_GROUPS = True    # Boolean value to check if the port needs to be bound to group or all kinds of broadcast
MULTICAST_TTL = 3       # Time to live for multicast- Controls the number of hops for packet.
time_start = time.localtime(time.time())  


MCAST_PORT_2 = 34007    # Port for the relay of incoming data

my_levels = {"Nitrate Level":1360,"Phosphate Level":1600}

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # seperate socket for UDP Multicasting
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Providing socket paramters to define socket behaviour

if IS_ALL_GROUPS:                   # Conditional binding of socket
    # on this port, receives ALL multicast groups
    sock.bind(('', MCAST_PORT))
    print("1.ALL Multicast succesfull")
else:
    # on this port, listen ONLY to MCAST_GRP
    sock.bind((MCAST_GRP, MCAST_PORT))
    print("1.Only MCAST_GRP succesful")

mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY) # Message request needed for the mulitcast recieving
if mreq:
    print("2.MREQ Done")

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)     # Setting up socket behaviour - Boilerplate code 
if sock:
    print("3.Socket Connect Established\n")

sender_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # Relay socket for peer broadcasting
sender_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL) # Setting up socket behaviour


while True:
    try:
        data = pickle.loads(sock.recv(1024))        # Recieving data and loading it as json/dictionary using pickle
        if data:
            Nitrate = data["Nitrate level"]                               # Destructuring of data
            Phosphate = data["Phosphate Level"] 
            Source = data["Source"]                   
            time_result = time.localtime(time.time())         
            print(f"Time: {time_result.tm_hour}:{time_result.tm_min}:{time_result.tm_sec} \nNitrate Level:{Nitrate} \nPhosphate Level: {Phosphate} \nSource: {Source}\n")
            data["Source"] = "Node-Reciever 2"  # Altering the source for further relay
            if my_levels["Nitrate Level"]>Nitrate:
                print("Excess Nitrate Content. Blocking Nozzle\n")
            else:
                print("Allowing Irrigation\n")
            # print("Recieved data, Relaying the same\n")
            sender_sock.sendto(pickle.dumps(data), (MCAST_GRP, MCAST_PORT_2)) # Using the UDP broadcasting socket to broadcast the recieved data
            time_start = time.localtime(time.time())
            if time_start.tm_hour - time.localtime(time.time()).tm_hour >1:
                print("\nTIMEOUT ALERT. Please check node 2\n")
        
                
        
    except KeyboardInterrupt:   # Detect Keyboard event 
        sys.exit(0)             # Exit program

sender_sock.close()
sock.close()