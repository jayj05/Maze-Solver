import pygame
import sys
from game_setup import MainWindow, GameMechanics, Player, TileMap, colors, maze_solver

WIN = MainWindow.WIN
pygame.display.set_caption("A* Path Finding Algorithm")
FPS = GameMechanics.FPS 
RECT_VELOCITY = GameMechanics.RECT_VELOCITY

trainer_sprite_sheet = pygame.image.load('Assets/trainer_sheet.png')
player = Player(trainer_sprite_sheet, 64, 64)

player_group = pygame.sprite.Group()
player_group.add(player)

tile_sprite_sheet = pygame.image.load('Assets/default_tiles_x.png')
csv_file = 'Assets/maze.csv'
tilemap = TileMap(tile_sprite_sheet, csv_file)
# tilemap.tiles is a 2D list that contains all the instances of the tile objects on the map

path_finder = maze_solver.MazeSolver()

def main():
    
    running = True 
    clock = pygame.time.Clock()

    grid = tilemap.tiles 

    ROWS = 20
    COLS = 28

    start = None 
    end = None

    started = False 
    while running:

        player_collision_list = pygame.sprite.spritecollide(player, tilemap.tile_group, False)
        clock.tick(FPS)

        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            
            if started:
                continue

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = player.get_clicked_pos(pos, MainWindow.WIDTH, MainWindow.HEIGHT, ROWS, COLS)
                tile = grid[row][col]

                if not start and tile != end and tile.type != "border":
                    start = tile 
                    start.make_start()
                elif not end and tile != start and tile.type != "border":
                    end = tile 
                    end.make_end()
            

            # Beginning movement when key is pressed 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    player.move_backward()
                elif event.key == pygame.K_w:
                    player.move_forward()
                elif event.key == pygame.K_a:
                    player.move_left()
                elif event.key == pygame.K_d:
                    player.move_right()
                elif event.key == pygame.K_SPACE and not started:
                    for row in grid:
                        for tile in row:
                            tile.update_neighbors(tilemap.tiles)
                    
                    path_finder.search(lambda: tilemap.draw_map(WIN), tilemap.tiles, start, end)
            
            # Stopping movement when key is not being pressed 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_s:
                    player.move_backward_done()
                elif event.key == pygame.K_w:
                    player.move_forward_done()
                elif event.key == pygame.K_a:
                    player.move_left_done()
                elif event.key == pygame.K_d:
                    player.move_right_done()
        
        # Making sure player can't go above the starting point
        if player.rect.y - RECT_VELOCITY < 0:
            player.rect.y += RECT_VELOCITY

        # Tile collisions 
        for tile in player_collision_list:
            if tile.type == 'walkable':
                pass
            
            elif tile.type == 'border':
                # Player is coming to the right of the tile 
                if player.rect.x > tile.rect.x:
                    player.rect.x += RECT_VELOCITY
                # Player is coming to the left of the tile 
                if player.rect.x < tile.rect.x:
                    player.rect.x -= RECT_VELOCITY
                # Player is coming from the top of the tile 
                if player.rect.y < tile.rect.y:
                    player.rect.y -= RECT_VELOCITY
                # Player is coming from the bottom of the tile 
                if player.rect.y > tile.rect.y:
                    player.rect.y += RECT_VELOCITY

            elif tile.type == 'exit':
                pass
    
        WIN.fill(colors.BLACK)
        tilemap.draw_map(WIN)
        player_group.draw(WIN)
        player_group.update()
        pygame.display.update()

if __name__ == "__main__":
    main()