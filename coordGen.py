import random, re, os
import numpy as np

DenseLiving = 0
PatternLiving = 0

def randomCoords(percentFill, x, y, fileName):
  size = x*y
  limit = int(size * percentFill)
  
  # Generate 10,000 points with x, y between 0 and 50
  coords = np.random.randint(0, x-1, (limit, 2))
  coords = [(int(x), int(y)) for x, y in coords]

  with open(fileName, "w") as txt:
    textWrite = f"{coords}"
    textWrite = re.sub("[\[\]]", "", textWrite)
    textWrite = re.sub("[(]", "[", textWrite)
    textWrite = re.sub("[)]", "]", textWrite)
    txt.write(textWrite)
  
  return len(coords)

def randomCoordPattern(types, x, y, fileName, percentage):
  size = x*y
  limit = int(size * percentage)
  outCoords = [] 
  trueOutCoords = [] 

  while len(outCoords) < limit - 1:
    xChoice = random.choice(range(x-9))
    yChoice = random.choice(range(y-9))
    coord = (xChoice, yChoice)

    if not coord in outCoords:
      outCoords.append(coord)
    os.system("cls")
    print(f"Outcoordlen: {len(outCoords)} || limit: {limit}")

  for coord in outCoords:
    pick = random.choice(types)
    for c in pick:
      xNew = coord[0] + c[0]
      yNew = coord[1] + c[1]
      trueOutCoords.append((xNew, yNew))

  with open(fileName, "w") as txt:
    textWrite = f"{trueOutCoords}"
    textWrite = re.sub("[\[\]]", "", textWrite)
    textWrite = re.sub("[(]", "[", textWrite)
    textWrite = re.sub("[)]", "]", textWrite)
    txt.write(textWrite)
  
  return len(trueOutCoords)

lUp =   [(0,0),(0,1),(0,2),(1,0),(2,1)]
rUp =   [(0,1),(1,0),(2,0),(2,1),(2,2)]
lDown = [(0,0),(0,1),(0,2),(1,2),(2,1)]
rDown = [(0,1),(1,2),(2,0),(2,1),(2,2)]

pattens = [lUp, rUp, lDown, rDown]

PatternLiving = randomCoordPattern(pattens, 10000, 10000, "SparseVoidCoords.txt", percentage = 0.000001)
DenseLiving = randomCoords(.50, 1000, 1000, "DenseSoupCoords.txt")
print(f"Dense: {DenseLiving} | PatternLiving: {PatternLiving}")
