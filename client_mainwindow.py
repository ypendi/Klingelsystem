from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMessageBox

import client_logik

import sys

class Window(QtWidgets.QWidget):

    clientsocket = None

    # client wird in dieser Methode mit dem Server verbunden (falls möglich)
    def setupClientLogik(self):
        self.clientsocket = client_logik.Client_Receiver()
        if self.clientsocket.verbinde_client():
            self.labelVerbunden.setText("VERBUNDEN: Es hat noch nicht geklingelt!")
        else:
            self.labelVerbunden.setText("NICHT VERBUNDEN!")
        # if connect doesnt work open popup to notify here!
        self.clientsocket.gotMsg.connect(self.empfangen)

    # Client window Grafik wird hier aufgesetzt
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
        self.btnEntkoppeln = QtWidgets.QPushButton(self.centralwidget)
        self.btnEntkoppeln.setGeometry(QtCore.QRect(460, 280, 241, 61))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.btnEntkoppeln.setFont(font)
        self.btnEntkoppeln.setObjectName("btnEntkoppeln")
        self.btnEntkoppeln.clicked.connect(self.entkoppeln) # entkoppeln button mit entkoppelt funktion verbunden
        self.labelVerbunden = QtWidgets.QLabel(self.centralwidget)
        self.labelVerbunden.setGeometry(QtCore.QRect(10, 120, 771, 61))
        font = QtGui.QFont()
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)
        self.labelVerbunden.setFont(font)
        self.labelVerbunden.setAlignment(QtCore.Qt.AlignCenter)
        self.labelVerbunden.setObjectName("labelVerbunden")
        self.btnVerbinden = QtWidgets.QPushButton(self.centralwidget)
        self.btnVerbinden.setGeometry(QtCore.QRect(110, 280, 231, 61))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.btnVerbinden.setFont(font)
        self.btnVerbinden.setObjectName("btnVerbinden")
        self.btnVerbinden.clicked.connect(self.connect) # verbinden button mit connect funktion verbunden
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
        self.label.setText(_translate("MainWindow", "CLIENT"))
        self.btnEntkoppeln.setText(_translate("MainWindow", "GERÄT ENTKOPPELN"))
        self.labelVerbunden.setText(_translate("MainWindow", "VERBUNDEN: ES HAT NOCH NICHT GEKLINGELT!"))
        self.btnVerbinden.setText(_translate("MainWindow", "GERÄT VERBINDEN"))
    
    # client wird vom server entkoppelt
    def entkoppeln(self):
        try:
            self.clientsocket.message_server("/disconnect")
            self.clientsocket.stopThread()
            self.labelVerbunden.setText("NICHT VERBUNDEN!")
        except:
            print("Error: Nicht mit Server verbunden")
            self.labelVerbunden.setText("NICHT VERBUNDEN!")

    def sende_ich_kann_nicht(self):
        self.clientsocket.message_server("ICH_GEHE_NICHT")

    def sende_ich_gehe(self):
        self.clientsocket.message_server("ICH_GEHE")    

    def connect(self):
        if self.clientsocket.verbinde_client():
            self.clientsocket.startThread()
            self.labelVerbunden.setText("VERBUNDEN: Es hat noch nicht geklingelt!")
        else:
            #self.labelVerbunden.setText("NICHT VERBUNDEN!")
            pass
            
    # empfängt die pyqtSignals aus client_logik (wird in der client_logik run methode aufgerufen)
    @pyqtSlot(str)
    def empfangen(self, msg):
        print("MSG:", msg)
        if msg == "KLINGEL":
            try:
                jgBox.close()
            except Exception as e:
                pass
            self.geklingelt_popup()
        if msg == "JEMAND_GEHT":
            msgBox.close()
            self.jemand_geht_popup()
            print(msg)
    

    def geklingelt_popup(self): # wird aufgerufen wenn es klingelt (pop up fenster)
        global msgBox
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle('KLINGEL')
        
        msgBox.setStyleSheet("QPushButton{ width:200px; height:25px; font-size: 13px;}")

        msgBox.setFont(QtGui.QFont('Arial', 16))
        msgBox.setText('ES HAT GEKLINGELT!')


        msgBox.setStandardButtons(QMessageBox.Yes|QMessageBox.No)

        buttonY = msgBox.button(QMessageBox.Yes)
        buttonY.setText('ICH GEHE')
        buttonY.setStyleSheet("color: #039c03; font:bold;")
        buttonY.clicked.connect(self.sende_ich_gehe) # ich gehe aus pop up window mit sende_ich_gehe verbunden

        buttonN = msgBox.button(QMessageBox.No)
        buttonN.setText('ICH KANN NICHT')
        buttonN.setStyleSheet("color: #f51b38; font:bold")
        buttonN.clicked.connect(self.sende_ich_kann_nicht)  # ich kann nicht aus pop up window mit sende_ich_kann_nicht verbunden

        msgBox.exec_()

    def jemand_geht_popup(self): # wird aufgerufen, wenn signal kommt, dass eine andere Person geht!
        global jgBox
        jgBox = QMessageBox()
        jgBox.setIcon(QMessageBox.Information)
        jgBox.setWindowTitle('JEMAND GEHT')
        
        jgBox.setStyleSheet("QPushButton{ width:200px; height:25px; font-size: 13px;}")

        jgBox.setFont(QtGui.QFont('Arial', 16))
        jgBox.setText('Eine andere Person kümmert sich darum!')


        jgBox.setStandardButtons(QMessageBox.Ok)

        buttonY = jgBox.button(QMessageBox.Ok)
        buttonY.setText('Ok')
        buttonY.setStyleSheet("color: #1233b5; font:bold;")

        jgBox.exec_()


if __name__ == "__main__":
    # started das setup des Fensters
    app = QtWidgets.QApplication(sys.argv)

    MainWindow = QtWidgets.QMainWindow()
    window = Window()
    window.setupUi(MainWindow)

    window.setupClientLogik()
    window.clientsocket.startThread()

    MainWindow.show()

    app.exec_()
    try:
        window.clientsocket.disconnect()
    except:
        pass
    sys.exit()
    
