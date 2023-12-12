import pygame
import math

# Initialize pygame
WindowSize = 600
pygame.init()
window = pygame.display.set_mode((WindowSize, WindowSize))
clock = pygame.time.Clock()

resolution = 2

# Initialize camera variables
cameraX = 0
cameraY = 0
cameraZ = 0
rotationX = 0
rotationY = 0

# Initialize mesh lists
pointsX = []
pointsY = []
pointsZ = []
triangles = []

projectedX = []
projectedY = []
triX = []
triY = []

# Adds a point (need to figure out a better solution than just multiplying by 200)
def addPoint(x,y,z):
    pointsX.append(x*200)
    pointsY.append(y*200)
    pointsZ.append(z)

# Adds a triangle to the mesh by listing the indexes of the points it makes up
def addTriangle(p1,p2,p3):
    triangles.append(p1)
    triangles.append(p2)
    triangles.append(p3)

# Rotates a point in 3D space around the world origin
def rotatePoint(x,y,z):
    updatedX = x * math.cos(rotationX) - z * math.sin(rotationX)
    updatedY = y
    updatedZ = x * math.sin(rotationX) + z * math.cos(rotationX)
    
    updatedX = updatedX
    updatedY = updatedY * math.cos(rotationY) - updatedZ * math.sin(rotationY)
    updatedZ = updatedY * math.sin(rotationY) + updatedZ * math.cos(rotationY)
    return [updatedX, updatedY, updatedZ]

# Projects a 3D point into 2D space acounting for the camera, adds 0.001 to Z to prevent division by zero
def projectPoint(x,y,z):
    updatedX = x - cameraX
    updatedY = y - cameraY
    updatedZ = z - cameraZ + 0.001
    return [updatedX/updatedZ, updatedY/updatedZ]

# Takes two 2D points in the form [x,y] and returns the distance
def DistanceBetweenPoints(p1,p2):
    x1 = p1[0]-p2[0]
    y1 = p1[1]-p2[1]
    x2 = x1*x1
    y2 = y1*y1
    d = math.sqrt(x2+y2)
    return d

# Takes two 2D points in the form [x,y] and a distance, and returns the point that far along the line
def PointAlongLine(p1, p2, td):
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

def FindSlope(p1, p2):
    y = p2[1] - p1[1]
    x = p2[0] - p1[0]
    if x == 0 or y == 0:
        return 0
    m = y / x
    return m

def findYIntercept(p, m):
    return p[1] - m * p[0]

# Swaps the position of two values in a array
def Swap(Array, pos1, pos2):
    value1 = Array[pos1]
    value2 = Array[pos2]
    Array[pos1] = value2
    Array[pos2] = value1

# Calculates the rotated and protected 2D positions for all the points
def calculatePoints():
    for i in range(len(pointsX)): 
        rotatedPoint = rotatePoint(pointsX[i],pointsY[i],pointsZ[i])
        projectedPoint = projectPoint(rotatedPoint[0],rotatedPoint[1],rotatedPoint[2])
        projectedX.append(projectedPoint[0])
        projectedY.append(projectedPoint[1])

# Draws a dot on all protected points (realize on the amount of x values and y values being the same witch should always be the case but will cause errors otherwise)
def drawPoints():
    for i in range(len(projectedX)):
        pygame.draw.circle(window, (255,0,0), (projectedX[i]+WindowSize/2,projectedY[i]+WindowSize/2), 5)

# Draws all the edges based off of indexs in the triangle list
def drawEdges():
    for i in range(0,len(triangles),3):
        pygame.draw.line(window, (255,255,255), (projectedX[triangles[i]]+WindowSize/2,projectedY[triangles[i]]+WindowSize/2), (projectedX[triangles[i+1]]+WindowSize/2,projectedY[triangles[i+1]]+WindowSize/2), 3)
        pygame.draw.line(window, (255,255,255), (projectedX[triangles[i+1]]+WindowSize/2,projectedY[triangles[i+1]]+WindowSize/2), (projectedX[triangles[i+2]]+WindowSize/2,projectedY[triangles[i+2]]+WindowSize/2), 3)
        pygame.draw.line(window, (255,255,255), (projectedX[triangles[i+2]]+WindowSize/2,projectedY[triangles[i+2]]+WindowSize/2), (projectedX[triangles[i]]+WindowSize/2,projectedY[triangles[i]]+WindowSize/2), 3)

def fillSingleTri():
    if triY[1] < triY[0]:
        Swap(triY, 0, 1)
        Swap(triX, 0, 1)
    if triY[2] < triY[0]:
        Swap(triY, 0, 2)
        Swap(triX, 0, 2)
    if triY[2] < triY[1]:
        Swap(triY, 1, 2)
        Swap(triX, 1, 2)
    
    m1 = FindSlope([triX[0], triY[0]],[triX[1], triY[1]])
    b1 = findYIntercept([triX[0], triY[0]], m1)
    m2 = FindSlope([triX[2], triY[2]],[triX[1], triY[1]])
    b2 = findYIntercept([triX[2], triY[2]], m2)
    m3 = FindSlope([triX[2], triY[2]],[triX[0], triY[0]])
    b3 = findYIntercept([triX[2], triY[2]], m3)
    
    for y in range(round(triY[0]),round(triY[2]),resolution):
