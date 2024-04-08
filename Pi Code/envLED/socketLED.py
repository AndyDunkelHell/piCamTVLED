import socket

#include all neccessary packages to get LEDs to work with Raspberry Pi
import time
import board
import neopixel

#Initialise a strips variable, provide the GPIO Data Pin
#utilised and the amount of LED Nodes on strip and brightness (0 to 1 value)
pixels1 = neopixel.NeoPixel(board.D18, 55, brightness=1)

#Also create an arbitary count variable
x=0

#Focusing on a particular strip, use the command Fill to make it all a single colour
#based on decimal code R, G, B. Number can be anything from 255 - 0. Use a RGB Colour
#Code Chart Website to quickly identify a desired fill colour.
pixels1.fill((0, 220, 0))
#Sleep for three seconds, You should now have all LEDs showing light with the first node
#Showing a different colour
time.sleep(4)

#Complete the script by returning all the LED to off
pixels1.fill((0, 0, 0))



def run_server():
    # create a socket object
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = "192.168.88.101"
    port = 8000

    # bind the socket to a specific address and port
    server.bind((server_ip, port))
    # listen for incoming connections
    server.listen(0)
    print(f"Listening on {server_ip}:{port}")

    # accept incoming connections
    client_socket, client_address = server.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

    # receive data from the client
    while True:
        request = client_socket.recv(1024)
        request = request.decode("utf-8") # convert bytes to string

        list_request = request.split(",")
        #while x < 8:
        try: 
            int_test = int(list_request[0])
        except:
            print(str(list_request[0]))
        else:
            pixels1[0] = (int(list_request[2]),int(list_request[1]), int(list_request[0]))
            pixels1[1] = (int(list_request[5]),int(list_request[4]), int(list_request[3]))
            pixels1[2] = (int(list_request[8]),int(list_request[7]), int(list_request[6]))
            pixels1[3] = (int(list_request[11]),int(list_request[10]), int(list_request[9]))
            pixels1[4] = (int(list_request[14]),int(list_request[13]), int(list_request[12]))
            pixels1[5] = (int(list_request[17]),int(list_request[16]), int(list_request[15]))
            pixels1[6] = (int(list_request[20]),int(list_request[19]), int(list_request[18]))
            pixels1[7] = (int(list_request[23]),int(list_request[22]), int(list_request[21]))
        #print(list_request[:2])

        # if we receive "close" from the client, then we break
        # out of the loop and close the conneciton
        if request.lower() == "close":
            # send response to the client which acknowledges that the
            # connection should be closed and break out of the loop
            client_socket.send("closed".encode("utf-8"))
            break

        #print(f"Received: {request}", end="\r")

        response = "accepted".encode("utf-8") # convert string to bytes
        # convert and send accept response to the client
        client_socket.send(response)

    # close connection socket with the client
    pixels1.fill((0, 0, 0))
    client_socket.close()
    print("Connection to client closed")
    # close server socket
    server.close()


run_server()
