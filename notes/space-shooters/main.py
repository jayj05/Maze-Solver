import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
SURFACE = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('First Game') 

WHITE = (255,255,255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect((WIDTH//2) - 5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Pygame/Assets/Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Pygame/Assets/Gun+Silencer.mp3'))

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60
VELOCITY = 5
BULLET_VELOCITY = 7
MAX_BULLETS = 3

# Creating unique event IDs
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Pygame','Assets', 'spaceship_yellow.png')) # os.path.join will bring those two objects together and we are using it is because depending on your OS the file separator may be different
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Pygame','Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Pygame', 'Assets', 'space.png')), (WIDTH, HEIGHT))

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    SURFACE.blit(SPACE, (0, 0)) # Pygame has colors based on rgb value
    
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    SURFACE.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    SURFACE.blit(yellow_health_text, (10, 10))

    SURFACE.blit(YELLOW_SPACESHIP, (yellow.x,yellow.y)) # blit allows images to be put on screen, and when we draw an object in pygame we draw from the top left, the second argument is the x, y coordinate
    SURFACE.blit(RED_SPACESHIP, (red.x, red.y))
    pygame.draw.rect(SURFACE, BLACK, BORDER)

    for bullet in red_bullets:
        pygame.draw.rect(SURFACE, RED, bullet)
    
    for bullet in yellow_bullets:
        pygame.draw.rect(SURFACE, YELLOW, bullet)
    pygame.display.update() # This will allow for creations on the surface to be shown

# This main function will handle the main game loop in pygame
# When making a game you will have a loop doing things like redrawing the window or checking for certain conditions to be met
def yellow_handle_movement(entity, keys_pressed):
    if keys_pressed[pygame.K_a] and entity.x - VELOCITY > 0: # LEFT
        entity.x -= VELOCITY
    if keys_pressed[pygame.K_d] and entity.x + entity.width  < BORDER.x: # RIGHT
        entity.x += VELOCITY
    if keys_pressed[pygame.K_w] and entity.y - VELOCITY > 0: # UP
        entity.y -= VELOCITY
    if keys_pressed[pygame.K_s] and entity.y + VELOCITY + entity.height < HEIGHT - 12 : # DOWN
        entity.y += VELOCITY

def red_handle_movement(entity, keys_pressed):
    if keys_pressed[pygame.K_LEFT] and entity.x - VELOCITY > BORDER.x + BORDER.width: # LEFT
        entity.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and entity.x + VELOCITY + entity.width < WIDTH: # RIGHT
        entity.x += VELOCITY
    if keys_pressed[pygame.K_UP] and entity.y - VELOCITY > 0: # UP
        entity.y -= VELOCITY
    if keys_pressed[pygame.K_DOWN] and entity.y + entity.height < HEIGHT - 15: # DOWN
        entity.y += VELOCITY

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VELOCITY
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VELOCITY
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    SURFACE.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))

    pygame.display.update()
    pygame.time.delay(5000)

def main():
    # These rectangles are used to represent our spaceships so that we can keep track of their x and y position in the main game loop
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT) # Rect(x, y, width, height)
    yellow = pygame.Rect(pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
    
    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    running = True 
    while running:
        clock.tick(FPS) # This is controlling the speed of our while loop, so right now the while is moving at the designated frames per second, this designated frame rate is also allowing the speed of the program to remain consistent on all computers 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) <= MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) <= MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_FIRE_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_FIRE_SOUND.play()
        
        winner_text = ''
        if red_health <= 0:
            winner_text = "Yellow Wins!"
        
        if yellow_health <= 0:
            winner_text = "Red Wins!"
        
        if winner_text != '':
            draw_winner(winner_text)
            break
        keys_pressed = pygame.key.get_pressed() # Every time the while loop runs it is going to tell us what keys are being pressed down
        yellow_handle_movement(yellow, keys_pressed)
        red_handle_movement(red, keys_pressed)
        # For example since our loop is running 60 times per second that means that red.x is getting updated 60 times per second
        
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
    
    main()

if __name__ == "__main__":
    main()