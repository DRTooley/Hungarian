

import sys
import random

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import (QBrush, QColor, QFont, QLinearGradient, QPainter,
        QPainterPath, QPalette, QPen)
from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
        QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
        QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
        QVBoxLayout, QWidget)

##########################################################################################################
################## Code for the data structures ##########################################################
##########################################################################################################

class IDAstarController():
    def __init__(self, puzzle):
        self.Root = IterativeDeepeningAStar(puzzle)
        self.f_limit = 1
        self.Solved = False
        self.Tree = [self.Root, None, None, None]

        self.ida_star()

    def ida_star(self):
        self.f_limit = self.Root.GetHeuristic()
        while not self.Solved:
            f_next = self.search(self.Root)
            print("f_next: ", f_next)
            if f_next == 0:
                return
            self.Tree = [self.Root, None, None, None]
            self.f_limit = f_next

    def search(self, node):
        f = node.GetSum()
        if f > self.f_limit:
            #print("f > f_limit: ", f)
            return f
        if node.GetHeuristic() == 0:
            print("Solution found at ["+ str(node.GetIndex()[0]) + ", " +str(node.GetIndex()[1]) + "] - (in node)")
            return 0
        f_next = 100
        for child in self.expand(node):
            temp = self.search(child)
            if temp == 0:
                print("Solution found at ["+ str(child.GetIndex()[0]) + ", " +str(child.GetIndex()[1]) + "] (in expand)")
                return 0
            if temp < f_next:
                f_next = temp

        return f_next

    def expand(self, node):
        myArr = []
        for i in range(4):
            myArr.append(IterativeDeepeningAStar(node.GetPuzzle(), node.GetDepth()+1, node.GetIndex(), [len(self.Tree),i],i))
        self.Tree.append(myArr)
        return myArr

class IterativeDeepeningAStar():
    def __init__(self, puzzle, depth=0, parentnumber=[None,None], mynumber=[0,0], move=None):
        self.Puzzle = HungarianRings(puzzle)
        self.Depth = depth
        self.PredecessorIndex = parentnumber
        self.MyIndex = mynumber
        self.Direction = move

        if(self.Direction == 0):
                self.Puzzle.rotateCCL()
        elif(self.Direction == 1):
                self.Puzzle.rotateCCR()
        elif(self.Direction == 2):
                self.Puzzle.rotateCL()
        elif(self.Direction == 3):
                self.Puzzle.rotateCR()

        self.HeuristicVal = self.Puzzle.getHeuristicVal()
        self.Sum = self.HeuristicVal + self.Depth

    def GetSum(self):
        return self.Sum
    def GetHeuristic(self):
        return self.HeuristicVal
    def GetDepth(self):
        return self.Depth
    def GetMove(self):
        return self.Direction
    def GetParentIndex(self):
        return self.PredecessorIndex
    def GetIndex(self):
        return self.MyIndex
    def GetPuzzle(self):
        return self.Puzzle


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

        colDict = {"black":0, "blue":1, "maroon":2, "green":3}

        self.colNumber = colDict[mycolor]

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




class HungarianRings:
    def __init__(self, CopyPuzzle=None):
        self.AllBalls = []
        if CopyPuzzle==None:
            self.createPuzzle()
        else:
            for ball in CopyPuzzle.GetBalls():
                self.AllBalls.append(ball)


    def getHeuristicVal(self):
        ballCount = [0, 0, 0, 0]
        #Implement Heuristic here

        for ball in self.AllBalls:
            if(self.sameColorRightAdjacent(ball)):
                ballCount[ball.colNumber]+=1
            else:
                pass#print("False! "+ball.ring+" "+str(ball.position))
        if(ballCount[0] == 9 and ballCount[1] == 9 and ballCount[2] == 8 and ballCount[3] == 8):
            #print("Ball Count [0]:"+str(ballCount[0])+"\n"+"Ball Count [1]:"+str(ballCount[1])+"\n"+"Ball Count [2]:"+str(ballCount[2])+"\n"+ "Ball Count [3]:"+str(ballCount[3])+"\n"+"Solved!")
            return 0
        else:
            #print("Ball Count [0]:"+str(ballCount[0])+"\n"+"Ball Count [1]:"+str(ballCount[1])+"\n"+"Ball Count [2]:"+str(ballCount[2])+"\n"+ "Ball Count [3]:"+str(ballCount[3])+"\n"+"Not Solved!")
            num = int((ballCount[0]+ ballCount[1] + ballCount[2] + ballCount[3] - 34)*(-0.5))
            return num

##########################################################################################################
################## Code for the randomizer ###############################################################
##########################################################################################################

    def choose(self):
        choice = random.randint(0, 3)
        if(choice == 0):
            if self.incrementTracker(choice):
                self.rotateCCL()
        elif(choice == 1):
            if self.incrementTracker(choice):
                self.rotateCCR()
        elif(choice == 2):
            if self.incrementTracker(choice):
                self.rotateCL()
        elif(choice == 3):
            if self.incrementTracker(choice):
                self.rotateCR()

    def incrementTracker(self, choice):
        undoMap = [2,3,0,1]
        if(self.tracker[0] == choice):
            if self.tracker[1] <9:
                self.tracker[1]+=1
                return True
            else:
                self.choose()
                return False
        elif undoMap[choice] == self.tracker[0]: #if the new choice undoes the last choice choose again
            self.choose()
            return False
        else:
            tracker = [choice, 1]
            return True

    def Randomize(self, turns):
        random.seed()
        self.tracker = [0, 0]
        for i in range(turns):
            self.choose()

    def GetBalls(self):
        return self.AllBalls


