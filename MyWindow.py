

import sys

from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
        QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
        QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
        QVBoxLayout)


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


        self.setLayout(mainLayout)

        self.setWindowTitle("Hungarian Solver")

    def createSolver(self):

        self.locations = QGroupBox()
        labels = QGridLayout()


        labelNorth = QLabel("North")
        labelSouth = QLabel("South")
        labelEast = QLabel("East")
        labelWest = QLabel("West")

        labels.addWidget(labelNorth, 1, 2)
        labels.addWidget(labelWest, 2, 1)
        labels.addWidget(labelEast, 2, 3)
        labels.addWidget(labelSouth, 3, 2)
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

        btn_RotateCL = QPushButton("Rotate Left Side Clockwise")
        btn_RotateCCL = QPushButton("Rotate Left Side Counter-Clockwise")

        btn_RotateCR = QPushButton("Rotate Right Side Clockwise")
        btn_RotateCCR = QPushButton("Rotate Right Side Counter-Clockwise")


        btn_Randomize = QPushButton("Randomize the Puzzle")
        btn_Solve = QPushButton("Solve")

        buttonColWidth = 215


        Buttons.addWidget(btn_RotateCL, 1, 0)
        Buttons.addWidget(btn_RotateCCL, 1, 1)
        Buttons.addWidget(btn_RotateCR, 2, 0)
        Buttons.addWidget(btn_RotateCCR, 2, 1)
        Buttons.addWidget(btn_Randomize, 4, 0)
        Buttons.addWidget(btn_Solve, 4, 1)

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

