import pygame 
import sys 



WIDTH, HEIGHT = (500, 500)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

sprite_sheet_image = pygame.image.load('trainer_sheet.png').convert_alpha()

BG = (50, 50, 50)

clock = pygame.time.Clock()

def get_image(sheet, frame, width, height, scale, color):
    image = pygame.Surface((width, height))
    image.blit(sheet, (0, 0), (frame*width, 0, width, height))
    image = pygame.transform.scale(image, (width*scale, height*scale))
    image.set_colorkey(color)
    return image

BLACK = (0, 0, 0)

frame0 = get_image(sprite_sheet_image, 0, 64, 64, 1, BLACK)
frame1 = get_image(sprite_sheet_image, 1, 64, 64, 1, BLACK)

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
    
    WIN.fill(BG)
    WIN.blit(frame0, (0, 0))
    WIN.blit(frame1, (100, 0))
    pygame.display.update()