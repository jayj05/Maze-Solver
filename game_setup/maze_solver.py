import os 
from queue import PriorityQueue
import pygame


class MazeSolver():

    def reconstruct_path(self, came_from, current, draw):
        
        # Only looping until we reach the start node, which is not inside the came_from hash
        while current in came_from:
        # Backtracking from the end node to the start node
            current = came_from[current]
            current.make_path()
            draw()

    def search(self, draw, grid, start, end):
        
        # Used as a tiebreaker in case the f_score of the nodes in the Priority Queue are equal 
        count = 0
        # A queue that serves items based on their priority number, PriorityQueue(priority number, data), the smallest priority number being served first
        # Will be used to store data pertaining to the neighbors of the current node 
        open_set = PriorityQueue()

        # A* always starts off by putting the start node first in the open set. 
        open_set.put((0, count, start))

        # Dict that will store the neighbor as a key and the node we used to get to that neighbor as the value 
        came_from = {}

        g_score = {tile: float("inf") for row in grid for tile in row}
        g_score[start] = 0

        f_score = {tile: float("inf") for row in grid for tile in row}
        f_score[start] = self.h(start.get_pos(), end.get_pos())

        # Keeping track of what is in the PriorityQueue
        open_set_hash = {start} 

        while not open_set.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            # Popping the node with the lowest f_score from the open_set
            current = open_set.get()[2]
            # Keeping track of what leaves the open_set
            open_set_hash.remove(current)

            # Once we pop the end node from the open set, our search is complete and now we need to backtrack the path it took to get to the end node
            if current == end:
                self.reconstruct_path(came_from, end, draw)
                end.make_end()
                return True

            for neighbor in current.neighbors:
                
                # All edges on the graph have a weight of 1, so the g_score of our neighbor is 1 more than the current node
                temp_g_score = g_score[current] + 1

                # If the g_score from our current node to the neighbor is less than the current g_score of that neighbor
                # we will update the g_score of the neighbor because that means we have found a shorter path to that node
                # we are always looking for the best path to every node when it comes to the g score 
                if temp_g_score < g_score[neighbor]:

                    came_from[neighbor] = current 
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + self.h(neighbor.get_pos(), end.get_pos())

                    if neighbor not in open_set_hash:
                        count += 1 
                        open_set.put((f_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)
                        neighbor.make_open()
            
            draw()

            # If the node we just considered is not the start node, then make it closed 
            if current != start:
                current.make_closed()
        
        return False 



    def h(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2 
        return abs(x2-x1) + abs(y2-y1)
