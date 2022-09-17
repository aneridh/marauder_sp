import pygame
import random #enemy location
import math #distance formula

from pygame import mixer
#mixer - package to include all kind of music

#initialize the module : must
pygame.init()

#screen_dimensions- windows (create a screen)
screen = pygame.display.set_mode((800,600))

#any action within the game window is defined as an event
#1_pressing any keys
#2_pressing red exit button

#title and icon:
pygame.display.set_caption("Space Marauder")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

#background
background = pygame.image.load('background.jpg')
#to be used in main while loop

#Background Sound
mixer.music.load('bg_final_m.mp3') #continuous sound load is used else sound
mixer.music.play(-1)# -1 denotes on loop

#player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480 # 0 = top, 600 = bottom
playerX_change = 0
# playerY_change = 0

#enemy_for multiple enemy - list: also need to change the game loop in order to specify which enemy:
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemy = 5

for i in range(num_of_enemy):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150)) # 0 = top, 600 = bottom
    enemyX_change.append(0.3)
    enemyY_change.append(40)

#bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0 #will not be used
bulletY_change = 10 
bullet_state = "Ready"
#Fire - bullet in motion
#Ready - stagnant

#Score:

score_value = 0 #global variable for scoring
font = pygame.font.Font('freesansbold.ttf',32) #pygame object to specify the type of font
#coordinates for score display
textX = 610
textY = 10


def show_score(x,y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 0))
    screen.blit(score,(x,y))

def player(x,y):
    #parameters: movement of image
    screen.blit(playerImg,(x,y))
    #blit : draw image on screen
    #2 parameters : 1 = image 2 = coordinates

def enemy(x,y,i):
    #parameters: movement of image
    screen.blit(enemyImg[i],(x,y))
    #blit : draw image on screen
    #2 parameters : 1 = image 2 = coordinates

#bullet_state and drawing image
def fire_bullet(x,y):
    global bullet_state
    bullet_state = "Fire"
    screen.blit(bulletImg,(x + 16, y + 10))

#collision _ enemy and bullet: distance formula (coordinate geometry)
def isCollision(enemyX,enemyY,bulletX,bulletY):
    D = math.sqrt(((enemyX-bulletX)**2) + ((enemyY-bulletY)**2))
    if D <= 27: #trial and testing _ to call collision
        return True
    else:
        return False

#Game Over
over = pygame.font.Font('freesansbold.ttf',64) #pygame object to specify the type of font

def game_over_text():
    over_text = over.render("Game Over!", True, (255, 255, 255))
    screen.blit(over_text,(210,250))#coodinates for centre
    
#game_loop
running = True
while running: #infinite_loop : only exit when condition becomes False
#display screen  would be considered inside the game window hence to take it into the while loop
#RGB - Red, Green, Blue
#values : RGB : (0,255) range
#do not forget indentation : (if) will display color on pressing exit button
    screen.fill(( 0, 0, 0))    
    # playerX -= 0.1
    # print(playerX)
    # playerY -= 0.1
    # print(playerY)

    #background - image : blit to draw
    #after black screen - layers
    screen.blit(background,(0,0))
#exit game window    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:#quit - capslock 
            running = False
        #if keystroke is pressed check : left or right
        if event.type == pygame.KEYDOWN:
            # print("A keyboard stroke is pressed")
            if event.key == pygame.K_LEFT:
                # print("Left arrow is pressed")
                playerX_change -= 0.5
            if event.key == pygame.K_RIGHT:
                # print("Right arrow is pressed") 
                playerX_change += 0.5
            if event.key == pygame.K_SPACE:
                if bullet_state == "Ready":
                    bulletX = playerX #individual bullet location
                    fire_bullet(bulletX, bulletY)  
                    bullet_Sound = mixer.Sound('bullet.wav')
                    bullet_Sound.play()#not on loop
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                # print("Keystroke has been released")
                playerX_change = 0 #stop image moving when released
#call player function after scree.fill : layers overlapping    
    playerX += playerX_change
    # playerY += playerY_change

    #setting Boundary: horizontal
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736: # size of img 64 pixels
        playerX = 736
    
   

    #enemy_algo
    for i in range(num_of_enemy):
        #Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemy):
                enemyY[j] = 1500 #in oder to move each enemy out of the window
            game_over_text() #function to display game over
            over_Sound = mixer.Sound('bullseye.wav')
            over_Sound.play()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.5
            enemyY[i] += enemyY_change[i]

        elif enemyX[i] >= 736: # size of img 64 pixels
            enemyX_change[i] = -0.5
            enemyY[i] += enemyY_change[i]
    
        #collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "Ready"
            score_value += 1
            enemyX[i] = random.randint(0,735)#reset enemy to default location
            enemyY[i] = random.randint(50,150)
            # print(score)
            collision_Sound = mixer.Sound('score_music.mp3')
            collision_Sound.play()#not on loop
        enemy(enemyX[i], enemyY[i], i)

    #bullet_movement
    if bulletY <= 0: #multiple bullets
        bulletY = 480
        bullet_state = "Ready"
    if bullet_state == "Fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    

    player(playerX,playerY)
    show_score( textX, textY)

#update the display: must
#indentation
    pygame.display.update()
