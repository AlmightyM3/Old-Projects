import pygame
import math

# Initialize pygame
WindowSize = 600
pygame.init()
window = pygame.display.set_mode((WindowSize, WindowSize))
clock = pygame.time.Clock()

point1 = [-100+WindowSize/2,100+WindowSize/2]
point2 = [0+WindowSize/2,WindowSize/2]

distince = 0

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

run = True
while run:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                distince += 10
            elif event.key == pygame.K_DOWN:
                distince -= 10
    
    window.fill((0,0,0))
    
    point3 = PointAlongLine(point1,point2,distince)
    
    pygame.draw.circle(window, (255,0,0), (point1[0],point1[1]), 10)
    pygame.draw.circle(window, (255,0,0), (point2[0],point2[1]), 10)
    pygame.draw.circle(window, (0,255,0), (point3[0],point3[1]), 6)
    
    clock.tick(30)
    pygame.display.flip()
pygame.quit()
exit()