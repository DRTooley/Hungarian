

import sys
import random
import plotly.plotly as py
from plotly.graph_objs import *

import HungarianPuzzle
import IDAStar


from PyQt5.QtWidgets import (QApplication, QGridLayout,QHBoxLayout, QPushButton, QSpinBox, QWidget)


class myGUI(QWidget):
    def __init__(self):
        super(myGUI, self).__init__()

        mainLayout = QHBoxLayout()
        self.labels = QGridLayout()
        self.HR = HungarianPuzzle.HungarianRings()
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
        self.btn_solve_five_graph.clicked.connect(self.SolveAndPlot)

        self.setLayout(mainLayout)

        self.setWindowTitle("Hungarian Solver ")

    def SolveAndPlot(self):
        graphplots = []
        random.seed()

        for i in range(5):
            self.HR = HungarianPuzzle.HungarianRings()
            choice = random.randint(9, 13)
            print("Next puzzle is randomized",choice,"times!")
            self.RanomizeCounter.setValue(choice)
            self.Randomize()
            self.draw()
            Ctrl = IDAStar.IDAstarController(self.HR)
            graphplots.append(Ctrl.ida_star())

        self.draw()

        self.graph(graphplots)


    def graph(self,gp):
        x1=[]
        y1=[]
        py.sign_in('Python-Demo-Account', 'gwt101uhh0')
        for row in gp:
            y1.append(row[0])
            x1.append(row[1])

        trace1 = Scatter(
            x=[x1[0], x1[1], x1[2], x1[3], x1[4]],
            y=[y1[0], y1[1], y1[2], y1[3], y1[4]],
            mode='markers',
            name='Runtime Data',
            text=['Run 1', 'Run 2', 'Run 3', 'Run 4', 'Run 5'],
            marker=Marker(
                color='rgb(164, 194, 244)',
                size=12,
                line=Line(
                    color='white',
                    width=0.5
                )
            )
        )
        data = Data([trace1])
        layout = Layout(
            title='IDA* Results',
            xaxis=XAxis(
                title='Depth'
            ),
            yaxis=YAxis(
                title='Nodes Expanded'
            )
        )
        fig = Figure(data=data, layout=layout)
        plot_url = py.plot(fig, filename='Run Time Data')


    def IDAstar(self):
        Ctrl = IDAStar.IDAstarController(self.HR)
        Ctrl.ida_star()
        self.HR = Ctrl.GetSolvedPuzzle()
        self.draw()

    def Reset(self):
        self.HR = HungarianPuzzle.HungarianRings()
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

        self.btn_solve_five_graph = QPushButton("Randomize, Solve 5, Graph")
        self.btn_Reset = QPushButton("Reset")
        self.btn_RotateCL = QPushButton("Rotate Left Side Clockwise")
        self.btn_RotateCCL = QPushButton("Rotate Left Side Counter-Clockwise")

        self.btn_RotateCR = QPushButton("Rotate Right Side Clockwise")
        self.btn_RotateCCR = QPushButton("Rotate Right Side Counter-Clockwise")
        self.btn_Solve = QPushButton("Solve")

        self.btn_Randomize = QPushButton("Randomize the Puzzle")
        self.RanomizeCounter = QSpinBox()
        self.RanomizeCounter.setRange(1, 100)
        self.RanomizeCounter.setSingleStep(1)

       # self.Buttons.addWidget(self.self.btn_solve_five_graph, 6, 0)
        self.Buttons.addWidget(self.btn_RotateCL, 1, 0)
        self.Buttons.addWidget(self.btn_RotateCCL, 1, 1)
        self.Buttons.addWidget(self.btn_RotateCR, 2, 0)
        self.Buttons.addWidget(self.btn_RotateCCR, 2, 1)
        self.Buttons.addWidget(self.btn_Randomize, 4, 0)
        self.Buttons.addWidget(self.RanomizeCounter, 4, 1)
        self.Buttons.addWidget(self.btn_Reset,5,1)
        self.Buttons.addWidget(self.btn_Solve,5,0)
        self.Buttons.addWidget(self.btn_solve_five_graph,6,0)











if __name__ == '__main__':

    app = QApplication(sys.argv)

    Puzzle = myGUI()
    Puzzle.show()

    sys.exit(app.exec_())
