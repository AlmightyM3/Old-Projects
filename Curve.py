import pygame
import math
import random

WindowSize = 600
pygame.init()
window = pygame.display.set_mode((WindowSize, WindowSize))
clock = pygame.time.Clock()

point1 = [round(random.random()*WindowSize + 1),round(random.random()*WindowSize + 1)]
point2 = [round(random.random()*WindowSize + 1),round(random.random()*WindowSize + 1)]
point3 = [round(random.random()*WindowSize + 1),round(random.random()*WindowSize + 1)]
point4 = [round(random.random()*WindowSize + 1),round(random.random()*WindowSize + 1)]

def initialize():
    window.fill((0,0,0))
    pygame.draw.circle(window, (135,0,135), (point1[0],point1[1]), 10)
    pygame.draw.circle(window, (135,0,135), (point2[0],point2[1]), 10)
    pygame.draw.circle(window, (135,0,135), (point3[0],point3[1]), 10)
    pygame.draw.circle(window, (135,0,135), (point4[0],point4[1]), 10)

    pygame.draw.line(window, (255, 255, 255), (point1[0],point1[1]), (point2[0],point2[1]))
    pygame.draw.line(window, (255, 255, 255), (point2[0],point2[1]), (point3[0],point3[1]))
    pygame.draw.line(window, (255, 255, 255), (point3[0],point3[1]), (point4[0],point4[1]))

def DistanceBetweenPoints(p1,p2):
    x1 = p1[0]-p2[0]
    y1 = p1[1]-p2[1]
    x2 = x1*x1
    y2 = y1*y1
    d = math.sqrt(x2+y2)
    return d

def PointAlongLine(p1,p2,td):
    d = DistanceBetweenPoints(p1,p2)
    t1 = td/d

    t2 = 1-t1
    x1 = t2*p1[0]
    x2 = t1*p2[0]
    y1 = t2*p1[1]
    y2 = t1*p2[1]

    dx = x1+x2
    dy = y1+y2
    point = [dx,dy]
    
    return point

def PercentagePointAlongLine(p1,p2,tp):
    d1 = tp/100
    d2 = DistanceBetweenPoints(p1,p2)*d1
    point = PointAlongLine(p1,p2,d2)
    return point

def DrawCurve():
    LineColor = (round(random.random()*255),round(random.random()*255),round(random.random()*255))
    OldPoint = point1
    for i in range(100):
        p1 = PercentagePointAlongLine(point1, point2, i)
        p2 = PercentagePointAlongLine(point2, point3, i)
        p3 = PercentagePointAlongLine(point3, point4, i)
        p4 = PercentagePointAlongLine(p1, p2, i)
        p5 = PercentagePointAlongLine(p2, p3, i)
        p6 = PercentagePointAlongLine(p4, p5, i)

        pygame.draw.line(window, LineColor, (OldPoint[0],OldPoint[1]), (p6[0],p6[1]), 5)
        OldPoint = p6
        #pygame.draw.circle(window, (135,255,0), (p6[0],p6[1]), 5)
        clock.tick(30)
        pygame.display.flip()
    pygame.draw.line(window, LineColor, (OldPoint[0],OldPoint[1]), (point4[0],point4[1]), 5)

initialize()
run = True
while run:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                DrawCurve()
            elif event.key == pygame.K_1:
                point1 = pygame.mouse.get_pos()
                initialize()
            elif event.key == pygame.K_2:
                point2 = pygame.mouse.get_pos()
                initialize()
            elif event.key == pygame.K_3:
                point3 = pygame.mouse.get_pos()
                initialize()
            elif event.key == pygame.K_4:
                point4 = pygame.mouse.get_pos()
                initialize()
            elif event.key == pygame.K_r:
                point1 = [round(random.random()*WindowSize + 1),round(random.random()*WindowSize + 1)]
                point2 = [round(random.random()*WindowSize + 1),round(random.random()*WindowSize + 1)]
                point3 = [round(random.random()*WindowSize + 1),round(random.random()*WindowSize + 1)]
                point4 = [round(random.random()*WindowSize + 1),round(random.random()*WindowSize + 1)]

                
    clock.tick(30)
    pygame.display.flip()
pygame.quit()
exit()