
import HungarianPuzzle
import heapq
import gc


##########################################################################################################
################## Code for the data structures ##########################################################
##########################################################################################################

class IDAstarController():
    def __init__(self, puzzle):
        self.Root = IterativeDeepeningAStar(puzzle)
        self.f_limit = 1
        self.PQ = []
        self.NodesExpanded = 0
        heapq.heappush(self.PQ, (self.Root.GetSum(), self.Root))

        self.SolvedNode = None


    def ida_star(self):
        print("Solving...")
        self.f_limit = self.Root.GetHeuristic()
        while True:
            f_next, self.SolvedNode = self.search(heapq.heappop(self.PQ)[1])


            if f_next == 0:
                print("Number of moves to solution       :",self.SolvedNode.GetDepth())
                print("Nodes Expanded in final iteration :", self.NodesExpanded)
                return self.NodesExpanded, self.SolvedNode.GetDepth()
            else:
                pass
                #print("f_next : ", f_next, " (",self.NodesExpanded,")")#Progress Check

            self.PQ = []
            gc.collect()
            heapq.heappush(self.PQ, (self.Root.GetSum(), self.Root))
            self.f_limit = f_next
            self.NodesExpanded=0

    def search(self, node):
        f_next = 100
        temp, SolvedNode = self.expand(node)
        self.NodesExpanded+=1
        while True:
            if temp == 0:
                #print("Solution found, (",SolvedNode.GetSum(),")")
                return 0, SolvedNode
            if temp < f_next:
                f_next = temp

            if len(self.PQ) == 0:
                return f_next, None
            nextNode = heapq.heappop(self.PQ)[1]
            temp, SolvedNode = self.expand(nextNode)

            #if self.NodesExpanded%1000==0:
                #print("f_next : ", f_next, " (",self.NodesExpanded,")")#Progress Check

        return f_next, None

    def expand(self, node):
        self.NodesExpanded+=1
        f = node.GetSum()
        #node.InfoPrint()#Debuging
        if f > self.f_limit:
            #print("f > f_limit: ", f)
            return f, None
        if node.GetHeuristic() == 0:
            #print("Moves made : ", node.GetDepth())
            return 0, node
        f_next = 100
        for i in range(4):

            temp = IterativeDeepeningAStar(node.GetPuzzle(), node.GetDepth()+1,i)
            if temp.GetSum() <= self.f_limit:
                if temp.GetHeuristic() == 0:
                    return 0, temp
                heapq.heappush(self.PQ, (temp.GetSum(),temp))
            elif temp.GetSum() < f_next:
                f_next = temp.GetSum()

        return f_next, None

    def GetSolvedPuzzle(self):
        if self.SolvedNode != None:
            return self.SolvedNode.GetPuzzle()
        else:
            return self.Root.GetPuzzle()

class IterativeDeepeningAStar():
    def __init__(self, puzzle, depth=0, move=None):
        self.Puzzle = HungarianPuzzle.HungarianRings(puzzle)
        self.Depth = depth
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

    def __lt__(self, other):
        if self.GetSum() == other.GetSum():
            return self.GetHeuristic() < other.GetHeuristic()
        else:
            return self.GetSum() < other.GetSum()

    def __gt__(self, other):
        if self.GetSum() == other.GetSum():
            return self.GetHeuristic() > other.GetHeuristic()
        else:
            return self.GetSum() > other.GetSum()


    def InfoPrint(self):
        print("Depth           : ", self.Depth)
        print("Heuristic Value : ", self.HeuristicVal)
        print("My Move         : ", self.Direction)
        print("")

    def GetSum(self):
        return self.Sum
    def GetHeuristic(self):
        return self.HeuristicVal
    def GetDepth(self):
        return self.Depth
    def GetMove(self):
        return self.Direction
#    def GetParentIndex(self):
#        return self.PredecessorIndex
#    def GetIndex(self):
#        return self.MyIndex
    def GetPuzzle(self):
        return self.Puzzle
