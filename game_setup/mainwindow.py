import pygame 

class MainWindow():
    WIDTH, HEIGHT = 896, 640
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    
    def __init__(self):
        pass
    

class GameMechanics():
    
    FPS = 60 
    VELOCITY = 0.5
    RECT_VELOCITY = 2