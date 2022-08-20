import socket 
import threading

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname()) # set SERVER to current devices IP address
ADDR = (SERVER, PORT)

HEADER = 64 # every first msg from client to server has to be 64bytes (first msg is amount of bytes of the actual msg)
FORMAT = 'utf-8'
DISCONNECT_MSG = "/disconnect"

clientlist = []


def starte_server():
    try:
        global server
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create a new IPv4 STREAM socket
        server.bind(ADDR)
        main()
    except:
        print("Error: Server läuft bereits")


def handle_client(clientsocket, addr):
    print(f"[NEW CONNECTION] addr: {addr}")

    connected = True

    while connected:
        try:
            message = clientsocket.recv(1024).decode(FORMAT)
            print(f"[{addr}]: {message}")


            if message == "ICH_GEHE_NICHT":
                pass
            elif message == "ICH_GEHE": # wenn einer der clients "zur klingel geht"
                for client in clientlist:   # sende signal an alle anderen clients 
                    print(client.getpeername())
                    if(client != clientsocket):
                        message = "JEMAND_GEHT".encode(FORMAT)
                        client.send(message)

            elif message == DISCONNECT_MSG: # break while loop
                connected = False
                clientlist.remove(clientsocket)
                break
        except:
            connected = False
            break


    
    print(f"[DISCONNECT] {addr} disconnected.")
    print(f"[ACTIVE CONNECTIONS]: {clientlist.count}")
    clientsocket.close() # close connection

def sende_klingelsignal_an_clients(): # sendet das Klingelsignal
    message = "KLINGEL"
    message = message.encode(FORMAT)
    
    if not clientlist: # list is empty 
        print("Error: keine Clients verbunden")
    else:
        for client in clientlist:
            # client.send(send_length)
            client.send(message)


def main():
    # starte_server()
    server.listen()
    print(f"[STARTING] server is running on {SERVER}")
    while True:
        clientsocket, addr = server.accept() # wait for new connection, store ip in addr and store socket obj in conn
        clientlist.append(clientsocket)
        thread = threading.Thread(target=handle_client, args=(clientsocket, addr)) # create a new thread of the handle_client function
        thread.start()
        print(f"[ACTIVE CONNECTIONS]: {threading.activeCount() -1}")

# main()


