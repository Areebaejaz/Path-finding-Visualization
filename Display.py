import pygame
from pygame import mixer
import math
from queue import PriorityQueue

WIDTH = 600                                            # Width of the display screen.
WIN = pygame.display.set_mode((WIDTH, WIDTH))          # Setting a display screen size.
pygame.display.set_caption("A* Path Finding Algorithm")# Caption of a window.



# Color codes for making paths and changing colors.
# Uppercase determines they are constant.

RED       = (255, 0, 0)
GREEN     = (0, 255, 0)
BLUE      = (0, 255, 0)
YELLOW    = (255, 255, 0)
WHITE     = (255, 255, 255)
BLACK     = (0, 0, 0)
PURPLE    = (128, 0, 128)
ORANGE    = (255, 165, 0)
GREY      = (128, 128, 128)
TURQUOISE = (64, 224, 208)


# Building  main visualiztion tool.
# holds bunch of different values.

class Spot:
    
    # To define total cubes and their appearence on screen.
    def __init__(self, row, col, width, total_rows):
        self.mixer      =mixer
        self.row        = row
        self.col        = col
        self.x          = row * width    # Actual corner position on screen.
        self.y          = col * width    # Actual corner position on screen.
        self.color      = WHITE          # Color of cubes.
        self.neighbors  = []
        self.width      = width
        self.total_rows = total_rows

    # Represent rows and columns.
    def get_pos(self):
        return self.row, self.col

    # Red color determines that we already looked at that path.
    def is_closed(self):
        return self.color == RED

    # Open point Color. 
    def is_open(self):
        return self.color == GREEN

    # It is a barrier we have to avoid that path.
    def is_barrier(self):
        return self.color == BLACK

    # It is the start node from which the path starts.
    def is_start(self):
        return self.color == ORANGE

    # End point color.
    def is_end(self):
        return self.color == TURQUOISE

    # change the color back to white.
    def reset(self):
        self.color = WHITE

# Actually changes the color.
    # Starting piont.
    def make_start(self):
        self.color = ORANGE

    # Already looked at the path.
    def make_closed(self):
        self.color = RED

    # Open point.
    def make_open(self):
        self.color = GREEN

    # Avoid the path.
    def make_barrier(self):
        self.color = BLACK

    # Ending point.
    def make_end(self):
        self.color = TURQUOISE

    # It is the path to follow.
    def make_path(self):
        self.color = PURPLE

    # Draw cube on the display screen.
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))      #Draw a cube in pygame

    # updating the neighbors of spot
    def update_neighbors(self,grid):
        self.neighbors = []
        if self.row < self.total_rows-1 and not grid[self.row+1][self.col].is_barrier(): # moving Down
            self.neighbors.append(grid[self.row+1][self.col])
            
        if self.row > 0  and not grid[self.row-1][self.col].is_barrier():                # moving Up
            self.neighbors.append(grid[self.row-1][self.col])
            
        if self.col < self.total_rows-1 and not grid[self.row][self.col+1].is_barrier(): # moving Right
            self.neighbors.append(grid[self.row][self.col+1])
            
        if self.col > 0 and not grid[self.row][self.col-1].is_barrier():                 # moving Left
            self.neighbors.append(grid[self.row][self.col-1])

    # defines what happened when we compare two spots
    def _LT_(self, other):
        return False
    
# Heuristic function    
# Figure out the distance between two points
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)
