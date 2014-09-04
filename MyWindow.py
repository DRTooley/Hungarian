

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
        self.FillColor = QColor(color)
        self.PenWidth = 1
        self.setBackgroundRole(QPalette.Base)


    def CreatePath(self):
        self.path = QPainterPath()
        self.path.arcMoveTo(self.yPos, self.xPos, 10.0, 10.0, 360.0)
        self.path.closeSubpath()


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.scale(self.width() / 100.0, self.height() / 100.0)
        painter.translate(50.0, 50.0)
        painter.rotate(0)
        painter.translate(-50.0, -50.0)

        painter.setPen(
                QPen(self.PenColor, self.PenWidth, Qt.SolidLine, Qt.RoundCap,
                        Qt.RoundJoin))
        gradient = QLinearGradient(0, 0, 0, 100)
        gradient.setColorAt(0.0, self.FillColor)
        gradient.setColorAt(1.0, self.FillColor)
        painter.setBrush(QBrush(gradient))
        painter.drawPath(self.path)


class myWindow(QDialog):
    def __init__(self):
        super(myWindow, self).__init__()

        self.createMenu()
        self.createControl()
        self.createSolver()

        mainLayout = QHBoxLayout()
        mainLayout.setMenuBar(self.menuBar)
        mainLayout.addWidget(self.controls)
        mainLayout.addWidget(self.locations)

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

    def createSolver(self):

        self.locations = QGroupBox()
        labels = QGridLayout()


        self.labelNorth = ColoredBall("black",50,150)
        self.labelSouth = QLabel("South")
        self.labelEast = QLabel("East")
        self.labelWest = QLabel("West")

        labels.addWidget(self.labelNorth, 1, 2)
        labels.addWidget(self.labelWest, 2, 1)
        labels.addWidget(self.labelEast, 2, 3)
        labels.addWidget(self.labelSouth, 3, 2)
        numCols = 4
        numRows = 5
        for i in range(numRows):
            labels.setRowMinimumHeight(i, 50)
        for j in range(numCols):
            labels.setColumnMinimumWidth(j, 50)

        self.locations.setLayout(labels)

    def createControl(self):
        self.controls = QGroupBox()
        Buttons = QGridLayout()

        self.btn_RotateCL = QPushButton("Rotate Left Side Clockwise")
        self.btn_RotateCCL = QPushButton("Rotate Left Side Counter-Clockwise")

        self.btn_RotateCR = QPushButton("Rotate Right Side Clockwise")
        self.btn_RotateCCR = QPushButton("Rotate Right Side Counter-Clockwise")


        self.btn_Randomize = QPushButton("Randomize the Puzzle")
        self.btn_Solve = QPushButton("Solve")

        buttonColWidth = 215


        Buttons.addWidget(self.btn_RotateCL, 1, 0)
        Buttons.addWidget(self.btn_RotateCCL, 1, 1)
        Buttons.addWidget(self.btn_RotateCR, 2, 0)
        Buttons.addWidget(self.btn_RotateCCR, 2, 1)
        Buttons.addWidget(self.btn_Randomize, 4, 0)
        Buttons.addWidget(self.btn_Solve, 4, 1)

        numRows=6 #runs through each row to ensure padding, also adds padding to top and bottom rows

        for i in range(numRows):
            Buttons.setRowMinimumHeight(i,10)

        Buttons.setColumnMinimumWidth(0, buttonColWidth)
        Buttons.setColumnMinimumWidth(1, buttonColWidth)

        self.controls.setLayout(Buttons)

    def createMenu(self):
        self.menuBar = QMenuBar()

        self.fileMenu = QMenu("File", self)
        self.exitAction = self.fileMenu.addAction("Exit")
        self.menuBar.addMenu(self.fileMenu)

        self.exitAction.triggered.connect(self.accept)


if __name__ == '__main__':



    app = QApplication(sys.argv)
    dialog = myWindow()
    sys.exit(dialog.exec_())

