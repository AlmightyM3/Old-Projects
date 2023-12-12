import pygame
import math

WindowSize = 600
pygame.init()
window = pygame.display.set_mode((WindowSize, WindowSize))
clock = pygame.time.Clock()
GridDivider = 50
GridCount = WindowSize//GridDivider

TrueX = 300
TrueY = 400

def DrawGrid():
    for x in range(GridCount):
        pygame.draw.line(window, (255, 255, 255), (x*GridDivider,0), (x*GridDivider,WindowSize))
        pygame.display.flip()
    for y in range(GridCount):
        pygame.draw.line(window, (255, 255, 255), (0,y*GridDivider), (WindowSize,y*GridDivider))
        pygame.display.flip()
    pygame.draw.circle(window, (255,255,255), (TrueX,TrueY), 8)
    pygame.display.flip()

def DrawQuad(a,h,k):
    a2 = a / GridDivider
    h2 = h * GridDivider
    k2 = k * GridDivider 
    OldPoint1 = [TrueX+h2,TrueY+k2]
    OldPoint2 = [TrueX+h2,TrueY+k2]
    for i in range(400):
        x = i/2
        
        x2 = x*x
        y = a2*x2

        NewPoint1 = [x+TrueX,0-y+TrueY]
        NewPoint2 = [0-x+TrueX,0-y+TrueY]
        NewPoint1 = [NewPoint1[0]+h2,NewPoint1[1]+k2]
        NewPoint2 = [NewPoint2[0]+h2,NewPoint2[1]+k2]
        
        pygame.draw.line(window, (255,255,255), (OldPoint1[0],OldPoint1[1]), (NewPoint1[0],NewPoint1[1]), 5)
        OldPoint1 = NewPoint1
        
        pygame.draw.line(window, (255,255,255), (OldPoint2[0],OldPoint2[1]), (NewPoint2[0],NewPoint2[1]), 5)
        OldPoint2 = NewPoint2

    pygame.display.flip()

def findA(VertexX, VertexY, PointX, PointY):
    p1 = PointX - VertexX
    p2 = p1 * p1
    p3 = PointY - VertexY
    a = p3 / p2
    return a

DrawGrid() 

inputVertexX = input("What should the vertex x be?")
inputVertexY = input("What should the vertex y be?")
inputPointX = input("What should the second point x be?")
inputPointY = input("What should the second point y be?")
trueA = findA(int(inputVertexX),int(inputVertexY),int(inputPointX), int(inputPointY))

print("")
print("The a value is: "+str(trueA))
print("Your equation is y="+str(trueA)+"(X-("+inputVertexX+"))^2+("+inputVertexY+")")
if trueA < 0:
    print("The parabola is fliped.")
else:
    print("The parabola is not fliped.")
if abs(trueA) < 1:
    print("The parabola has been compressed by "+str(abs(trueA)))
elif abs(trueA) > 1:
    print("The parabola has been streched by "+str(abs(trueA)))
if int(inputVertexX) > 0:
    print("The parabola has been transformed horizontally right by "+str(abs(int(inputVertexX))))
elif int(inputVertexX) < 0:
    print("The parabola has been transformed horizontally left by "+str(abs(int(inputVertexX))))
if int(inputVertexY) > 0:
    print("The parabola has been transformed vertically up by "+str(abs(int(inputVertexY))))
elif int(inputVertexY) < 0:
    print("The parabola has been transformed vertically down by "+str(abs(int(inputVertexY))))

DrawQuad(float(trueA),int(inputVertexX),0-int(inputVertexY))

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    clock.tick(30)
    pygame.display.flip()
pygame.quit()
exit()