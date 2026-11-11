import re, os, sys, time, tracemalloc

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
        os.system("cls")
        for row in self.uniList:
            for i in row:
                if i == 0:
                    print("_     ", end="")
                else:
                    print("X     ", end="")
            print("\n")
    
    def showStats(self):
        print(f"Width: {self.w}\tHeight: {self.h}\nGenerations: {self.generations+1}\tLivingCellCount: {self.living_Cells}\nTime: {time.localtime()}")

    def inputFile(self, filePath: str = "output.txt"):
        with open(filePath, "r") as txt:
            line1 = txt.readline().split(" ") # width height
            for i in range(len(line1)):
                line1[i] = int(line1[i])
            self.w = int(line1[0])
            self.h = int(line1[1])
            self.uniList = [[0 for _ in range(self.w)] for _ in range(self.h)]

            line2 = int(txt.readline()) # Generations
            self.generations = (line2)

            line3 = int(txt.readline()) # Living cells
            self.living_Cells = int(line3)

            line4 = txt.readline().split("],") # Alive coords
            self.living_Cell_Pos.clear()
            for i in range(len(line4)):
                line4[i] = re.sub("[,\[\] ]", "", line4[i])
                self.living_Cell_Pos.append([int(line4[i][0]),int(line4[i][1])])
            for pos in self.living_Cell_Pos:
                self.uniList[pos[1]][pos[0]] = 1
            
    def outputFile(self, outputFile: str = "output.txt"):
        with open(outputFile, "w") as txt:
            livingCellPos = f"{self.living_Cell_Pos}"
            livingCellPos = livingCellPos[1:-1]
            txt.write(f"{self.w} {self.h}\n{self.generations}\n{self.living_Cells}\n{livingCellPos}")
    
    def detect(self, x, y) -> int:
        alive = 0
        thingsToProcess = [[x-1, y-1], [x, y-1], [x+1, y-1],
                           [x-1, y], [x+1, y],
                           [x-1, y+1], [x, y+1], [x+1, y+1]]

        for pos in thingsToProcess:
            if not ((pos[0] <= -1 or pos[1] <= -1) or (pos[0] >= self.w or pos[1] >= self.h)):
                if self.uniList[pos[1]][pos[0]] == 1:
                    alive += 1
        return alive
    
    def rules(self, aliveCount: int, alive: bool) -> int: # Using living cell count and uses conways rules to determine if cell lives (1) or dies (0)
        if alive and aliveCount < 2:
            return 0
        if alive and aliveCount > 3:
            return 0
        if aliveCount == 3:
            return 1
        if not alive:
            return 0
        if alive:
            return 1

    def startGenerations(self, generation: int, display: bool = False, speed: float = .2):
        for i in range(generation):

            self.showStats()

            if display:
                self.show()
                self.showStats()
                time.sleep(speed)

            uniListUpdates = [[0 for _ in range(self.w)] for _ in range(self.h)]
            for y in range(self.h):
                for x in range(self.w):
                    # Detect what cells live or die and update lists, then after, complete list conversion to update death and life
                    detected = self.detect(x, y)
                    currentCell = self.rules(detected, self.uniList[y][x]==1)

                    if currentCell == 1: # Alive
                        if not self.living_Cell_Pos.__contains__([x,y]):
                            self.living_Cell_Pos.append([x,y])
                            self.living_Cells += 1
                    else: # Dead
                        if self.living_Cell_Pos.__contains__([x,y]):
                            self.living_Cell_Pos.remove([x,y])
                            self.living_Cells -= 1

                    uniListUpdates[y][x] = currentCell
            self.uniList = uniListUpdates
            self.generations += 1

if __name__ == "__main__":
    args = sys.argv

    display = False
    save = True
    useInput = True
    inputFile = "DenseSoup_CaseA.txt"
    outputFile = "output.txt"
    generations = 200

    for arg in args: # Check and parse cmd arguments
        match arg:
            case "--save":
                save = True
            case "--graphics":
                display = True
            case "--output":
                outputFile = args[args.index("--output") + 1] 
                save = True
            case "--input":
                inputFile = args[args.index("--input") + 1]
                useInput = True
            case "--gen":
                generations = int(args[args.index("--gen") + 1])
    
    uni1 = universe() #Init default
    if useInput:
        uni1.inputFile(inputFile)

    tracemalloc.start()
    startTime = time.time()
    uni1.startGenerations(generation=generations, display=display, speed=.5)
    stopTime = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    if save:
        uni1.outputFile(outputFile)

    print(f"Completed in {(stopTime - startTime):.3f} seconds!!!")
    print(f"Current MALLOC: {current}, Peak MALLOC: {peak}")
