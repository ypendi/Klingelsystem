import socket 

from PyQt5.QtCore import pyqtSignal, QThread

class Client_Receiver(QThread):

    SERVER_IP = "192.168.56.1" # set SERVER to servers IP 
    PORT = 5050
    client_socket = None
    connected = False

    FORMAT = "utf-8"
    DISCONNECT_MSG = "/disconnect"
    KLINGEL_MSG = "KLINGEL"

    gotMsg = pyqtSignal([str])

    def __init__(self, ip=SERVER_IP, port=PORT):
        super(QThread, self).__init__()
        self.SERVER_IP = ip
        self.PORT = port
        # self.verbinde_client()

    def startThread(self):
        if self.connected == False:
            print("Nicht mit Server verbunden")
            return
        if self.isRunning():
            print("läuft bereits!")
            return
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

    def verbinde_client(self):
        if self.connected == False:
            try:
                self.connected = True 
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.connect((self.SERVER_IP, self.PORT))
                print(f"Verbunden:{self.SERVER_IP}:{self.PORT}")
                return True
            except Exception as e:
                print("Verbinden fehlgeschlagen", e)
                self.connected = False
                self.client_socket = None
                return False

    def disconnect(self):
        self.client_socket.send(self.DISCONNECT_MSG.encode(self.FORMAT))
        self.client_socket.close()
        self.connected = False 

    def message_server(self, message):
        message = message.encode(self.FORMAT)
        self.client_socket.send(message)

    def run(self): # run
        try: 
            while not self.isInterruptionRequested():
                msg = self.client_socket.recv(1024).decode(self.FORMAT)

                if msg == self.KLINGEL_MSG:
                    self.gotMsg.emit(msg)
                elif msg == "JEMAND_GEHT":
                    self.gotMsg.emit(msg)
                else:
                    print("MSG:", msg)    

        except Exception as f:
            print("Error: ", f)
            return