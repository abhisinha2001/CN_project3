import socket # Needed for creating and working with sockets
import pickle # Needed as the data is being sent and recieved in the form json
import time   # Required to perform sleep 
import sys    # Required for exiting loops based on keyboard interrupt

PORT = 33000
MCAST_GRP = '224.1.1.1'     # Multicast group used to send a UDP broadcast over a specific group 
# MCAST_PORT = 34000           # Port for the mulsticast to run on
MULTICAST_TTL = 3
time_start = time.localtime(time.time()) 

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # seperate socket for UDP Multicasting
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)  # Providing socket parameters to define socket behaviour

while True:
    try:
        s= socket.socket(socket.AF_INET,socket.SOCK_STREAM) # Creating a socket that supports TCP connection
        # socket.gethostname()
        s.connect((socket.gethostname(),PORT))
        # s.connect(('10.35.70.12',PORT))              # Connecting with the server socket
        data = pickle.loads(s.recv(1024))                   # Recieving data and loading it as byte stream using pickle
        if data:
            Nitrate = data["Nitrate level"]                               # Destructuring of data
            Phosphate = data["Phosphate Level"]
            Source  = data["Source"]                   
            time_result = time.localtime(time.time())         
            print(f"Time: {time_result.tm_hour}:{time_result.tm_min}:{time_result.tm_sec} \nNitrate Level:{Nitrate} \nPhosphate Level: {Phosphate} \nSource: {Source}\n")# Console message
            data["Source"] = "Central Node"     # Altering the source for further relay
            time_start = time.localtime(time.time())
            for MCAST_PORT in range(34000,34005):
                sock.sendto(pickle.dumps(data), (MCAST_GRP, MCAST_PORT)) # Using the UDP broadcasting socket to broadcast the recieved data
        if time_start.tm_hour - time.localtime(time.time()).tm_hour >1:
            print("\nTIMEOUT ALERT. Please check central node\n")
                
        time.sleep(2)                           # Performing a request every second
    except KeyboardInterrupt:                   # Detect Keyboard event
        sys.exit(0)                             # Exit program
    

s.close()
sock.close()

