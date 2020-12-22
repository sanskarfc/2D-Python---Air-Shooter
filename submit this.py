#importing pygame module
import pygame

#importing random module
import random

#importing time library to have time survived as the score
import time

#import pygame.locals to access keypresses
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

#setting up screen height and screen width
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


#defining the Player object extending pygame.sprite.Sprite
#instead of a surface, we use an image
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load(r"C:\Users\sansk\Desktop\fly.png").convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

    #by these, we can move the sprite up,down,left and right by 5 units by each key press
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        #this is to prevent the player leaving the game screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


#defining the enemy(i.e., the missiles here) extending pygame.sprite.Sprite
#instead of a surface, we use an image for a better looking sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load(r"C:\Users\sansk\Desktop\torpedo.png").convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        # The starting position is randomly generated, as is the speed
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        if(difficultyy=="E"):
            speed_end=10
            speed_start=5
        if(difficultyy=="M"):
            speed_end=20
            speed_start=15
        if(difficultyy=="H"):
            speed_end=30
            speed_start=29
        self.speed = random.randint(speed_start, speed_end)

    #moving objects
    #removing the missiles after the right edge of missiles passes the left edge of the game screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


#defining the cloud object
# Use an image for a better looking sprite
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load(r"C:\Users\sansk\Desktop\cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        #the starting position of the cloud is randomly generated using the random function
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    #moving the cloud at a constant speed
    #removing it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()

# Initialize pygame
pygame.init()

#Displaying the difficulty level on the game screen
myfont = pygame.font.SysFont('Comic Sans MS', 30)

difficultyy=input("Difficulty? : Easy(E) or Medium(M) or Hard(H)")

if(difficultyy=='E'):
    textsurface=myfont.render('EASY DIFFICULTY', False, (0,0,0))

if(difficultyy=='M'):
    textsurface=myfont.render('MEDIUM DIFFICULTY', False, (0,0,0))

if(difficultyy=='H'):
    textsurface=myfont.render('HARD DIFFICULTY', False, (0,0,0))

# Setup the clock for a decent framerate(had this idea from the internet)
clock = pygame.time.Clock()

start_time=time.time()
end_time=time.time()

font_time = pygame.font.SysFont(('Comic Sans MS'), 32)

def timer(x,y):
    font_times= font_time.render("TIME:"+str(int(end_time-start_time)),True,(0,0,0))
    screen.blit(font_times, (x,y))



# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create custom events for adding a new enemy and cloud
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

# Creating our 'player'
player = Player()

# Create groups to hold enemy sprites, cloud sprites, and all sprites
# - enemies is used for collision detection and position updates
# - clouds is used for position updates
# - all_sprites isused for rendering
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

#Background
background=pygame.image.load(r"C:\Users\sansk\Desktop\bg.png").convert()

#Variable to keep our main loop running
running = True

#Our main loop
while running:
    end_time=time.time()
    # Look at every event in the queue
    for event in pygame.event.get():
        #User hit the key
        if event.type == KEYDOWN:
            #Stop if ESC cap is pressed
            if event.key == K_ESCAPE:
                running = False

        #Close the game window when the user closes the game window
        elif event.type == QUIT:
            running = False

        # Adding a new enemy
        elif event.type == ADDENEMY:
            # Create the new enemy, and add it to our sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        #Adding new clouds
        elif event.type == ADDCLOUD:
            # Create the new cloud, and add it to our sprite groups
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    # Update the position of our enemies and clouds
    enemies.update()
    clouds.update()

    #Adding the background
    screen.blit(background, (0,0))

    # Draw all our sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    screen.blit(textsurface,dest=(0,0))

    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
        # If so, remove the player
        player.kill()

        # Stop the loop
        running = False

    timer(660,0)

    # Flip everything to the display
    pygame.display.flip()

    # Ensure we maintain a 30 frames per second rate
    clock.tick(30)
