import pygame 
import sys 

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.sprites = []
        self.is_animating = False
        for i in range(10):
            self.sprites.append(pygame.transform.scale(pygame.image.load(f'notes/frog_images/move_{str(i)}.png'), (250, 150)))

        self.current_sprite = 0 
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = (pos_x, pos_y)
    
    def animate(self):
        self.is_animating = True
    
    def update(self):
        if self.is_animating:
            self.current_sprite += 0.25
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
                self.is_animating = False
            self.image = self.sprites[int(self.current_sprite)]

clock = pygame.time.Clock()
FPS = 60

WIDTH, HEIGHT = 400, 400 
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('sprite animation')

moving_sprites = pygame.sprite.Group()
player = Player(10, 10)
moving_sprites.add(player)

running = True 
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
        if event.type == pygame.KEYDOWN:
            player.animate()

    WIN.fill((255, 255, 255))
    moving_sprites.draw(WIN)
    moving_sprites.update()
    pygame.display.update()
