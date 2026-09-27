import re, os, sys, time, tracemalloc

class universe:
    w = 0
    h = 0
    generations = 0
    living_Cells = 0
    living_Cell_Pos = []
    
    def show(self): # Need improvement ############ DOES NOT WORK #####################
        os.system("cls")
        for row in self.uniList:
            for i in row:
                if i == 0:
                    print("_     ", end="")
                else:
                    print("X     ", end="")
            print("\n")
    
    def showStats(self):
        print(f"Width: {self.w}\tHeight: {self.h}\nGenerations: {self.generations+1}\tLivingCellCount: {self.living_Cells}\nLivingCellPos:\n{self.living_Cell_Pos}")

    def inputFile(self, filePath: str = "output.txt"):
        with open(filePath, "r") as txt:
            line1 = txt.readline().split(" ") # width height
            for i in range(len(line1)):
                line1[i] = int(line1[i])
            self.w = int(line1[0])
            self.h = int(line1[1])

            line2 = int(txt.readline()) # Generations
            self.generations = (line2)

            line3 = int(txt.readline()) # Living cells
            self.living_Cells = int(line3)

            line4 = txt.readline().split("],") # Alive coords
            self.living_Cell_Pos.clear()
            for i in range(len(line4)): # Make coords
                line4[i] = re.sub("[,\[\] ]", "", line4[i])
                self.living_Cell_Pos.append([int(line4[i][0]),int(line4[i][1])])
            
    def outputFile(self, outputFile: str = "output.txt"):
        with open(outputFile, "w") as txt:
            livingCellPos = f"{self.living_Cell_Pos}"
            livingCellPos = livingCellPos[1:-1]
            txt.write(f"{self.w} {self.h}\n{self.generations}\n{self.living_Cells}\n{livingCellPos}")
    
    def detectMatrix(self, x, y) -> list:
        thingsToProcess = [[x-1, y-1], [x, y-1], [x+1, y-1],
                           [x-1, y], [x, y], [x+1, y],
                           [x-1, y+1], [x, y+1], [x+1, y+1]]

        return thingsToProcess
    """    
    def rules(self, repeats: int, alive: bool) -> int: # Using living cell count and uses conways rules to determine if cell lives (1) or dies (0)
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
    """

    def startGenerations(self, generation: int, display: bool = False, speed: float = .2):
        for i in range(generation):

            if display:
                self.show()
                self.showStats()
                time.sleep(speed)
            
            self.living_Cell_Pos.sort()
            print(f"\nCells: {self.living_Cell_Pos} | Gen: {i}")

            thingsToProcess = []
            for coord in self.living_Cell_Pos: # This makes 3x3 area to find repeats
                test = self.detectMatrix(coord[0], coord[1])
                thingsToProcess += test
            thingsToProcess.sort() # This processes the repeats to a dictionary with how many repeats were found
            thingsToProcess = [f"{thingsToProcess[i]}" for i in range(len(thingsToProcess))]
            repeats = {i:thingsToProcess.count(i) for i in thingsToProcess}

            cellsToRemove = []
            for cell in self.living_Cell_Pos: # Checks living cell repeats and can kill it
                # print(f"Cell repeats: {cell}: {repeats[f'{cell}']-1}") 
                if repeats[f'{cell}']-1 > 3 or repeats[f'{cell}']-1 < 2:
                    cellsToRemove.append(cell)
                    repeats.pop(f'{cell}')
                elif repeats[f'{cell}'] == 3:
                    repeats.pop(f'{cell}')

            for cell in cellsToRemove: # Kills all living cells that need to
                self.living_Cell_Pos.remove(cell)
            
            for cell in list(repeats.keys()): # Should handled all alive cells by now, update dead cells
                if repeats[cell] == 3: # Revive dead cells
                    cell = re.sub("[\[\] ]", "", cell)
                    cell = cell.split(",")
                    cell = [int(cell[0]), int(cell[1])]
                    self.living_Cell_Pos.append(cell)


            """ # OLD CODE
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
            """

if __name__ == "__main__":
    args = sys.argv

    display = False
    save = False
    useInput = True
    inputFile = "output.txt"
    outputFile = "output2.txt"
    generations = 5

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

    print(f"\n\nCompleted in {(stopTime - startTime):.3f} seconds!!!")
    print(f"Current MALLOC: {current}, Peak MALLOC: {peak}")
