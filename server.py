import socket # Needed for creating and working with sockets
import pickle # Needed as the data is being sent and recieved in the form json
import random # Used to generate a random index for CO2 level
import sys    # Required for exiting loops based on keyboard interrupt

PORT = 33000    #Arbitrary port number assigned for socket communication (Usually above 5000)

Levels = [{"Nitrogen level":1290,"Phosphate Level":1900,"PH":6.6},{"Nitrogen level":2200,"Phosphate Level":1800,"PH":7.1},{"Nitrogen level":1314,"Phosphate Level":1800,"PH":7.1},{"Nitrogen level":1400,"Phosphate Level":2100,"PH":8.4}] #Testing CO2 values in ppm(parts per million)

s= socket.socket(socket.AF_INET,socket.SOCK_STREAM) # Creating a socket that supports TCD connection
s.bind((socket.gethostname(),PORT))                 # Binding the socket to a the previosly declared port
s.listen(5)                                         #Listening for connections

while True:                                         
    data = Levels[random.randint(0, len(Levels)-1)] # Produce a random value from the Levels array
    try:
        clientsocket,address = s.accept()                   #Accept a client connection and resolve into clientsocket and address
        print(f"Connection from {address} has been established") # Connection confirmation prompt
        clientsocket.send(pickle.dumps(data))               # Converting the json data using pickle and sending over to client
    except KeyboardInterrupt:                # Detecting keyboard event to quit the program
        sys.exit(0)                          #Performing exit
    

s.close() #Closing socket

