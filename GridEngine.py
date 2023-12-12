import pygame
import random

WindowSize = 600
pygame.init()
window = pygame.display.set_mode((WindowSize, WindowSize))
clock = pygame.time.Clock()

GridDivider = 60
GridCount = WindowSize//GridDivider

TestImage = pygame.image.load('test.png')
Size = (GridDivider,GridDivider)
ScaledTestImage = pygame.transform.scale(TestImage, Size)

Grid = [[0 for i in range(GridCount)] for j in range(GridCount)]

def GetValue(x,y):
    try: 
        value = Grid[x][y]
    except:
        value = 0
    return value

def GetNeighborsDiagonal(x,y):
    N  = GetValue(x,y-1)
    NE = GetValue(x+1,y-1)
    E  = GetValue(x+1,y)
    SE = GetValue(x+1,y+1)
    S  = GetValue(x,y+1)
    SW = GetValue(x-1,y+1)
    W  = GetValue(x-1,y)
    NW = GetValue(x-1,y-1)
    
    neighbors = [N,NE,E,SE,S,SW,W,NW]
    return neighbors
def GetNeighborsAxis(x,y):
    N  = GetValue(x,y-1)
    E  = GetValue(x+1,y)
    S  = GetValue(x,y+1)
    W  = GetValue(x-1,y)
    
    neighbors = [N,E,S,W]
    return neighbors

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
                pygame.draw.rect(window, (255, 0, 0), pygame.Rect(y*GridDivider, x*GridDivider, GridDivider, GridDivider))
            elif i == 2:
                pygame.draw.rect(window, (0, 255, 0), pygame.Rect(y*GridDivider, x*GridDivider, GridDivider, GridDivider))
            elif i == 3:
                pygame.draw.rect(window, (0, 0, 255), pygame.Rect(y*GridDivider, x*GridDivider, GridDivider, GridDivider))
            elif i == 4:
                window.blit(ScaledTestImage, (y*GridDivider, x*GridDivider))
            x+=1
        y+=1
    
    DrawGrid()
    pygame.display.update()
    
DrawGrid()

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
            
    clock.tick(30)
pygame.quit()
exit()