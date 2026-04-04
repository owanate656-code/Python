import pygame
import sys
import random

pygame.init()
#-------------------------Game Variables And Constants-------------------
GAME_WIDTH = 500
GAME_HEIGHT = 500


PLAYER_X = 20
PLAYER_Y = 200
PLAYER_VELOCITY_Y = 5

PLAYER_HEIGHT =  60
PLAYER_WIDTH = 5

BOT_HEIGHT =  60
BOT_WIDTH = 5

BOT_X = 480
BOT_Y = PLAYER_VELOCITY_Y

MAX_BOUNCE_SPEED = 8
MINIMUM_BOUNCE_SPEED = 3
BACKGROUND_COLOR = '#f6fd91'
running = True
gameover = False
botWinState = False
playerWinState = False
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption('PyPong')
clock = pygame.time.Clock()

pygame.font.init()
consolas = pygame.font.SysFont('Consolas' , 20)

class Player(pygame.Rect):
    def __init__(self, ):
        pygame.Rect.__init__(self, PLAYER_X , PLAYER_Y ,PLAYER_WIDTH , PLAYER_HEIGHT)
        self.color = '#0c05d1'
        self.velocity_y = PLAYER_VELOCITY_Y
        self.direction = 'down'
        self.score = 0

class Bot(pygame.Rect):
    def __init__(self,):
        pygame.Rect.__init__(self , BOT_X , PLAYER_Y , BOT_WIDTH , BOT_HEIGHT)
        self.color = '#0c05d1'
        self.velocity_y = 8
        self.score = 0
        

class Ball:
    def __init__(self):
        self.x = GAME_WIDTH//2
        self.y = GAME_HEIGHT//2
        self.radius = 10
        self.color = '#92fc82'
        self.possible_velocity = [2,  -2, -2,3,3 ]
        self.velocity_x = random.choice(self.possible_velocity)
        self.velocity_y = random.choice(self.possible_velocity)
    

        
def draw():
    global playerWinState
    window.fill(BACKGROUND_COLOR)
    pygame.draw.rect(window , player.color , player)
    pygame.draw.rect(window , bot.color , bot)
    pygame.draw.circle(window , ball.color , (ball.x , ball.y), ball.radius ,)
    playerScoreText = consolas.render(str(player.score ), True , 'black')
    window.blit(playerScoreText , (20  , 20))

    botScoreText = consolas.render(str(bot.score) , True , 'black')
    window.blit(botScoreText , (480 , 480))

    if playerWinState:
        playerWinsText = consolas.render( 'Player Wins', True , 'black')
        window.blit(playerWinsText , (150, 230))
        instructionText = consolas.render('Press Enter To Restart or Baskspace to Close',True , 'black' )
        window.blit(instructionText , (10, 250))
    if botWinState:
        botWinsText = consolas.render( 'Bot Wins', True , 'black')
        window.blit(botWinsText , (150, 230))
        instructionText = consolas.render('Press Enter To Restart or Baskspace to Close',True , 'black' )
        window.blit(instructionText , (10, 250))



def check_collision():
    global botWinState , playerWinState
    #border-Collision with Padldles
    if player.y <=0:
          player.y = 0
    
    elif (player.y +player.height)>=  GAME_HEIGHT:
            player.y = GAME_HEIGHT - player.height
    if bot.y <=0:
        bot.y = 0
    elif (bot.y + bot.height)>= GAME_HEIGHT:
        bot.y = GAME_HEIGHT - bot.height
    
    

    #Ball Collison
    
    
    #Checks Ball Collision with Borders
    if ball.x -ball.radius<= 0:
        bot.score += 1
        ball.x = GAME_WIDTH//2
        ball.y = GAME_HEIGHT //2
        ball.velocity_x = random.choice(ball.possible_velocity)
        ball.velocity_y = random.choice(ball.possible_velocity)
    
    elif ball.x +ball.radius >= GAME_WIDTH:
        player.score += 1
        ball.x = GAME_WIDTH//2
        ball.y = GAME_HEIGHT //2
        ball.velocity_x = random.choice(ball.possible_velocity)
        ball.velocity_y = random.choice(ball.possible_velocity)

    if ball.y - ball.radius <= 0:
        ball.velocity_y *= -1
    
    elif ball.y + ball.radius >= GAME_HEIGHT:
        ball.velocity_y *= -1


    #BALL COLLISION WITH PADDLES
    topBall = ball.y - ball.radius
    bottomBall = ball.y + ball.radius
    closest_x_right = ball.x - ball.radius #closect distance to the right side of paddle
    
    if (bottomBall >= player.y) and (topBall <= player.y + player.height) and (closest_x_right <= player.x + player.width):
        
        player_center = player.y + (player.height//2)
     
        distance = ball.y - player_center
        bounce_factor = distance / (player.height //2)
        ball.velocity_y = bounce_factor * MAX_BOUNCE_SPEED
        if abs(ball.velocity_y) <= MINIMUM_BOUNCE_SPEED:
        # ball.velocity_y = MINIMUM_BOUNCE_SPEED + (0.5 + abs(ball.velocity_y)) * (1 if ball.velocity_y > 0 else 1)
            ball.velocity_y = MINIMUM_BOUNCE_SPEED
        ball.velocity_x  *= -1


    if (bottomBall >= bot.y) and (topBall <= bot.y + bot.height) and (ball.x + ball.radius>= bot.x):
        bot_center = bot.y + (bot.height//2)
        distance = ball.y - bot_center
        bounce_factor = distance / (bot.height //2)
        ball.velocity_y = bounce_factor * MAX_BOUNCE_SPEED
        ball.velocity_y = bounce_factor * MAX_BOUNCE_SPEED
        if abs(ball.velocity_y) <= MINIMUM_BOUNCE_SPEED:
        # ball.velocity_y = MINIMUM_BOUNCE_SPEED + (0.5 + abs(ball.velocity_y)) * (1 if ball.velocity_y > 0 else 1)
            ball.velocity_y = MINIMUM_BOUNCE_SPEED

        ball.velocity_x  *= -1
    
    if player.score == 10 and bot.score != 10:
        playerWinState= True
        ball.velocity_y = 0
        ball.velocity_x =0
    elif player.score != 10 and bot.score == 10:
        botWinState= True
        ball.velocity_y = 0
        ball.velocity_x =0
  
        
        
    
def move():
    ball.y += ball.velocity_y
    ball.x += ball.velocity_x

def botMovement():
    global lastTimeBotMoved
    current_time = pygame.time.get_ticks()
    reaction_delay = 40
    if current_time - lastTimeBotMoved >= reaction_delay:
        lastTimeBotMoved = current_time
        if ball.y  > bot.y+ (bot.height //2) and ball.velocity_x>0:
            bot.y += bot.velocity_y
        elif ball.y < bot.y + (bot.height //2) and ball.velocity_x >0:
            bot.y += -bot.velocity_y
        

def restart():
    global botWinState , playerWinState
    player.score = 0
    bot.score = 0
    ball.velocity_x = random.choice(ball.possible_velocity)
    ball.velocity_y = random.choice(ball.possible_velocity)
    botWinState = False
    playerWinState = False
    bot.x = BOT_X
    bot.y = BOT_Y
    player.x = PLAYER_X
    player.y = PLAYER_Y

player = Player()
ball = Ball()
bot = Bot()
lastTimeBotMoved = 0
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
    
    if keys[pygame.K_RETURN]:
        restart()

    if keys[pygame.K_BACKSPACE]:
        running = False
        sys.exit()
    check_collision()
    botMovement()
    move()
    draw() 
    pygame.display.update()
  
    clock.tick(40)


