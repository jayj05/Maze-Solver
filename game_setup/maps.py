import pygame
import csv
import os

from game_setup.mainwindow import MainWindow
from .colors import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, type, row, col):
        super().__init__()
        self.image = image
        self.total_rows = 20
        self.total_cols = 28
        self.row = row 
        self.col = col 
        self.color = WHITE 
        self.type = type
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

        self.neighbors = []
        # This varibale will be used to determine whether the tile is in the open set 
        self.status = ""
    
    def get_pos(self):
        return self.row, self.col

    def is_start(self):
        return self.color == ORANGE
    
    def is_end(self):
        return self.color == TURQUOISE
    
    def is_open(self):
        return self.color == GREEN
    
    def is_closed(self):
        return self.status == RED
    
    def is_barrier(self):
        return self.type == "border"
    
    def make_start(self):
        self.color = ORANGE
        self.image = pygame.Surface((32, 32))
        self.image.fill(self.color)
    
    def make_end(self):
        self.color = TURQUOISE
        self.image = pygame.Surface((32, 32))
        self.image.fill(self.color)

    def make_open(self):
        self.color = GREEN
        self.image = pygame.Surface((32, 32))
        self.image.fill(self.color)
    
    def make_closed(self):
        self.color = RED 
        self.image = pygame.Surface((32, 32))
        self.image.fill(self.color)
    
    def reset(self):
        self.color = WHITE
    
    def make_path(self):
        self.color = PURPLE
        self.image = pygame.Surface((32, 32))
        self.image.fill(self.color)

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.rect.x, self.rect.y, 32, 32))

    def update_neighbors(self, grid):
        self.neighbors = []

        if self.row < self.total_rows - 1 and not grid[self.row+1][self.col].is_barrier(): # DOWN
            self.neighbors.append(grid[self.row+1][self.col])

        if self.row > 0 and not grid[self.row-1][self.col].is_barrier(): # UP
            self.neighbors.append(grid[self.row-1][self.col])

        if self.col < self.total_cols - 1 and not grid[self.row][self.col+1].is_barrier(): # LEFT
            self.neighbors.append(grid[self.row][self.col+1])

        if self.col > 0 and not grid[self.row][self.col-1].is_barrier(): # RIGHT
            self.neighbors.append(grid[self.row][self.col-1])

    def __lt__(self, other):
        return False 


class TileMap():
    def __init__(self, spritesheet, csv_filename):
        self.sheet = spritesheet
        self.tile_size = 32
        self.start_x = 0 
        self.start_y = 0

        # 2-D List containing all the tiles in the map 
        self.tiles = self.load_tiles(csv_filename)


        # In order to blit a sprite object onto a surface in pygame
        # you have to add it to a sprite group and then draw that group
        # on to the screen. 
        self.tile_group = pygame.sprite.Group()
        for r in self.tiles:
            for c in r:
                self.tile_group.add(c)
        

    def draw_map(self, surface):
        self.tile_group.draw(surface)

    # Creating a sprite object for each tile in the map and storing its type
    # along with position on the screen
    def load_tiles(self, filename):
        tiles = [] 
        tilemap = self.read_csv(filename)
        
        row, col = 0, 0
        for r in tilemap:
            col = 0
            temp = []
            for tile in r:
                if tile == '0':
                    temp.append(Tile(self.walkable_tile(32, 32), col*self.tile_size, row*self.tile_size, 'walkable', row, col))
                elif tile == '1':
                    temp.append(Tile(self.border_tile(32, 32), col*self.tile_size, row*self.tile_size, 'border', row, col))
                elif tile == '3':
                    temp.append(Tile(self.exit_tile(32, 32), col*self.tile_size, row*self.tile_size, 'exit', row, col))
                # Move to next tile in row
                col += 1
            # Move to next row
            tiles.append(temp)
            row += 1

        return tiles
    
    # Creates a 2D list of each row in a csv file
    # which will be the map of the game
    def read_csv(self, filename):
        map = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))
            return map

    # Each of these functions portion out a section of the sprite sheet 
    # that pertains to the desired tile          
    def border_tile(self, width, height):
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(self.sheet, (0, 0), (32, 0, width, height))
        return image
        
    def walkable_tile(self, width, height):
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(self.sheet, (0, 0), (0, 0, width, height))
        return image

    def exit_tile(self, width, height):
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(self.sheet, (0, 0), (64, 0, width, height))
        return image