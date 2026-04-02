import pygame
import sys
import random
import time


pygame.init()
#-------------------------Game Variables And Constants-------------------
GAME_WIDTH = 500
GAME_HEIGHT = 500


PLAYER_X = 20
PLAYER_Y = 200
PLAYER_VELOCITY_Y = 5
BALL_VELOCITY_X = 5
BALL_VELOCITY_Y = 5
PLAYER_HEIGHT =  60
PLAYER_WIDTH = 5

BOT_X = 480

MAX_BOUNCE_SPEED = 8
BACKGROUND_COLOR = '#f6fd91'
running = True
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption('PyPong')
clock = pygame.time.Clock()


class Player(pygame.Rect):
    def __init__(self, ):
        pygame.Rect.__init__(self, PLAYER_X , PLAYER_Y ,PLAYER_WIDTH , PLAYER_HEIGHT)
        self.color = '#0c05d1'
        self.velocity_y = PLAYER_VELOCITY_Y
        self.direction = 'down'

class Bot(pygame.Rect):
    def __init__(self,):
        pygame.Rect.__init__(self , BOT_X , PLAYER_Y , PLAYER_WIDTH , PLAYER_HEIGHT)
        self.color = '#0c05d1'
        self.velocity_y = PLAYER_VELOCITY_Y
        self.direction = 'down'
        

class Ball:
    def __init__(self):
        self.x = GAME_WIDTH//2
        self.y = GAME_HEIGHT//2
        self.radius = 10
        self.color = '#92fc82'
        self.velocity_x = 5
        self.velocity_y = 7
        self.directions = ['up', 'down']
        self.direction = random.choice(self.directions)

        
def draw():
    window.fill(BACKGROUND_COLOR)
    pygame.draw.rect(window , player.color , player)
    pygame.draw.rect(window , bot.color , bot)
    pygame.draw.circle(window , ball.color , (ball.x , ball.y), ball.radius ,)


def check_collision():
    #border-Collision
    if player.y <=0:
          player.y = 0
    
    elif (player.y +player.height)>=  GAME_HEIGHT:
            player.y = GAME_HEIGHT - player.height
    

    #Ball Collison
    
    
    #Checks Ball Collision with Borders
    # if ball.x +ball.radius<= 0:
    #     ball.velocity_x *=-1
    
    elif ball.x +ball.radius >= GAME_WIDTH:
        ball.velocity_x *=-1

    if ball.y +ball.radius <= 0:
        ball.velocity_y *= -1
    elif ball.y + ball.radius >= GAME_HEIGHT:
        ball.velocity_y *= -1



    # #Checks Ball Collsion with Rectangles
    # closest_x_right = ball.x - ball.radius
    # # closest_y_right = ball.y - ball.radius
    # # if closest_x_right <= (player.x +player.width)  :
    # #     ball.velocity_x*= -1
    # #     ball.velocity_y *= -1

    # if closest_x_right <= (player.x + player.width):
    #     center_y = ball.y + ball.radius //2
    #     player_center = player.height //2

    #     ball.velocity_y  = (center_y - player_center) *-1.5
    #     ball.velocity_x *= -1.05
    # closest_x_left = ball.x + ball.radius

    closest_x_right = ball.x - ball.radius
    if closest_x_right <= (player.x + player.width) and ball.y <= player.y + player.height:
        player_center = player.y + (player.height//2)
        distance = ball.y - player_center
        bounce_factor = distance / (player.height //2)
        ball.velocity_y = bounce_factor * MAX_BOUNCE_SPEED
        ball.velocity_x  *= -1

    
 
    
    
def move():
    #PLAYER MOVEMENT
    # if player.direction == 'down':
    #     player.y += player.velocity_y
        
      
    # elif player.direction == 'up':
    #     player.y += -player.velocity_y

    #BALL MOVEMENT
    ball.y += ball.velocity_y
    ball.x += ball.velocity_x
    
player = Player()
ball = Ball()
bot = Bot()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player.direction =  'up'
        player.y += -player.velocity_y
    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player.direction =  'down'
        player.y += player.velocity_y

    pygame.display.update()
    check_collision()
    move()
    draw()
  
    clock.tick(30)


