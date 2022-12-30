# Author: Bjorn Xiao 
# Date: 21/12/2022
# Ballon Shooting Game

from random import choice 
import os
import pygame
pygame.font.init() 
# version: pygame 2.1

WIDTH, HEIGHT = 900, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bjorn Xiao Balloon Shooting Game!")

WHITE = (250, 250, 250)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

BORDER = pygame.Rect(10, 10, WIDTH - 20, HEIGHT - 20)

IMAGE_WIDTH = 55
IMAGE_HEIGHT = 40
FPS = 60

MAX_BULLETS = 5
SHOOTER_VEL = 5         
BALLON_VEL = 3
BULLET_VEL = 10 * BALLON_VEL
BALLON_DIRECTION = 1

FONT = pygame.font.SysFont('comicsans', 80)
SMALL_FONT = pygame.font.SysFont('comicsans', 30)

SHOOTER_IMAGE = pygame.image.load(
    os.path.join('Bjorn_Xiao_Ballon', 'Assets', 'shotgun.png'))
SHOOTER = pygame.transform.rotate(
    pygame.transform.scale(SHOOTER_IMAGE, (IMAGE_WIDTH, IMAGE_HEIGHT)), -30)

BALLON_IMAGE = pygame.image.load(
    os.path.join('Bjorn_Xiao_Ballon', 'Assets', 'ballon.png'))
BALLON = pygame.transform.scale(BALLON_IMAGE, (IMAGE_WIDTH, IMAGE_HEIGHT))

HIT = pygame.USEREVENT + 1
MISS = pygame.USEREVENT + 2

def draw_window(ballon, shooter, bullets, missed_bullet):
    WIN.fill(BLACK)
    pygame.draw.rect(WIN, WHITE, BORDER)
    
    # Shooter is meant to be moved as player wish 
    WIN.blit(SHOOTER, (shooter.x, shooter.y))
    
    # Ballon moves 
    WIN.blit(BALLON, (ballon.x, ballon.y))
    
    # Missed Bullets counting
    missed_text = SMALL_FONT.render(
        "Missed bullets = " + str(missed_bullet), 1, RED)
    WIN.blit(missed_text, (40,10))
    
    # Bullets
    for bullet in bullets:
        pygame.draw.rect(WIN, RED, bullet)
    
    pygame.display.update()
    
def move_shooter(key_pressed, shooter):
    # Move shooter UP
    if key_pressed[pygame.K_UP] and shooter.top - SHOOTER_VEL > BORDER.top:              
        shooter.y -= SHOOTER_VEL
         
    # Move shooter DOWN
    if key_pressed[pygame.K_DOWN] and shooter.bottom + SHOOTER_VEL < BORDER.bottom:
        shooter.y += SHOOTER_VEL
        
def move_ballon(ballon):
    # Random moving up or down within the border
    global BALLON_DIRECTION
    
    if ballon.top <= BORDER.top or ballon.bottom >= BORDER.bottom: 
        BALLON_DIRECTION *= -1
    
    # Randomly change direction when it reaches midpoints
    if ballon.top == BORDER.bottom//2:
        change_direction = choice([-1,1])
        BALLON_DIRECTION *= change_direction
         
    ballon.y += BALLON_VEL * BALLON_DIRECTION

def handel_bullet(bullets, ballon, missed_bullet): 
    for bullet in bullets: 
        bullet.x += BULLET_VEL
        if ballon.colliderect(bullet):
            pygame.event.post(pygame.event.Event(HIT))
            bullets.remove(bullet)
        elif bullet.x > WIDTH:
            pygame.event.post(pygame.event.Event(MISS))
            bullets.remove(bullet)
            
            
            
def draw_winning_windows(text):
    winning_window = pygame.Rect(0, HEIGHT//2 - 50, WIDTH, 100)
    pygame.draw.rect(WIN, BLACK, winning_window)
    
    draw_text = FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2 , 
                         HEIGHT//2 - draw_text.get_height()//2))
    
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    ballon = pygame.Rect(800, 100, IMAGE_WIDTH, IMAGE_HEIGHT)
    shooter = pygame.Rect(50, 100, IMAGE_WIDTH, IMAGE_HEIGHT)
    
    bullets = []
    winning_text = ""
    missed_bullets = 0
    clock = pygame.time.Clock()
    run = True
    
    while run: 
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(bullets) < MAX_BULLETS: # FIRE A BULLET
                    bullet = pygame.Rect(
                        shooter.right, shooter.y + shooter.height//2, 10, 5) 
                    bullets.append(bullet)
            
            if event.type == HIT:
                winning_text = "YOU WON!"
            if event.type == MISS: 
                missed_bullets += 1
            
        if winning_text != "":
            draw_winning_windows(winning_text)
            break    
                    
        key_pressed = pygame.key.get_pressed()
        move_shooter(key_pressed, shooter)
        move_ballon(ballon)
        handel_bullet(bullets, ballon, missed_bullets)
        draw_window(ballon, shooter, bullets, missed_bullets)
                     
    pygame.quit()  
    
 
if __name__ == "__main__":
    main()  
    