##########################################################################################################
################## End Randomizer ########################################################################
##########################################################################################################

    def createPuzzle(self):

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




    def rotateCCL(self):
        for i in range(len(self.AllBalls)):
            if self.AllBalls[i].ring is not "right":
                self.AllBalls[i].setRing("left")
                self.AllBalls[i].setPosition(self.AllBalls[i].position-1)

    def rotateCCR(self):
        for i in range(len(self.AllBalls)):
            if self.AllBalls[i].ring is not "left":
                self.AllBalls[i].setRing("right")
                self.AllBalls[i].setPosition(self.AllBalls[i].position+1)

    def rotateCL(self):
        for i in range(len(self.AllBalls)):
            if self.AllBalls[i].ring is not "right":
                self.AllBalls[i].setRing("left")
                self.AllBalls[i].setPosition(self.AllBalls[i].position+1)

    def rotateCR(self):
        for i in range(len(self.AllBalls)):
            if self.AllBalls[i].ring is not "left":
                self.AllBalls[i].setRing("right")
                self.AllBalls[i].setPosition(self.AllBalls[i].position-1)


    def sameColorRightAdjacent(self, ball):
        if(ball.ring is "both"):
            if ball.position == 4:
                for i in range(len(self.AllBalls)):
                    if 5 == self.AllBalls[i].position and ball.colNumber == self.AllBalls[i].colNumber:
                        return True
            else:
                for i in range(len(self.AllBalls)):
                    if 0 == self.AllBalls[i].position and ball.colNumber == self.AllBalls[i].colNumber:
                        return True
        else:
            for i in range(len(self.AllBalls)):
                if (ball.position+1) == self.AllBalls[i].position and ball.colNumber == self.AllBalls[i].colNumber:
                    if ball.ring == self.AllBalls[i].ring or self.AllBalls[i].ring == "both":
                        return True
        return False


##########################################################################################################
################## End Data Structures ###################################################################
##########################################################################################################


class myGUI(QWidget):
    def __init__(self):
        super(myGUI, self).__init__()

        mainLayout = QHBoxLayout()
        self.labels = QGridLayout()
        self.HR = HungarianRings()
        mainLayout.addLayout(self.labels)
        self.draw()
        self.createControl()
        mainLayout.addLayout(self.Buttons)
        self.btn_RotateCCL.clicked.connect(self.rotateCCL)
        self.btn_RotateCCR.clicked.connect(self.rotateCCR)
        self.btn_RotateCR.clicked.connect(self.rotateCR)
        self.btn_RotateCL.clicked.connect(self.rotateCL)
        self.btn_Randomize.clicked.connect(self.Randomize)
        self.btn_Reset.clicked.connect(self.Reset)
        self.btn_Solve.clicked.connect(self.IDAstar)

        self.setLayout(mainLayout)

        self.setWindowTitle("Hungarian Solver")

    def IDAstar(self):
        IDAstarController(self.HR)

    def Reset(self):
        self.HR = HungarianRings()
        self.draw()

    def rotateCCL(self):
        self.HR.rotateCCL()
        self.draw()

    def rotateCCR(self):
        self.HR.rotateCCR()
        self.draw()

    def rotateCL(self):
        self.HR.rotateCL()
        self.draw()

    def rotateCR(self):
        self.HR.rotateCR()
        self.draw()

    def Randomize(self):
        self.HR.Randomize(self.RanomizeCounter.value())
        self.draw()

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


        for i in range(len(self.HR.AllBalls)):

            if self.HR.AllBalls[i].ring is not "left":
                horizontal = RxDict[self.HR.AllBalls[i].position]

            else:
                horizontal = LxDict[self.HR.AllBalls[i].position]

            vertical = yDict[self.HR.AllBalls[i].position]
            self.labels.addWidget(self.HR.AllBalls[i], vertical, horizontal, 2, 2)





    def createControl(self):
        self.Buttons = QGridLayout()

        self.btn_Reset = QPushButton("Reset")
        self.btn_RotateCL = QPushButton("Rotate Left Side Clockwise")
        self.btn_RotateCCL = QPushButton("Rotate Left Side Counter-Clockwise")

        self.btn_RotateCR = QPushButton("Rotate Right Side Clockwise")
        self.btn_RotateCCR = QPushButton("Rotate Right Side Counter-Clockwise")
        self.btn_Solve = QPushButton("Solve")


        self.btn_Randomize = QPushButton("Randomize the Puzzle")
        self.RanomizeCounter = QSpinBox()
        self.RanomizeCounter.setRange(0, 99999999)
        self.RanomizeCounter.setSingleStep(1)





        self.Buttons.addWidget(self.btn_RotateCL, 1, 0)
        self.Buttons.addWidget(self.btn_RotateCCL, 1, 1)
        self.Buttons.addWidget(self.btn_RotateCR, 2, 0)
        self.Buttons.addWidget(self.btn_RotateCCR, 2, 1)
        self.Buttons.addWidget(self.btn_Randomize, 4, 0)
        self.Buttons.addWidget(self.RanomizeCounter, 4, 1)
        self.Buttons.addWidget(self.btn_Reset,5,1)
        self.Buttons.addWidget(self.btn_Solve,5,0)








if __name__ == '__main__':

    app = QApplication(sys.argv)
    myGUI = myGUI()
    myGUI.show()
    sys.exit(app.exec_())

