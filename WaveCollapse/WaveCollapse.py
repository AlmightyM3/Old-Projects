import pygame
import random

WindowSize = 600
pygame.init()
window = pygame.display.set_mode((WindowSize, WindowSize))
clock = pygame.time.Clock()

GridDivider = 30
GridCount = WindowSize//GridDivider

SandImage = pygame.image.load('WaveCollapse/sand.png')
GrassImage = pygame.image.load('WaveCollapse/grass.png')
WaveImage = pygame.image.load('WaveCollapse/wave.png')
MountainImage = pygame.image.load('WaveCollapse/mountain.png')
TreeImage = pygame.image.load('WaveCollapse/tree.png')
Size = (GridDivider,GridDivider)
ScaledGrassImage = pygame.transform.scale(GrassImage, Size)
ScaledSandImage = pygame.transform.scale(SandImage, Size)
ScaledWaveImage = pygame.transform.scale(WaveImage, Size)
ScaledMountainImage = pygame.transform.scale(MountainImage, Size)
ScaledTreeImage = pygame.transform.scale(TreeImage, Size)

Grid = [[0 for i in range(GridCount)] for j in range(GridCount)]

def GetValue(x,y):
    try: 
        value = Grid[x][y]
        onScreen = True 
    except:
        value = 0
        onScreen = False
    result = [value, onScreen]
    return result

def GetNeighborsAxis(x,y):
    N  = GetValue(x,y-1)[0]
    E  = GetValue(x+1,y)[0]
    S  = GetValue(x,y+1)[0]
    W  = GetValue(x-1,y)[0]
    
    neighbors = [N,E,S,W]
    return neighbors
def GetNeighborCoordinatesAxis(x,y):
    N  = [x,y-1]
    E  = [x+1,y]
    S  = [x,y+1]
    W  = [x-1,y]
    
    neighbors = [N,E,S,W]
    return neighbors

def RemoveItems(TargetList, item):
    c = TargetList.count(item)
    for i in range(c):
        TargetList.remove(item)
    return TargetList

def DrawGrid():
    for x in range(GridCount):
        pygame.draw.line(window, (255, 255, 255), (x*GridDivider,0), (x*GridDivider,WindowSize))
    for y in range(GridCount):
        pygame.draw.line(window, (255, 255, 255), (0,y*GridDivider), (WindowSize,y*GridDivider))
        
def DrawScreen():
    window.fill((0,0,0))
    
    y = 0
    for row in Grid:
        x=0
        for i in row:
            if i == 1:
                window.blit(ScaledGrassImage, (y*GridDivider, x*GridDivider))
            elif i == 2:
                window.blit(ScaledSandImage, (y*GridDivider, x*GridDivider))
            elif i == 3:
                window.blit(ScaledWaveImage, (y*GridDivider, x*GridDivider))
            elif i == 4:
                window.blit(ScaledMountainImage, (y*GridDivider, x*GridDivider))
            elif i == 5:
                window.blit(ScaledTreeImage, (y*GridDivider, x*GridDivider))
            x+=1
        y+=1
    
    DrawGrid()
    pygame.display.update()
    
DrawGrid()

def GetLowestCombination():
    BestLength = 999
    BestCombination = [1,2,3,4,5]
    BestCoordinates = [0,0]
    y = 0
    for row in Grid:
        x=0
        for i in row:
            Check = GetValue(x,y)
            if Check[0] == 0 and Check[1] == True:        #if thare is no tile in place
                potentialResult = [1,2,3,4,5]
                compare = GetNeighborsAxis(x,y)

                if 2 in compare:
                    if 4 in potentialResult:
                        potentialResult = RemoveItems(potentialResult,4)
                if 3 in compare:
                    if 4 in potentialResult:
                        potentialResult = RemoveItems(potentialResult,4)
                    if 5 in potentialResult:
                        potentialResult = RemoveItems(potentialResult,5)
                    if 3 in potentialResult:
                        potentialResult.append(3)
                if 4 in compare:
                    if 2 in potentialResult:
                        potentialResult = RemoveItems(potentialResult,2)
                    if 3 in potentialResult:
                        potentialResult = RemoveItems(potentialResult,3)
                if 5 in compare:
                    if 3 in potentialResult:
                        potentialResult = RemoveItems(potentialResult,3)
#                    if 5 in potentialResult:
#                        potentialResult.append(5)
#                        potentialResult.append(5)
#                        potentialResult.append(5)
                
                if len(potentialResult) < BestLength:
                    BestLength = len(potentialResult)
                    BestCombination = potentialResult
                    BestCoordinates = [x,y]
                    
            x+=1
        y+=1
    solution = [BestCombination,BestCoordinates, BestLength]
    return solution

def solve():
    target = GetLowestCombination()
    if not target[2] == 999:
        Grid[target[1][0]][target[1][1]] = random.choice(target[0])
        DrawScreen()
        clock.tick(30)
        solve()

solve()

run = True
while run:
    
    DrawScreen()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                x = pygame.mouse.get_pos()[0] // GridDivider
                y = pygame.mouse.get_pos()[1] // GridDivider
                Grid[x][y] = 1
            elif event.key == pygame.K_2:
                x = pygame.mouse.get_pos()[0] // GridDivider
                y = pygame.mouse.get_pos()[1] // GridDivider
                Grid[x][y] = 2
            elif event.key == pygame.K_3:
                x = pygame.mouse.get_pos()[0] // GridDivider
                y = pygame.mouse.get_pos()[1] // GridDivider
                Grid[x][y] = 3
            elif event.key == pygame.K_4:
                x = pygame.mouse.get_pos()[0] // GridDivider
                y = pygame.mouse.get_pos()[1] // GridDivider
                Grid[x][y] = 4
            elif event.key == pygame.K_5:
                x = pygame.mouse.get_pos()[0] // GridDivider
                y = pygame.mouse.get_pos()[1] // GridDivider
                Grid[x][y] = 5
    clock.tick(30)
pygame.quit()
exit()