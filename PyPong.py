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

MOVE_BOT = pygame.USEREVENT +1
MAX_BOUNCE_SPEED = 8
BACKGROUND_COLOR = '#f6fd91'
running = True
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption('PyPong')
clock = pygame.time.Clock()

pygame.time.set_timer(MOVE_BOT , 1000)
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
        self.velocity_y = 8
      
        

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
    #border-Collision with Padldles
    if player.y <=0:
          player.y = 0
    
    elif (player.y +player.height)>=  GAME_HEIGHT:
            player.y = GAME_HEIGHT - player.height
    if bot.y <=0:
        bot.y = 0
    elif (bot.y + player.height)>= GAME_HEIGHT:
        bot.y = GAME_HEIGHT - bot.height
    
    

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

    topBall = ball.y - ball.radius
    bottomBall = ball.y + ball.radius
    closest_x_right = ball.x - ball.radius
    
    if (bottomBall >= player.y) and (topBall <= player.y + player.height) and (closest_x_right <= player.x + player.width):
        player_center = player.y + (player.height//2)
        distance = ball.y - player_center
        bounce_factor = distance / (player.height //2)
        ball.velocity_y = bounce_factor * MAX_BOUNCE_SPEED
        ball.velocity_x  *= -1

    if (bottomBall >= bot.y) and (topBall <= bot.y + bot.height) and (closest_x_right<= bot.x + player.width):
        player_center = player.y + (player.height//2)
        distance = ball.y - player_center
        bounce_factor = distance / (player.height //2)
        ball.velocity_y = bounce_factor * MAX_BOUNCE_SPEED
        ball.velocity_x  *= -1

    
 
    
    
def move():
    ball.y += ball.velocity_y
    ball.x += ball.velocity_x

def botMovement():
    if ball.y > bot.y and ball.velocity_x>0:
        bot.y += bot.velocity_y
    elif ball.y < bot.y and ball.velocity_x >0:
        bot.y += -bot.velocity_y


player = Player()
ball = Ball()
bot = Bot()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
        if event.type == MOVE_BOT:
            botMovement()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player.direction =  'up'
        player.y += -player.velocity_y
    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player.direction =  'down'
        player.y += player.velocity_y

    print(f'ball y {ball.y}')

    # print(last_time_active)
    pygame.display.update()
    check_collision()

    move()
    draw()
  
    clock.tick(30)


