import sys
import math
import numpy as np
import random
import os
import time

from enum import Enum
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QComboBox, QLabel, QFileDialog, QMessageBox
from PyQt5.QtCore import QSize, Qt, QPoint
from PyQt5.QtGui import QPainter, QPen, QBrush, QCursor, QPixmap

boyut = 60
bosluk = 20
ycap = 18
Yers = []
ayer = None
yer1 = None
yer2 = None
bas = False


ihtimals = []
son = []
son_index = 0
eniyi = []
skor = 32


class Yon(Enum):
    Sag = 0
    Ust = 1
    Sol = 2
    Alt = 3


class YerDurum(Enum):
    Bos = 0
    Hedef = 1
    Dolu = 2
    Aktif = 3
    AktifSag = 4
    AktifUst = 5
    AktifSol = 6
    AktifAlt = 7


class Islem(Enum):
    Yok = 0
    Oyna = 1
    Dosyadan = 2
    Dene = 3


class Har():
    baslangic = 0
    bitis = 0

    def __init__(self, baslangic, bitis):
        self.baslangic = baslangic
        self.bitis = bitis

    def set(self, baslangic, bitis):
        self.baslangic = baslangic
        self.bitis = bitis


class Yer():
    id = 0
    x = 0
    y = 0
    durum = YerDurum.Bos

    def __init__(self, id, x, y, durum):
        self.id = id
        self.x = x
        self.y = y
        self.durum = durum

    def setDurum(self, durum):
        self.durum = durum

    def getKomsu(self, yon):
        if yon == Yon.Sag:
            return self.getYerXY(self.x + 1, self.y)
        elif yon == Yon.Ust:
            return self.getYerXY(self.x, self.y + 1)
        elif yon == Yon.Sol:
            return self.getYerXY(self.x - 1, self.y)
        elif yon == Yon.Alt:
            return self.getYerXY(self.x, self.y - 1)
        else:
            return None

    def getUzakKomsu(self, yon):
        if yon == Yon.Sag:
            return self.getYerXY(self.x + 2, self.y)
        elif yon == Yon.Ust:
            return self.getYerXY(self.x, self.y + 2)
        elif yon == Yon.Sol:
            return self.getYerXY(self.x - 2, self.y)
        elif yon == Yon.Alt:
            return self.getYerXY(self.x, self.y - 2)
        else:
            return None

    def getHareket(self, yon):
        if self.durum.value > 1 :
            komsu = self.getKomsu(yon)
            if komsu != None:
                if komsu.durum.value < 2:
                    uzakKomsu = self.getUzakKomsu(yon)
                    if uzakKomsu != None:
                        if uzakKomsu.durum.value < 2:
                            return True
        return False

    def uzerindeMi(self, nx, ny):
        mx = bosluk + (self.x + 3) * boyut + boyut / 2
        my = bosluk + (3 - self.y) * boyut  + boyut / 2

        u = math.sqrt((nx-mx)*(nx-mx) + (ny-my)*(ny-my))
        return u <= ycap

    @staticmethod
    def getYerId(id):
        if id >= 0 and id < len(Yers):
            return Yers[id]
        else:
            return None

    @staticmethod
    def getYerXY(x, y):
        gecersiz = abs(x) >= 2 and abs(y) >= 2
        if gecersiz:
            return None
        else:
            for i in range(0, len(Yers)):
                yer = Yers[i]
                if yer.x == x and yer.y == y:
                    return yer

            return None

    @staticmethod
    def getYerPixel(px, py):
        for i in range(0, len(Yers)):
            yer = Yers[i]
            if yer.uzerindeMi(px, py):
                return yer
        return None

