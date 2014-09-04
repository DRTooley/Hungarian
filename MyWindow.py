

import sys
from math import cos, pi, sin
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import (QBrush, QColor, QFont, QLinearGradient, QPainter,
        QPainterPath, QPalette, QPen)
from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
        QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
        QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
        QVBoxLayout, QWidget)


class ColoredBall(QWidget):
    def __init__(self, color, ypos, xpos,  parent=None):
        super(ColoredBall, self).__init__(parent)
        self.yPos = ypos
        self.xPos = xpos

        self.CreatePath()

        self.PenColor = QColor("black")
        self.FillColor1 = QColor(color)
        self.FillColor2 = QColor("white")
        self.rotationAngle = 0
        self.PenWidth = 1
        self.setBackgroundRole(QPalette.Base)

    def minimumSizeHint(self):
        return QSize(50, 50)

    def sizeHint(self):
        return QSize(100, 100)

    def setFillRule(self, rule):
        self.path.setFillRule(rule)
        self.update()

    def setFillGradient(self, color1, color2):
        self.FillColor1 = color1
        self.FillColor2 = color2
        self.update()

    def setPenWidth(self, width):
        self.penWidth = width
        self.update()

    def setPenColor(self, color):
        self.penColor = color
        self.update()

    def setRotationAngle(self, degrees):
        self.rotationAngle = degrees
        self.update()


    def CreatePath(self):
        self.path = QPainterPath()
        self.path.arcMoveTo(self.yPos, self.xPos, 50.0, 60.0, 360.0)
        self.path.closeSubpath()
        self.path.setFillRule(Qt.FillRule(Qt.WindingFill))


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.scale(self.width() / 100.0, self.height() / 100.0)
        painter.translate(50.0, 50.0)
        painter.rotate(-self.rotationAngle)
        painter.translate(-50.0, -50.0)

        painter.setPen(
                QPen(self.PenColor, self.PenWidth, Qt.SolidLine, Qt.RoundCap,
                        Qt.RoundJoin))
        gradient = QLinearGradient(0, 0, 0, 100)
        gradient.setColorAt(0.0, self.FillColor1)
        gradient.setColorAt(1.0, self.FillColor2)
        painter.setBrush(QBrush(gradient))
        painter.drawPath(self.path)


class myWindow(QWidget):
    def __init__(self):
        super(myWindow, self).__init__()


        self.createControl()
        self.createPuzzle()

        mainLayout = QHBoxLayout()
        mainLayout.addLayout(self.Buttons)
        mainLayout.addLayout(self.labels)

        self.btn_RotateCCL.clicked.connect(self.rotateCCL)
        self.btn_RotateCCR.clicked.connect(self.rotateCCR)
        self.btn_RotateCR.clicked.connect(self.rotateCR)
        self.btn_RotateCL.clicked.connect(self.rotateCL)
        self.btn_Randomize.clicked.connect(self.Randomize)
        self.btn_Solve.clicked.connect(self.Solve)

        self.setLayout(mainLayout)

        self.setWindowTitle("Hungarian Solver")

    def rotateCCL(self):
        pass

    def rotateCCR(self):
        pass

    def rotateCL(self):
        pass

    def rotateCR(self):
        pass

    def Randomize(self):
        pass

    def Solve(self):
        pass

    def createPuzzle(self):


        self.labels = QGridLayout()


        self.labelNorth = ColoredBall("black",50.0,200.0)
        self.labelSouth = ColoredBall("maroon",150.0,200.0)
        self.labelEast = ColoredBall("green",100.0,150.0)
        self.labelWest = ColoredBall("blue",100.0,250.0)

        self.labels.addWidget(self.labelNorth, 1, 2)
        self.labels.addWidget(self.labelWest, 2, 1)
        self.labels.addWidget(self.labelEast, 2, 3)
        self.labels.addWidget(self.labelSouth, 3, 2)
#        numCols = 4
#        numRows = 5
#        for i in range(numRows):
#            labels.setRowMinimumHeight(i, 50)
#        for j in range(numCols):
#            labels.setColumnMinimumWidth(j, 50)



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

