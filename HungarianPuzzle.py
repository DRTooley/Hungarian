

import random

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import (QBrush, QColor, QLinearGradient, QPainter,
        QPainterPath, QPalette, QPen)
from PyQt5.QtWidgets import (QWidget)




class ColoredBall(QWidget):
    def __init__(self, mycolor, pos, ring, parent=None):
        super(ColoredBall, self).__init__(parent)

        self.MyColor = mycolor
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

    def GetColor(self):
        return self.MyColor
    def GetPos(self):
        return self.position
    def GetRing(self):
        return self.ring

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
                self.AllBalls.append(ColoredBall(ball.GetColor(), ball.GetPos(), ball.GetRing()))




    def getHeuristicVal(self):
        ballCount = [0, 0, 0, 0]
        #Implement Heuristic here

        for ball in self.AllBalls:
            if(self.sameColorNextAdjacent(ball)):
                ballCount[ball.colNumber]+=1
            else:
                pass#print("False! "+ball.ring+" "+str(ball.position))
        if(ballCount[0] == 9 and ballCount[1] == 9 and ballCount[2] == 8 and ballCount[3] == 8):
            #print("Ball Count [0]:"+str(ballCount[0])+"\n"+"Ball Count [1]:"+str(ballCount[1])+"\n"+"Ball Count [2]:"+str(ballCount[2])+"\n"+ "Ball Count [3]:"+str(ballCount[3])+"\n"+"Solved!")
            return 0
        else:
            #print("Ball Count [0]:"+str(ballCount[0])+"\n"+"Ball Count [1]:"+str(ballCount[1])+"\n"+"Ball Count [2]:"+str(ballCount[2])+"\n"+ "Ball Count [3]:"+str(ballCount[3])+"\n"+"Not Solved!")
            num = int((ballCount[0]+ ballCount[1] + ballCount[2] + ballCount[3] - 34)*(-0.25) + 0.75)
            return num


    def sameColorNextAdjacent(self, ball):
        if(ball.ring is "both"):
            if ball.position == 4:
                for i in range(len(self.AllBalls)):
                    if 5 == self.AllBalls[i].position and ball.colNumber == self.AllBalls[i].colNumber:
                        for j in range(len(self.AllBalls)):
                            if self.AllBalls[j].position == 3:
                                if self.AllBalls[i].ring == self.AllBalls[j].ring and self.AllBalls[i].colNumber == self.AllBalls[j].colNumber:
                                    return True
            else:
                for i in range(len(self.AllBalls)):
                    if 0 == self.AllBalls[i].position and ball.colNumber == self.AllBalls[i].colNumber:
                        for j in range(len(self.AllBalls)):
                            if self.AllBalls[j].position == 18:
                                if self.AllBalls[i].ring == self.AllBalls[j].ring and self.AllBalls[i].colNumber == self.AllBalls[j].colNumber:
                                    return True
        else:
            for i in range(len(self.AllBalls)):
                if (ball.position+1) == self.AllBalls[i].position and ball.colNumber == self.AllBalls[i].colNumber:
                    if ball.ring == self.AllBalls[i].ring or self.AllBalls[i].ring == "both":
                        return True
        return False
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
        undoMap = [2,3,0,1] #choice 0 reverses choice 2, choice 1 reveres choice 3, choice 2 reverses choice 0, choice 3 reveres choice 1
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





##########################################################################################################
################## End Data Structures ###################################################################
##########################################################################################################