from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from PyQt5.QtGui import QPainter, QPen, QBrush
from PyQt5.QtCore import Qt
from PyQt5.uic.properties import QtCore

boyut = 40
bosluk = 10
ycap = 10

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "Drawing Ellipse"
        self.top = 200
        self.left = 500
        self.width = 600
        self.height = 400

        self.InitWindow()

    def setupUi(self, MainWindow):
        Window.setObjectName("Window")
        Window.resize(300, 300)
        self.centralwidget = Qt.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Cizdir = Qt.QPushButton(self.centralwidget, clicked=lambda: self.paintEvent())
        self.Cizdir.setGeometry(QtCore.QRect(270, 270, 30, 30))
        self.Cizdir.setObjectName("Cizdir")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.InitWindow()

    def paintEvent(self, event):
        global boyut, bosluk, ycap
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))

        painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        # painter.setBrush(QBrush(Qt.green, Qt.DiagCrossPattern))

        painter.drawEllipse(bosluk, bosluk, boyut, boyut)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ElipsCiz"))
        self.Cizdir.setText(_translate("MainWindow", "Ciz"))
App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())