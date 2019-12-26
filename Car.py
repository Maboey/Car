import pygame
import math
import random
#region variables
screenWidth = 1100
screenHeight = 618
HW = screenWidth//2
HH = screenHeight//2
displaySurface = pygame.display.set_mode((screenWidth,screenHeight))
pygame.display.set_caption("Intelligent Car")
clock = pygame.time.Clock()
run = True
fps = 50
red = [255,0,0]
green = [40,150,40]
blue = [0,0,255]
white = [255,255,255]
black = [0,0,0]
backgroundSprite = pygame.image.load('Sprite/background.png')
backgroundSprite = pygame.transform.scale(backgroundSprite, (1100, 618))
backgroundMask = pygame.mask.from_surface(backgroundSprite)
backgroundRect = backgroundSprite.get_rect()
circuitSprite = pygame.image.load('Sprite/circuit.png')
circuitSprite = pygame.transform.scale(circuitSprite, (1100, 618))
carSprite = pygame.image.load('Sprite/car.png')
carSprite = pygame.transform.scale(carSprite, (55, 35))
collision = False
defaultX = 780
defaultY = 80
path = []
actions = [0,1,2,3,4,5]
action = actions[0]
Counterpath = 0
CounterpathDivisor = 0
#endregion
class car (object):
    def __init__(self):
        self.x = defaultX
        self.y = defaultY
        self.angle = 180
        self.speed = 0
        self.acceleration = 1
        self.maxSpeed = 5
        self.AngleTurnStrenght = 1
        self.width = 55
        self.height = 35
    def draw(self):

        self.x += math.cos(math.radians(-self.angle)) * self.speed
        self.y += math.sin(math.radians(-self.angle)) * self.speed
    
        if self.x < 0:
            self.x=0
        if self.y < 0:
            self.y=0
        if self.x > screenWidth - self.width:
            self.x = screenWidth - self.width
        if self.y > screenHeight - self.height:
            self.y = screenHeight - self.height

        displaySurface.blit((pygame.transform.rotate(carSprite, self.angle)), (self.x, self.y))       
def redrawGameWindow():
    displaySurface.blit(backgroundSprite, (0,0))
    displaySurface.blit(circuitSprite, (0,0))
    car.draw()
    if collision:
        pygame.draw.circle(displaySurface, red, (round(car.x),round(car.y)), 10,)
    pygame.display.update()
car = car()
ox = HW - backgroundRect.center[0]
oy = HH - backgroundRect.center[1]
while run:
    try:
        action = path[Counterpath]
    except:
        action = random.randrange(0,5)
    for event in pygame.event.get():
                 if event.type == pygame.QUIT:
                    run = False
    carMask = pygame.mask.from_surface(carSprite)
    mx = car.x
    my = car.y
    offset = (round(mx - ox),round(my - oy))
    if backgroundMask.overlap(carMask,offset):
        collision = True
    else:
        collision = False
    if action == 1 or action == 2 or action == 3: # go forward
        if car.speed <= car.maxSpeed:
            car.speed += car.acceleration
    else: # slow down if not forward
        if car.speed > 0:
            car.speed -= car.acceleration
        if car.speed < 0:
            car.speed += car.acceleration
    if action == 2 or action == 4: # turn right
        car.angle += car.AngleTurnStrenght 
    if action == 3 or action == 5: # turn left
        car.angle -= car.AngleTurnStrenght   
    if collision:
        CounterpathDivisor = 0
        Counterpath = 0
        car.x = defaultX
        car.y = defaultY
        car.speed = 0
        car.angle = 180
        path = path[:-3]
    elif Counterpath>len(path):
        path.append(action)
        print(path)
    if CounterpathDivisor < 3:
        CounterpathDivisor += 1
    else:
        Counterpath += 1
        CounterpathDivisor = 0
    redrawGameWindow()
    clock.tick(400)
pygame.quit()