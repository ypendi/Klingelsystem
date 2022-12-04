# GUI des Servers

from PyQt5 import QtCore, QtGui, QtWidgets
import server_logik

class Window(object):

    serversocket = None 
    def setupServerLogik(self):
        self.serversocket = server_logik.Server()

    def setupUi(self, MainWindow):
        MainWindow.setWindowState(QtCore.Qt.WindowMaximized)
        MainWindow.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        MainWindow.setObjectName("MainWindow")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(310, 20, 181, 61))
        font = QtGui.QFont()
        font.setPointSize(27)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.labelServerStatus = QtWidgets.QLabel(self.centralwidget)
        self.labelServerStatus.setGeometry(QtCore.QRect(10, 120, 771, 61))
        font = QtGui.QFont()
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)
        self.labelServerStatus.setFont(font)
        self.labelServerStatus.setAlignment(QtCore.Qt.AlignCenter)
        self.labelServerStatus.setObjectName("labelServerStatus")
        self.btnKlingel = QtWidgets.QPushButton(self.centralwidget)
        self.btnKlingel.setGeometry(QtCore.QRect(460, 280, 240, 69))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.btnKlingel.setFont(font)
        self.btnKlingel.setObjectName("btnKlingel")
        self.btnKlingel.clicked.connect(self.sende_klingelsignal) # klingel button wird mit sende_klingelsignal verbunden
        self.btnStartServer = QtWidgets.QPushButton(self.centralwidget)
        self.btnStartServer.setGeometry(QtCore.QRect(110, 280, 241, 61))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.btnStartServer.setFont(font)
        self.btnStartServer.setObjectName("btnStartServer")
        self.btnStartServer.clicked.connect(self.start_server) # wenn der Starte Server button manuell geklickt wird wird start_server Funktion aufgerufen
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "SERVER"))
        self.btnKlingel.setText(_translate("MainWindow", "KLINGEL"))
        self.btnStartServer.setText(_translate("MainWindow", "START SERVER"))
        self.labelServerStatus.setText("SERVER LÄUFT")

    # startet den Server Thread vom server objekt aus server_logik
    def start_server(self):
        try:
            self.serversocket.startThread()
            # self.labelServerStatus.setText("SERVER LÄUFT")
        except:
            print("Error: Problem beim Starten des Servers")

    def sende_klingelsignal(self):
        self.serversocket.sende_klingelsignal_an_clients()



if __name__ == "__main__":
    import sys
    # setzt das Fenster und GUI auf
    app = QtWidgets.QApplication(sys.argv)

    MainWindow = QtWidgets.QMainWindow()
    window = Window()
    window.setupUi(MainWindow)

    window.setupServerLogik()
    window.serversocket.startThread()

    MainWindow.show()
    
    sys.exit(app.exec_())
