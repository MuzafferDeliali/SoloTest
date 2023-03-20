import PyQt5
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
import sys
from PyQt5.QtGui import QPainter, QPen, QBrush
from PyQt5.QtCore import Qt, QRect

boyut = 40
bosluk = 10
ycap = 10

class Window(QMainWindow):
    def __init__(self):
        import PyQt5.QtWidgets
        super().__init__()

        self.title = "Drawing Ellipse"
        self.top = 200
        self.left = 500
        self.width = 300
        self.height = 300
        self.Cizdir = PyQt5.QtWidgets.QPushButton(self.window(), clicked=lambda: self.paintEvent(QPushButton))
        self.Cizdir.setGeometry(PyQt5.QtCore.QRect(270, 270, 30, 30))
        self.Cizdir.setObjectName("Cizdir")
        self.InitWindow()

    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

    def paintEvent(self, event):
        global boyut, bosluk, ycap
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))

        painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        # painter.setBrush(QBrush(Qt.green, Qt.DiagCrossPattern))

        painter.drawEllipse(bosluk, bosluk, boyut, boyut)


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())