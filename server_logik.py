import socket 
import threading

from PyQt5.QtCore import pyqtSignal, QThread

import RPi.GPIO as GPIO

class Server(QThread):
    PORT = 5050
    SERVER = "192.168.2.120" # set SERVER IP address
    ADDR = (SERVER, PORT)

    FORMAT = 'utf-8'
    DISCONNECT_MSG = "/disconnect"

    clientlist = [] # speichert alle verbundenen clients

    def __init__(self, ip=SERVER, port=PORT):
        super(QThread, self).__init__()
        self.SERVER = ip
        self.PORT = port
        self.starte_server()

    def startThread(self):
        self.start()
    
    def stopThread(self):
        if not self.isRunning():
            print("not running!")
        else:
            self.requestInterruption()
            self.quit()
            if not self.wait(100):
                self.terminate()
                if not self.wait(100):
                    print("Terminate failed!")
        self.disconnect()

    # aufsetzen des servers
    def starte_server(self):
        try:
            global server
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create a new IPv4 STREAM socket
            server.bind(self.ADDR)
            #self.run()
        except:
            print("Error: Server läuft bereits")

    # wird aufgerufen, wenn ein client sich verbindet (in einem seperaten Thread)
    def handle_client(self, clientsocket, addr):
        print(f"[NEW CONNECTION] addr: {addr}")

        connected = True

        while connected:
            try:
                message = clientsocket.recv(1024).decode(self.FORMAT) # empfängt nachricht des clients
                print(f"[{addr}]: {message}")


                if message == "ICH_GEHE_NICHT": # wenn die nachricht "vom client ICH_GEHE_NICHT ist"
                    pass # passiert nichts
                elif message == "ICH_GEHE": # wenn einer der clients "zur klingel geht"
                    for client in self.clientlist:   # sende signal an alle anderen clients 
                        print(client.getpeername())
                        if(client != clientsocket):
                            message = "JEMAND_GEHT".encode(self.FORMAT)
                            client.send(message)

                elif message == self.DISCONNECT_MSG: # wenn der client entkoppelt
                    connected = False 
                    self.clientlist.remove(clientsocket) # von liste löschen
                    break
            except:
                connected = False
                break

        
        print(f"[DISCONNECT] {addr} disconnected.")
        print(f"[ACTIVE CONNECTIONS]: {len(self.clientlist)}")
        clientsocket.close() # close connection

    def sende_klingelsignal_an_clients(self): # sendet das Klingelsignal
        message = "KLINGEL"
        message = message.encode(self.FORMAT)
        
        if not self.clientlist: # wenn keine clients verbunden sind
            print("Error: keine Clients verbunden")
        else:
            for client in self.clientlist:
                # client.send(send_length)
                client.send(message)

    # ------------------------------------------- falls das signal der echten Klingel abgegriffen werden soll -------------------------------------------
    def listen_physische_klingel(self):
        # input pin vom Klingelsignal
        input_pin = 17
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(input_pin, GPIO.IN) # pin wird auf input gesetzt

        while True:
            if GPIO.input(input_pin) == 0:
                print("stromkreis geschlossen.")
                self.sende_klingelsignal_an_clients()

    # Mainthread des Servers
    def run(self):
        try:
            server.listen()
            print(f"[STARTING] server is running on {self.SERVER}")
            while not self.isInterruptionRequested():
                clientsocket, addr = server.accept() # wait for new connection, store ip in addr and store socket obj in conn
                self.clientlist.append(clientsocket)
                handle_clients_thread = threading.Thread(target=self.handle_client, args=(clientsocket, addr)) # create a new thread of the handle_client function
                handle_clients_thread.start()
                # physische_klingel_thread = threading.Thread(target=self.listen_physische_klingel) # -------------------------------------------------
                # physische_klingel_thread.start()
                print(f"[ACTIVE CONNECTIONS]: {threading.activeCount() -1}")
    
        except Exception as e:
            print("Error:", e)
            return