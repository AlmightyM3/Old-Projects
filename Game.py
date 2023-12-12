import pygame
import math
import random

WindowSize = 600
pygame.init()
window = pygame.display.set_mode((WindowSize, WindowSize))
clock = pygame.time.Clock()

class point:
    def __init__(self, x,y):
        self.x = x
        self.y = y

class Player:
    velocity = point(0,0)
    def __init__(self, p1, s, color):
        self.p1 = p1
        self.color = color
        self.p2 = point(p1.x + s.x, p1.y + s.y)
        self.s = s
    def updatePlayer(self):
        self.p2 = point(self.p1.x + self.s.x, self.p1.y + self.s.y)

class Platform:
    def __init__(self, p1, p2, color):
        self.p1 = p1
        self.color = color
        self.p2 = p2
        self.s = point(p2.x-p1.x, p2.y-p1.y)
        
    def rectOverlap(self):
        if self.p1.x > player.p2.x or player.p1.x > self.p2.x:
            return False
        if self.p1.y > player.p2.y or player.p1.y > self.p2.y:
            return False
        
        return True

player = Player(point(50,50), point(48,64), (0,0,225))

Platforms = [Platform(point(350,300), point(450, 550), (0,122,122)), Platform(point(150,500), point(450, 550), (0,225,0))]

def Draw():
    window.fill((0, 0, 0))
    
    for i in range(len(Platforms)):
        pygame.draw.rect(window, Platforms[i].color, pygame.Rect(Platforms[i].p1.x, Platforms[i].p1.y, 
                                                                 Platforms[i].s.x, Platforms[i].s.y))
    pygame.draw.rect(window, player.color, pygame.Rect(player.p1.x, player.p1.y, player.s.x, player.s.y))
    
    pygame.display.flip()

def CheckColl():
    coll = False
    
    player.updatePlayer()

    Horizontal = False
    Vertical = False
    
    for i in range(len(Platforms)):
        test = Platforms[i].rectOverlap()
        if test or player.p1.y > WindowSize - player.s.y:
            coll = True
            
            if test:
                if Platforms[i].p1.x < player.p2.x or player.p1.x < Platforms[i].p2.x:
                    Horizontal = True
                if Platforms[i].p1.y < player.p2.y or player.p1.y < Platforms[i].p2.y:
                    Vertical = True
            else:
                Vertical = True
            
    return coll, Horizontal, Vertical

run = True
while run:
    coll, collHorizontal, collVertical = CheckColl()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player.velocity.x += 5
            if event.key == pygame.K_LEFT:
                player.velocity.x -= 5
            
            if event.key == pygame.K_SPACE:
                if collVertical:
                    player.velocity.y = -15
                    
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                player.velocity.x -= 5
            if event.key == pygame.K_LEFT:
                player.velocity.x += 5
    
    player.p1.x += player.velocity.x
    
    if not collVertical:
        player.velocity.y += 1
        
    player.p1.y += player.velocity.y
    
    if collVertical and player.velocity.y > 0:
        player.velocity.y = 0
        
        player.p1.y -= 1
        while CheckColl()[1]:
            player.p1.y -= 1
        player.p1.y += 1
    
    if collHorizontal:
        player.p1.y -= 1
        while CheckColl()[2]:
            player.p1.x -= player.velocity.x
            if player.velocity.x == 0:
                break 
        player.p1.y += 1

    Draw()
    
    clock.tick(30)
pygame.quit()
exit()