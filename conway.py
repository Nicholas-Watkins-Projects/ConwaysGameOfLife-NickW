
class universe:
    w = 0
    h = 0
    generations = 0
    living_Cells = 0
    living_Cell_Pos = []
    uniList = []

    def __init__(self, width = 14, height = 14, AliveList = [[1,2],[2,3],[3,3],[3,2],[3,1]]):
        self.w = width
        self.h = height
        self.living_Cells = len(AliveList)
        self.living_Cell_Pos = AliveList
        self.uniList = [[0 for _ in range(width)] for _ in range(height)]
        for pos in AliveList:
            self.uniList[pos[1]][pos[0]] = 1
    
    def show(self):
        for row in self.uniList:
            for i in row:
                if i == 0:
                    print("_     ", end="")
                else:
                    print("X     ", end="")
            print("\n")
    
    def output(self):
        with open("output.txt", "w") as txt:
            livingCellPos = f"{self.living_Cell_Pos}"
            livingCellPos = livingCellPos[1:-1]
            txt.write(f"{self.w} {self.h}\n{self.generations}\n{self.living_Cells}\n{livingCellPos}")
    
    def detect(self, x, y) -> int:
        alive = 0
        thingsToProcess = [[x-1, y-1], [x, y-1], [x+1, y-1],
                           [x-1, y], [x, y], [x+1, y],
                           [x-1, y+1], [x, y+1], [x+1, y+1]]
        for pos in thingsToProcess:
            if not (pos[0] <= -1 or pos[1] <= -1):
                if self.uniList[pos[1]][pos[0]] == 1:
                    alive += 1

    def startGenerations(self, generation: int):
        for i in range(generation):

            toLive = []
            toDie = []
            
            for i in range(self.uniList):
                for j in range(i):
                    # Detect what cells live or die and update lists, then after, complete list conversion to update death and life
                    pass


            pass
        



uni1 = universe()
uni1.show()
uni1.output()

# Haskell check it out, OCaml for functional programming