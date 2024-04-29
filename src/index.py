import pygame
import random

pygame.init()

# Size the screen
screen = pygame.display.set_mode((288, 512))
clock = pygame.time.Clock()
# It's running the game
running = True
# Assets path
pathGameObjects = '../Flappy-Bird-assets/Game-Objects/'
pathUI = '../Flappy-Bird-assets/UI/'
# Check game start
initGame = False

# Load assets for screen
background = pygame.image.load(f'{pathGameObjects}background-day.png').convert()
base = pygame.image.load(f'{pathGameObjects}base.png').convert()
message = pygame.image.load(f'{pathUI}message.png').convert_alpha()

sprite = [pygame.image.load(f'{pathGameObjects}yellowbird-downflap.png'),
          pygame.image.load(f'{pathGameObjects}yellowbird-midflap.png'),
          pygame.image.load(f'{pathGameObjects}yellowbird-upflap.png')]
obstaculo = pygame.image.load(f'{pathGameObjects}pipe-green.png')

puntuacion = [pygame.image.load(f'{pathUI}Numbers/0.png'),
              pygame.image.load(f'{pathUI}Numbers/1.png'),
              pygame.image.load(f'{pathUI}Numbers/2.png'),
              pygame.image.load(f'{pathUI}Numbers/3.png'),
              pygame.image.load(f'{pathUI}Numbers/4.png'),
              pygame.image.load(f'{pathUI}Numbers/5.png'),
              pygame.image.load(f'{pathUI}Numbers/6.png'),
              pygame.image.load(f'{pathUI}Numbers/7.png'),
              pygame.image.load(f'{pathUI}Numbers/8.png'),
              pygame.image.load(f'{pathUI}Numbers/9.png')
            ]
gameOver = pygame.image.load(f'{pathUI}gameover.png')

bird_rect = sprite[1].get_rect()
pipGreen_rect_1 = obstaculo.get_rect()
pipGreen_rect_2 = obstaculo.get_rect()
pipGreen_rect_3 = obstaculo.get_rect()
pipGreen_rect_4 = obstaculo.get_rect()


count_points = [0,0]


class Bird ():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.gravedad = 0.3
        self.velocity = 0
        self.aumentoGravedad = 0
    
    def jump (self):
        self.y -= 30
        self.gravedad = 0
        self.velocity = 0
        self.aumentoGravedad = 0
        
    
    def update (self):
        self.aumentoGravedad += 0.04
        self.y += (self.gravedad + self.aumentoGravedad)
        # print(self.x, self.y)
        if self.y > 480:
            self.y = 480
            self.gravedad = 0
            self.aumentoGravedad = 0


    def draw (self, screen, sprite, angle):
        if self.aumentoGravedad >= 0 and self.aumentoGravedad <= 1: angle += 40
        else: angle -= 70
        sprite = pygame.transform.rotate(sprite, angle)
        screen.blit(sprite, [self.x, int(self.y)])
    
    def createRect (self, bird):
        bird.x = self.x
        bird.y = self.y+8


class PipeGreen ():
    def __init__(self, x, y) :
        self.x = x
        self.y = y
      
    def update(self, n, e):
        self.x -= 1
        if self.x <= -50: 
            self.x = 300

            if not n % 2 == 0:
                self.y = random.randint(100, 380)
            else:
                self.y = ((e)-320)-70
           
    def draw(self,screen, obstaculo, angle):
        obstaculo = pygame.transform.rotate(obstaculo, angle)
        screen.blit(obstaculo, [int(self.x),  self.y])
    
    def createRect (self, p):
        p.x = self.x
        p.y = self.y



bird = Bird(110, 190)
pipeGreen = PipeGreen(260, random.randint(130, 370))
pipeGreen_2 = PipeGreen(260, ((pipeGreen.y)-320)-65)
pipeGreen_3 = PipeGreen(430, random.randint(130, 370))
pipeGreen_4 = PipeGreen(430, ((pipeGreen_3.y)-320)-65)


paused = False

# Change frame sprites
incrementTile = 0
changeTile = 0
angle = 0
while running:

   
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():

        if event.type == pygame.MOUSEBUTTONDOWN and not paused:
            initGame = True 
            bird.jump()

        if keys[pygame.K_SPACE] and not paused:
            bird.jump()

        if event.type == pygame.QUIT:
            running = False
                
  
    
        # Paint assets in screen
    screen.blit(background, [0,0])
    screen.blit(base, [0, 400])
    
    if not paused:
        if not initGame:
            screen.blit(message, [53, 85])
        else:
            screen.blit(message, [-300, 85])
        
            pipeGreen.update(1, pipeGreen.y)
            pipeGreen_2.update(2, pipeGreen.y)
            pipeGreen_3.update(1, pipeGreen_3.y)
            pipeGreen_4.update(2, pipeGreen_3.y)
            bird.update()
        
            pipeGreen.draw(screen, obstaculo, angle = 0)

            pipeGreen.createRect(pipGreen_rect_1)

            pipeGreen_2.draw(screen, obstaculo, angle = 180)
            pipeGreen_2.createRect(pipGreen_rect_2)

            pipeGreen_3.draw(screen, obstaculo, angle = 0)
            pipeGreen_3.createRect(pipGreen_rect_3)

            pipeGreen_4.draw(screen, obstaculo, angle = 180)
            pipeGreen_4.createRect(pipGreen_rect_4)
            screen.blit(base, [0, 400])
            if bird_rect.colliderect(pipGreen_rect_1) or bird_rect.colliderect(pipGreen_rect_2) or bird_rect.colliderect(pipGreen_rect_3) or bird_rect.colliderect(pipGreen_rect_4) or bird.y >= 410:
                print('Colision')
                paused = True
            elif pipeGreen.x == 90 or pipeGreen_3.x == 90:
                count_points = [count_points[0], count_points[1] + 1 ]
                if count_points[1] == 10:
                    count_points[1] = 0
                    count_points[0] += 1
            
            screen.blit(puntuacion[count_points[0]], [127, 30])
            screen.blit(puntuacion[count_points[1]], [150, 30])

            bird.draw(screen, sprite[changeTile], angle)
        
            bird.createRect(bird_rect)
        
    
        # Controler change frame sprite
        if incrementTile >= 2.8: incrementTile = 0
        else: 
            incrementTile += 0.1
            changeTile = int(round(incrementTile,1))
    else:
       
        pipeGreen.draw(screen, obstaculo, angle = 0)
        pipeGreen_2.draw(screen, obstaculo, angle = 180)
        pipeGreen_2.createRect(pipGreen_rect_2)
        pipeGreen_3.draw(screen, obstaculo, angle = 0)
        pipeGreen_4.draw(screen, obstaculo, angle = 180)
        screen.blit(base, [0, 400])
        bird.draw(screen, sprite[changeTile], angle = 190)
        bird.update()

        screen.blit(puntuacion[count_points[0]], [127, 200])
        screen.blit(puntuacion[count_points[1]], [150, 200])

        screen.blit(gameOver, [50, 80])


    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()