#        if y < triY[1]:
#            if m3 == 0:
#                x1 = WindowSize/2
#            else:
#                x1 = (y-b3)/m3
#            if m1 == 0:
#                x2 = WindowSize/2
#            else:
#                x2 = (y-b1)/m1
#            if not x1 <  0 and not x1 >  WindowSize:
#                pygame.draw.line(window, (0,0,255), (x1, y), (x2, y), resolution)
#            else:
#                print('triY[0]' + str(triY[0]))
#                print('triY[1]' + str(triY[1]))
#                print('triY[2]' + str(triY[2]))
#                print('y=' + str(y))
#                print('x1=' + str(x1))
#                print('x2=' + str(x2))
#                print('b2=' + str(b2))
#                print('b3=' + str(b3))
#                print('m1=' + str(m1))
#                print('m3=' + str(m3))
#                quit()
        if y < triY[1]:
            if m3 == 0:
                x1 = triX[2]
            else:
                x1 = (y-b3)/m3
            if m1 == 0:
                x2 = triX[0]
            else:
                x2 = (y-b1)/m1
            if not x1 <  0 and not x1 >  WindowSize:
                pygame.draw.line(window, (0,0,255), (x1, y), (x2, y), resolution)
    
#        elif y > triY[1]:
#            if m3 == 0:
#                x1 = WindowSize/2
#            else:
#                x1 = (y-b3)/m3
#            if m2 == 0:
#                x2 = WindowSize/2
#            else:
#                x2 = (y-b2)/m2
#            if not x1 <  0 and not x1 >  WindowSize:
#                pygame.draw.line(window, (0,0,255), (x1, y), (x2, y), resolution)
#            else:
#                print('y=' + str(y))
#                print('x1=' + str(x1))
#                print('x2=' + str(x2))
#                print('b2=' + str(b2))
#                print('b3=' + str(b3))
#                print('m2=' + str(m2))
#                print('m3=' + str(m3))
#                quit()
        if y > triY[1]:
            if m3 == 0:
                x1 = triX[0]
            else:
                x1 = (y-b3)/m3
            if m2 == 0:
                x2 = triX[2]
            else:
                x2 = (y-b1)/m2
            if not x1 <  0 and not x1 >  WindowSize:
                pygame.draw.line(window, (0,0,255), (x1, y), (x2, y), resolution)
        #else:
        #    x1 = (y-b3)/m3
        #    x2 = triX[1]
        #    pygame.draw.line(window, (0,0,255), (x1, y), (x2, y), 1)

def fillTriangles():
    global triX
    global triY
    
    for i in range(0,len(triangles),3):
        triX = []
        triY = []
        
        triX.append(projectedX[triangles[i]]+WindowSize/2)
        triY.append(projectedY[triangles[i]]+WindowSize/2)
        triX.append(projectedX[triangles[i+1]]+WindowSize/2)
        triY.append(projectedY[triangles[i+1]]+WindowSize/2)
        triX.append(projectedX[triangles[i+2]]+WindowSize/2)
        triY.append(projectedY[triangles[i+2]]+WindowSize/2)
        
        if 1 == 1: #Add logic to determine if the triangle should be drawn using back-face culling here.
            fillSingleTri()

# Resets all values and draws the new mesh to the screen
def reset():
    global cameraX
    global cameraY
    global cameraZ
    global rotationX
    global rotationY
    
    global pointsX
    global pointsY
    global pointsZ
    global triangles
    
    cameraX = 0
    cameraY = 0
    cameraZ = 0
    rotationX = 0
    rotationY = 0

    pointsX = []
    pointsY = []
    pointsZ = []
    triangles = []
    
    addPoint(-1,-1,4)
    addPoint(1,-1,4)
    addPoint(-1,1,4)
    addPoint(1,1,4)
    addPoint(-1,-1,6)
    addPoint(1,-1,6)
    addPoint(-1,1,6)
    addPoint(1,1,6)
    addTriangle(0,1,2)
    addTriangle(1,3,2)
    addTriangle(2,6,3)
    addTriangle(6,3,7)
    addTriangle(0,1,4)
    addTriangle(1,4,5)
    addTriangle(0,4,2)
    addTriangle(4,2,6)
    addTriangle(1,3,5)
    addTriangle(5,3,7)
    addTriangle(4,5,6)
    addTriangle(5,7,6)

    window.fill((0,0,0))
    pygame.display.flip()
    projectedX = []
    projectedY = []
    calculatePoints()
    fillTriangles()
    drawEdges()
    drawPoints()

    pygame.display.flip()

reset()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            # Camera rotation, controlled by arrow keys
            if event.key == pygame.K_UP:
                rotationY += 0.005
            elif event.key == pygame.K_DOWN:
                rotationY -= 0.005
            if event.key == pygame.K_RIGHT:
                rotationX += 0.005
            elif event.key == pygame.K_LEFT:
                rotationX -= 0.005
            
            # Camera movement controlled by WASDQE
            if event.key == pygame.K_w:
                cameraY += 20
            elif event.key == pygame.K_s:
                cameraY -= 20
            if event.key == pygame.K_a:
                cameraX += 20
            elif event.key == pygame.K_d:
                cameraX -= 20
            if event.key == pygame.K_e:
                cameraZ += 2
            elif event.key == pygame.K_q:
                cameraZ -= 2
            
            # Resets all when R is pressed
            if event.key == pygame.K_r:
                reset()
    
    # Draws the current frame to the screen
    window.fill((0,0,0))
    projectedX = []
    projectedY = []
    calculatePoints()
    fillTriangles()
    drawEdges()
    drawPoints()
    
    clock.tick(30)
    pygame.display.flip()
pygame.quit()
exit()