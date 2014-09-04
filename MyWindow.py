

import sys
import random

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import (QBrush, QColor, QFont, QLinearGradient, QPainter,
        QPainterPath, QPalette, QPen)
from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
        QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
        QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
        QVBoxLayout, QWidget)


class ColoredBall(QWidget):
    def __init__(self, mycolor, pos, ring, parent=None):
        super(ColoredBall, self).__init__(parent)

        self.position = pos
        self.ring = ring
        self.CreatePath()
        self.penColor = QColor("black")
        self.fillColor1 = QColor(mycolor)
        self.fillColor2 = QColor("white")
        self.penWidth = 1
        self.setBackgroundRole(QPalette.Base)

    def setRing(self, ring):
        self.ring = ring

    def setPosition(self, pos):
        if pos == -1:
            self.position = 19
        elif pos == 20:
            self.position = 0
        else:
            self.position = pos
        if self.position == 4 or self.position == 19:
            self.setRing("both")

    def CreatePath(self):
        self.path = QPainterPath()
        self.path.moveTo(60,35)
        self.path.arcTo(10, 10, 50.0, 50.0, 0.0, 360.0)
        self.path.closeSubpath()

    def minimumSizeHint(self):
        return QSize(50, 50)

    def sizeHint(self):
        return QSize(100, 100)



    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.scale(self.width() / 100.0, self.height() / 100.0)

        painter.setPen(
                QPen(self.penColor, self.penWidth, Qt.SolidLine, Qt.RoundCap,
                        Qt.RoundJoin))
        gradient = QLinearGradient(0, 0, 0, 100)
        gradient.setColorAt(0.0, self.fillColor1)
        gradient.setColorAt(1.0, self.fillColor2)
        painter.setBrush(QBrush(gradient))
        painter.drawPath(self.path)



class myWindow(QWidget):
    def __init__(self):
        super(myWindow, self).__init__()

        mainLayout = QHBoxLayout()

        self.createPuzzle()
        mainLayout.addLayout(self.labels)
        self.createControl()
        mainLayout.addLayout(self.Buttons)
        self.btn_RotateCCL.clicked.connect(self.rotateCCL)
        self.btn_RotateCCR.clicked.connect(self.rotateCCR)
        self.btn_RotateCR.clicked.connect(self.rotateCR)
        self.btn_RotateCL.clicked.connect(self.rotateCL)
        self.btn_Randomize.clicked.connect(self.Randomize)
        self.btn_Solve.clicked.connect(self.Solve)

        self.setLayout(mainLayout)

        self.setWindowTitle("Hungarian Solver")

    def rotateCCL(self):
        for i in range(len(self.AllBalls)):
            if self.AllBalls[i].ring is not "right":
                self.AllBalls[i].setRing("left")
                self.AllBalls[i].setPosition(self.AllBalls[i].position-1)
        self.draw()

    def rotateCCR(self):
        for i in range(len(self.AllBalls)):
            if self.AllBalls[i].ring is not "left":
                self.AllBalls[i].setRing("right")
                self.AllBalls[i].setPosition(self.AllBalls[i].position+1)
        self.draw()

    def rotateCL(self):
        for i in range(len(self.AllBalls)):
            if self.AllBalls[i].ring is not "right":
                self.AllBalls[i].setRing("left")
                self.AllBalls[i].setPosition(self.AllBalls[i].position+1)
        self.draw()

    def rotateCR(self):
        for i in range(len(self.AllBalls)):
            if self.AllBalls[i].ring is not "left":
                self.AllBalls[i].setRing("right")
                self.AllBalls[i].setPosition(self.AllBalls[i].position-1)
        self.draw()

    def Randomize(self):
        random.seed()
        turns = random.randint(200,1000)
        for i in range(turns):
            choice = random.randint(0,3)
            if(choice == 0):
                self.rotateCCL()
            elif(choice == 1):
                self.rotateCCR()
            elif(choice == 2):
                self.rotateCL()
            elif(choice == 3):
                self.rotateCR()

    def Solve(self):
        pass

    def draw(self):
        RxDict = [
            6, 5, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 14, 13, 12, 11, 10, 9, 8, 7
        ]

        LxDict = [
            8, 9, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 0, 1, 2, 3, 4, 5, 6, 7
        ]

        yDict = [
            3, 4, 6, 7, 8, 9, 10, 10, 9, 8, 7, 6, 4, 3, 2, 1, 0, 0, 1, 2
        ]


        for i in range(len(self.AllBalls)):

            if self.AllBalls[i].ring is not "left":
                horizontal = RxDict[self.AllBalls[i].position]

            else:
                horizontal = LxDict[self.AllBalls[i].position]

            vertical = yDict[self.AllBalls[i].position]
            self.labels.addWidget(self.AllBalls[i], vertical, horizontal, 2, 1)

    def createPuzzle(self):


        self.labels = QGridLayout()


        self.AllBalls = []

        for i in range(9, 19):
            self.AllBalls.append(ColoredBall("black", i, "right"))
            self.AllBalls.append(ColoredBall("blue", i-4, "left"))

        for i in range(9):
            self.AllBalls.append(ColoredBall("maroon", i, "right"))
            if i == 4:
                self.AllBalls[len(self.AllBalls)-1].setRing("both")
        for i in range(4):
            self.AllBalls.append(ColoredBall("green", i, "left"))
            self.AllBalls.append(ColoredBall("green", i+15, "left"))
        self.AllBalls.append(ColoredBall("green", 19, "both"))

        self.draw()



    def createControl(self):
        self.Buttons = QGridLayout()

        self.btn_RotateCL = QPushButton("Rotate Left Side Clockwise")
        self.btn_RotateCCL = QPushButton("Rotate Left Side Counter-Clockwise")

        self.btn_RotateCR = QPushButton("Rotate Right Side Clockwise")
        self.btn_RotateCCR = QPushButton("Rotate Right Side Counter-Clockwise")


        self.btn_Randomize = QPushButton("Randomize the Puzzle")
        self.btn_Solve = QPushButton("Solve")

        buttonColWidth = 215


        self.Buttons.addWidget(self.btn_RotateCL, 1, 0)
        self.Buttons.addWidget(self.btn_RotateCCL, 1, 1)
        self.Buttons.addWidget(self.btn_RotateCR, 2, 0)
        self.Buttons.addWidget(self.btn_RotateCCR, 2, 1)
        self.Buttons.addWidget(self.btn_Randomize, 4, 0)
        self.Buttons.addWidget(self.btn_Solve, 4, 1)

#        numRows=6 #runs through each row to ensure padding, also adds padding to top and bottom rows
#
#        for i in range(numRows):
#            Buttons.setRowMinimumHeight(i,10)
#
#        Buttons.setColumnMinimumWidth(0, buttonColWidth)
#        Buttons.setColumnMinimumWidth(1, buttonColWidth)




if __name__ == '__main__':

    app = QApplication(sys.argv)
    myWindow = myWindow()
    myWindow.show()
    sys.exit(app.exec_())

