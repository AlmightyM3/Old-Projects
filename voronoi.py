import pygame
import math
import random

WindowSize = 600
pygame.init()
window = pygame.display.set_mode((WindowSize, WindowSize))
clock = pygame.time.Clock()

class Point:
    def __init__(self, x,y):
        self.x = x
        self.y = y
    
        self.color = (round(random.random()*150 + 75),round(random.random()*150 + 75),round(random.random()*200 + 25))

p = [Point(round(random.random()*WindowSize + 1),round(random.random()*WindowSize + 1)) for i in range(12)]

def DistanceBetweenPoints(p1,p2):
    x1 = p1[0]-p2[0]
    y1 = p1[1]-p2[1]
    return math.sqrt(x1*x1+y1*y1)

def Draw():
    window.fill((0, 0, 0))
    for x in range(WindowSize):
        for y in range(WindowSize):
            ClosestDistance = WindowSize + 1
            ClosestPoint = 0
            for i in range(len(p)):
                Distance = DistanceBetweenPoints([x,y], [p[i].x,p[i].y])
                if Distance < ClosestDistance:
                    ClosestDistance = Distance
                    ClosestPoint = i
            window.fill(p[ClosestPoint].color, ((x,y), (1, 1)))
        pygame.display.flip()
    for i in range(len(p)):
        window.fill((225,225,225), ((p[i].x,p[i].y), (6, 6)))
    pygame.display.flip()

Draw()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False    

    if pygame.mouse.get_pressed()[0]:
        x = pygame.mouse.get_pos()[0]
        y = pygame.mouse.get_pos()[1]
        p.append(Point(x,y))
    if pygame.mouse.get_pressed()[2]:
        Draw()
        
    pygame.display.flip()
    clock.tick(30)
pygame.quit()
exit()
