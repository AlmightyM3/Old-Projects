import pygame
import math

# initialize pygame
print("Starting...")
WindowSize = 600
WindowSize2 = WindowSize//2
loadingBarHight = 10
pygame.init()
window = pygame.display.set_mode((WindowSize, WindowSize + loadingBarHight))
clock = pygame.time.Clock()

# Define a 3D point
class Point:
    def __init__(self, x,y,z):
        self.x = x
        self.y = y
        self.z = z

# Define sphere SDF
class Sphere:
    def __init__(self, p, r):
        self.p = p
        self.r = r
    
    def check(self, checkPoint):
        d = DistanceBetweenPoints(checkPoint,self.p)
        return d - self.r

# Define distance between 3D points
def DistanceBetweenPoints(p1,p2):
    x = p1.x-p2.x
    y = p1.y-p2.y
    z = p1.z-p2.z
    return math.sqrt(x*x + y*y + z*z)

# Extremely simplified ray code (Gets a point td distance between two other points, but the point can be past the second point, similar to Lerp)
def PointAlongLine(p1,p2,td):
    d = DistanceBetweenPoints(p1,p2)
    t1 = td/d

    t2 = 1-t1
    x1 = t2*p1.x
    x2 = t1*p2.x
    y1 = t2*p1.y
    y2 = t1*p2.y
    z1 = t2*p1.z
    z2 = t1*p2.z
    
    return Point(x1+x2, y1+y2, z1+z2)

# Gets the lowest distance of all of the objects in the scene
def GetWorldDistance(p):
    d = [objects[j].check(p) for j in range(len(objects))] 
    return min(d)

# Normalizes a point so it still has the same direction, but has a length of one
def Normalize(p):
    d = DistanceBetweenPoints(p,Point(0,0,0))
    return Point(p.x/d,p.y/d,p.z/d)

# Gets the surface normal of a point on an object by sampling points around it 
def GetNormal(p):
    x = GetWorldDistance(Point(p.x + 1, p.y, p.z)) - GetWorldDistance(Point(p.x - 1, p.y, p.z))
    y = GetWorldDistance(Point(p.x, p.y + 1, p.z)) - GetWorldDistance(Point(p.x, p.y - 1, p.z))
    z = GetWorldDistance(Point(p.x, p.y, p.z + 1)) - GetWorldDistance(Point(p.x, p.y, p.z - 1))
    
    return Normalize(Point(x,y,z))

# Gets dot product of 2 points
def DotProduct(p1,p2):
    return p1.x*p2.x + p1.y*p2.y + p1.z*p2.z

# Reflects p1 around p2
def Reflect(p1,p2): # r=2(p1⋅p2)p2 - p1
    r = DotProduct(p1,p2)
    r = Point(r*2*p2.x, r*2*p2.y, r*2*p2.z)
    return Point(r.x-p1.x, r.y-p1.y, r.y-p1.y)

# Define the scene
print("Loading scene...")
objects = [Sphere(Point(0,0,20), 40), Sphere(Point(200,-230,15), 30)]

camera = Point(0,0,-25)

lightDir = Normalize(Point(1,-1,0))

# Draw the scene
def Draw():
    window.fill((25, 25, 25))
    for x in range(WindowSize):
        for y in range(WindowSize):
# Start the actual ray marching for every pixel on screen
            i = 0
            done = False
            CurrentPosition = Point(camera.x + x - WindowSize2,camera.y + y - WindowSize2, 0)
            dist = 1
            while not done:
                d = GetWorldDistance(CurrentPosition)
                
                dist += d
                
                if i > 4:
                    done = True
                i += 1
                
                if d <= 0:
                    done = True
                    
                    normal = GetNormal(CurrentPosition)
                    
                    #window.fill((normal.x*127.5+127.5,normal.y*127.5+127.5,normal.z*127.5+127.5), ((x,y), (1, 1))) # normal visualization
                    
                    DiffuseLight = max(0, DotProduct(normal, lightDir)) # Diffuse lighting
                    
                    DirectionToView = Normalize(Point(camera.x-CurrentPosition.x, camera.y-CurrentPosition.y, camera.z-CurrentPosition.z))
                    ReflectedDirection = Reflect(Point(-lightDir.x, -lightDir.y, -lightDir.z), normal)
                    SpecularLight = max(0, DotProduct(DirectionToView, ReflectedDirection))
                    
                    #window.fill((ReflectedDirection.x*127.5+127.5,ReflectedDirection.y*127.5+127.5,ReflectedDirection.z*127.5+127.5), ((x,y), (1, 1)))
                    window.fill((DiffuseLight*255,DiffuseLight*255,DiffuseLight*255), ((x,y), (1, 1)))
                else:
                    CurrentPosition = PointAlongLine(camera, CurrentPosition, dist)
                
# Create progress bar at the bottom and draw screen
        window.fill((255,255,255), ((x,WindowSize), (1, loadingBarHight))) 
        pygame.display.flip()
    pygame.display.flip()

print("Drawing scene...")
Draw()

print("Done!")
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                Draw()
                
# Camera movement
            if event.key == pygame.K_w:
                camera.y += 20
            elif event.key == pygame.K_s:
                camera.y -= 20
            if event.key == pygame.K_a:
                camera.x += 20
            elif event.key == pygame.K_d:
                camera.x -= 20
            if event.key == pygame.K_e:
                camera.z += 10
            elif event.key == pygame.K_q:
                camera.z -= 10
            
            if event.key == pygame.K_r:
                camera = Point(0,0,-25)
    
    pygame.display.flip()
    clock.tick(30)
print("Exiting")
pygame.quit()
exit()
