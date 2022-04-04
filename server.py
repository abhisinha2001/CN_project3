import socket # Needed for creating and working with sockets
import pickle # Needed as the data is being sent and recieved in the form json
import random # Used to generate a random index for CO2 level
import sys    # Required for exiting loops based on keyboard interrupt

PORT = 5050    #Arbitrary port number assigned for socket communication (Usually above 5000)

Levels = [1423,1546,1987,900] #Testing CO2 values in ppm(parts per million)

data = {"title":"C02 Level","level":1512,"source":"Server"} #Default data packet generated from server alarm

s= socket.socket(socket.AF_INET,socket.SOCK_STREAM) # Creating a socket that supports TCD connection
s.bind((socket.gethostname(),PORT))                 # Binding the socket to a the previosly declared port
s.listen(5)                                         #Listening for connections

while True:                                         
    data["level"] = Levels[random.randint(0, len(Levels)-1)] # Produce a random value from the Levels array
    try:
        clientsocket,address = s.accept()                   #Accept a client connection and resolve into clientsocket and address
        print(f"Connection from {address} has been established") # Connection confirmation prompt
        clientsocket.send(pickle.dumps(data))               # Converting the json data using pickle and sending over to client
    except KeyboardInterrupt:                # Detecting keyboard event to quit the program
        sys.exit(0)                          #Performing exit
    

s.close() #Closing socket