class MainWindow(QMainWindow):
    def __init__(self):
        global boyut, bosluk, ycap
        QMainWindow.__init__(self)
        s = boyut * 7 + 2 * bosluk


        self.setMinimumSize(QSize(s, s))
        self.mousePressEvent(self.mousePressEvent)
        self.mouseReleaseEvent(self.mouseReleaseEvent)
        btnOyna = QPushButton('Oyna', self)
        btnOyna.clicked.connect(self.oyna_click)
        btnOyna.resize(100,24)
        btnOyna.move(10, 10)


        label1 = QLabel("Skor", self)
        label1.resize(40, 24)
        label1.move(10, 40)

        self.comSkor = QComboBox(self)
        self.comSkor.addItem("1")
        self.comSkor.addItem("2")
        self.comSkor.addItem("3")
        self.comSkor.addItem("4")
        self.comSkor.addItem("5")
        self.comSkor.resize(30, 24)
        self.comSkor.move(35, 40)

        btnDene = QPushButton('Dene', self)
        btnDene.clicked.connect(self.dene_click)
        btnDene.resize(40,24)
        btnDene.move(70, 40)

        btnSonGoster = QPushButton('Son Oyun Göster', self)
        btnSonGoster.clicked.connect(self.songoster_click)
        btnSonGoster.resize(100,24)
        btnSonGoster.move(10, 70)

        btnOyunGoster = QPushButton('Oyun Göster', self)
        btnOyunGoster.clicked.connect(self.oyungoster_click)
        btnOyunGoster.resize(100,24)
        btnOyunGoster.move(10, 100)
        self.islem = Islem.Yok


    def oyna_click(self):
        global son
        son = []
        self.islem = Islem.Oyna
        self.yerReset()
        self.repaint()

    def dene_click(self):
        self.islem = Islem.Dene
        self.yerReset()
        maxskor = int(self.comSkor.currentText())
        self.skoraKadarOyna(maxskor)
        self.repaint()

    def songoster_click(self):
        self.islem = Islem.Dosyadan
        self.dosyadanOyna("son.txt")


    def oyungoster_click(self):
        self.islem = Islem.Dosyadan
        fname = QFileDialog.getOpenFileName(self, 'Open file',
                                            'c:\\users', "Image files (*.txt)")
        if fname[0] != "":
            self.dosyadanOyna(fname[0])


    def paintEvent(self, event):
        QMainWindow.paintEvent(self, event)
        self.tumYerCiz()

    def yerCiz(self, yer):
        global boyut, bosluk, ycap
        px = bosluk + (yer.x + 3) * boyut
        py = bosluk + (3 - yer.y) * boyut
        f = int((boyut / 2) - ycap)
        x1 = int(px + f)
        y1 = int (py + f)
        cap = int(2 * ycap)
        painter = QPainter(self)
        if yer.durum == YerDurum.Hedef:
            renk_cevre = Qt.red
            renk_dolgu = Qt.white
        elif yer.durum == YerDurum.Dolu:
            renk_cevre = Qt.black
            renk_dolgu = Qt.gray
        elif yer.durum.value >= 4:
            renk_cevre = Qt.red
            renk_dolgu = Qt.gray
        else:
            renk_cevre = Qt.black
            renk_dolgu = Qt.white

        pen = QPen(renk_cevre, 5)
        painter.setPen(pen)
        painter.drawEllipse(x1, y1, cap, cap)
        brush = QBrush(renk_dolgu, Qt.SolidPattern)
        painter.setBrush(brush)
        painter.drawEllipse(x1, y1, cap, cap)

        if yer.durum.value > 3:
            p1 = QPoint()
            p2 = QPoint()
            p3 = QPoint()
            p4 = QPoint()
            uc = 5
            pen = QPen(renk_cevre, 3)
            painter.setPen(pen)

            if yer.durum == YerDurum.AktifSag:
                p1.setX(int(px + 2 * f))
                p1.setY(int(py + boyut / 2))
                p2.setX(int(px + boyut - 2 * f))
                p2.setY(p1.y())

                p3.setX(p2.x() - uc)
                p3.setY(p2.y() - uc)
                p4.setX(p2.x() - uc)
                p4.setY(p2.y() + uc)
            elif yer.durum == YerDurum.AktifUst:
                p1.setX(int(px + boyut / 2))
                p1.setY(int(py + boyut - 2 * f))
                p2.setX(p1.x())
                p2.setY(int(py + 2 * f))

                p3.setX(p2.x() - uc)
                p3.setY(p2.y() + uc)
                p4.setX(p2.x() + uc)
                p4.setY(p2.y() + uc)

            elif yer.durum == YerDurum.AktifSol:
                p1.setX(int(px + boyut - 2 * f))
                p1.setY(int(py + boyut / 2))
                p2.setX(int(px + 2 * f))
                p2.setY(p1.y())

                p3.setX(p2.x() + uc)
                p3.setY(p2.y() - uc)
                p4.setX(p2.x() + uc)
                p4.setY(p2.y() + uc)

            elif yer.durum == YerDurum.AktifAlt:
                p1.setX(int(px + boyut / 2))
                p1.setY(int(py + 2 * f))
                p2.setX(p1.x())
                p2.setY(int(py + boyut - 2 * f))

                p3.setX(p2.x() - uc)
                p3.setY(p2.y() - uc)
                p4.setX(p2.x() + uc)
                p4.setY(p2.y() - uc)

            painter.drawLine(p1, p2)
            painter.drawLine(p2, p3)
            painter.drawLine(p2, p4)

        painter.end()

    def yerReset(self):
        global Yers
        id = 0
        Yers.clear()
        for x in range(-3, 4):
            for y in range(-3, 4):
                cizme = abs(x) >= 2 and abs(y) >= 2
                if cizme == False:
                    yer = Yer(id, x, y, YerDurum.Dolu)
                    id = id + 1
                    if x == 0 and y == 0:
                        yer.setDurum(YerDurum.Bos)

                    Yers.append(yer)

    def tumYerCiz(self):
        global Yers
        for id in range(0, len(Yers)):
            yer = Yer.getYerId(id)
            self.yerCiz(yer)

    def mousePressEvent(self, event):
        global yer1, bas
        bas = True
        yer = Yer.getYerPixel(self.mapFromGlobal(QCursor.pos()).x(), self.mapFromGlobal(QCursor.pos()).y())
        if yer != None:
            yer1 = yer

    def mouseReleaseEvent(self, event):
        global yer1, yer2, bas, ihtimals, son

        yer = Yer.getYerPixel(self.mapFromGlobal(QCursor.pos()).x(), self.mapFromGlobal(QCursor.pos()).y())
        if yer != None and bas == True:
            yer2 = yer
            self.hareketYap(yer1, yer2)
            bas = False
            self.setIhtimals()
            if len(ihtimals) == 0:
                sk = self.doluSay()
                self.oyunKaydet(son, "son.txt", sk)
                msg = QMessageBox(QMessageBox.Information, "HAMLE KALMADI", "Oyununuzda " + str(sk) + " taş bıraktınız.", QMessageBox.Ok)
                msg.exec_()

    def uzakKomsuMu(self, y1, y2):
        if y1 == None or y2 == None:
            return False
        dx = int(abs(y2.x - y1.x))
        dy = int(abs(y2.y - y1.y))

        return (dy == 0 and dx == 2) or (dx == 0 and dy == 2)

    def getAraKomsu(self, y1, y2):
        if self.uzakKomsuMu(y1, y2):
            if y1.x == y2.x:
                ort_y = int((y1.y + y2.y)/2)
                return Yer.getYerXY(y1.x, ort_y)
            elif y1.y == y2.y:
                ort_x= int((y1.x + y2.x)/2)
                return Yer.getYerXY(ort_x, y1.y)

        return None

    def getHareketOnay(self, y1, y2):
        if self.uzakKomsuMu(y1, y2):
            if y1.durum.value > 1:
                araKomsu = self.getAraKomsu(y1, y2)
                return araKomsu.durum.value > 1 and y2.durum.value < 2
        return False

    def hareketYap(self, y1, y2):
        global islem
        if self.getHareketOnay(y1, y2):
            araKomsu = self.getAraKomsu(y1, y2)
            if y2.x > y1.x:
                y1.setDurum(YerDurum.AktifSag)
            elif y2.x < y1.x:
                y1.setDurum(YerDurum.AktifSol)
            elif y2.y > y1.y:
                y1.setDurum(YerDurum.AktifUst)
            elif y2.y < y1.y:
                y1.setDurum(YerDurum.AktifAlt)

            y2.setDurum(YerDurum.Hedef)
            self.repaint()
            if self.islem == Islem.Oyna:
                time.sleep(0.4)
            elif self.islem == Islem.Dosyadan:
                time.sleep(1)

            y1.setDurum(YerDurum.Bos)
            araKomsu.setDurum(YerDurum.Bos)
            y2.setDurum(YerDurum.Dolu)

            if self.islem == Islem.Oyna:
                son.append(Har(y1.id, y2.id))
            self.repaint()
            return True
        else:
            return False

    def doluSay(self):
        n = 0
        for id in range(0, len(Yers)):
            y1 = Yers[id]
            if y1.durum.value > 1:
                n += 1
        return n


    def setIhtimals(self):
        global Yers, ihtimals
        sonuc = False
        ihtimals = []
        for id in range(0, len(Yers)):
            y1 = Yers[id]
            if y1.durum.value > 1:
                for yon in range(0, 4):
                    y2 = y1.getUzakKomsu(Yon(yon))
                    if y2 != None:
                        if self.getHareketOnay(y1, y2):
                            sonuc = True
                            ihtimals.append(Har(y1.id, y2.id))

        return sonuc

    def rastgeleHareket(self):
        global ihtimals, Yers, son
        ih_sonuc = self.setIhtimals()

        i = None
        if ih_sonuc == False:
            return False
        elif len(ihtimals) == 1:
            i = 0
        else:
            i = random.randrange(0, len(ihtimals))

        ih = ihtimals[i]
        son.append(ih)

        y1 = Yer.getYerId(ih.baslangic)
        y2 = Yer.getYerId(ih.bitis)
        self.hareketYap(y1, y2)
        return True

    def skoraKadarOyna(self, maxskor):
        global skor
        sonskor = 32
        skor = 32
        while sonskor > maxskor:
            self.yerReset()
            sonskor = self.rastgeleOyna()
        print("BİTTİ")

    def oyunKaydet(self, oyunliste, dosya, sk):
        if os.path.exists(dosya):
            os.remove(dosya)

        with open(dosya, 'w') as f:
            for i in range(len(oyunliste)):
                s = str(oyunliste[i].baslangic) + ">" + str(oyunliste[i].bitis) + "\n"
                f.write(s)
                eniyi.append(oyunliste[i])
            f.write("SKOR:" + str(sk))
        f.close()

    def rastgeleOyna(self):
        global skor, eniyi, son
        devam = True
        son = []
        while devam:
            devam = self.rastgeleHareket()

        n = self.doluSay()
        if n < skor:
            skor = n
            eniyi = []

            self.oyunKaydet(son, "son.txt", skor)
        return skor

    def hamleYap(self):
        global son, son_index
        if son_index < len(son):
            y1 = Yer.getYerId(son[son_index].baslangic)
            y2 = Yer.getYerId(son[son_index].bitis)
            self.hareketYap(y1, y2)
            son_index += 1
            return True
        else:
            return False


    def oyunOku(self, dosya):
        global son
        son = []
        try:
            with open(dosya) as f:
                hamle = ""
                while not (hamle.startswith("SKOR")):
                    hamle = f.readline()
                    if not (hamle.startswith('SKOR')):
                        i = hamle.index('>')
                        if i < 1 or i > 2:
                            return False
                        baslangic = int(hamle[0:i])
                        bitis = int(hamle[i + 1::])
                        if baslangic < 0 or baslangic > 32 or bitis < 0 or bitis > 32:
                            return False
                        son.append(Har(baslangic, bitis))
                    else:
                        break
            f.close()
            return True
        except:
            return False


    def dosyadanOyna(self, dosya):
        global son, son_index
        if not(self.oyunOku(dosya)):
            msg = QMessageBox(QMessageBox.Critical, "GEÇERSİZ DOSYA", "Seçtiğiniz dosya geçerli değil",QMessageBox.Ok)
            msg.exec_()
            return
        son_index = 0
        devam = True
        self.yerReset()
        self.tumYerCiz()
        while devam:
            devam = self.hamleYap()
            if self.islem == Islem.Oyna:
                time.sleep(0.1)
            elif self.islem == Islem.Dosyadan:
                time.sleep(0.6)
            self.repaint()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())