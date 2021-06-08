import pygame
from pygame import mixer
import math
from queue import PriorityQueue

WIDTH = 600                                            # Width of the display screen.
WIN = pygame.display.set_mode((WIDTH, WIDTH))          # Setting a display screen size.

# Including exception handling
try:
    caption_file = open("caption.txt", "r")            # open a file to read its data                       
    content = caption_file.read()
    pygame.display.set_caption(content)                # Caption of a window.

except IOError:
    print("Error! can't find 'Caption' file or read data.")

else:
    caption_file.close()                               # close the file


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

    # GREY color determines that we already looked at that path.
    def is_closed(self):
        return self.color == GREY

    # Open point Color. 
    def is_open(self):
        return self.color == YELLOW

    # It is a barrier we have to avoid that path.
    def is_barrier(self):
        return self.color == BLACK

    # It is the start node from which the path starts.
    def is_start(self):
        return self.color == TURQUOISE

    # End point color.
    def is_end(self):
        return self.color == RED

    # change the color back to white.
    def reset(self):
        self.color = WHITE

# Actually changes the color.
    # Starting piont.
    def make_start(self):
        self.color = TURQUOISE

    # Already looked at the path.
    def make_closed(self):
        self.color = GREY

    # Open point.
    def make_open(self):
        self.color = YELLOW

    # Avoid the path.
    def make_barrier(self):
        self.color = BLACK

    # Ending point.
    def make_end(self):
        self.color = RED

    # It is the path to follow.
    def make_path(self):
        self.color = GREEN

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

# Actual shortest past from the starting point to the ending point.
def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def algorithm(draw, grid, start, end):                            # draw is a function
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))                               # put add these to the priority queue.'0' is the start node f_score and 'count' is any number 'start' is the actual node for the spot
    came_from = {}                                                # Tells what node did this node come from.Keep track of the path 
    g_score = {spot:float("inf") for row in grid for spot in row} # Starts at float infinity
    g_score[start] = 0                                            # Start node is 0
    f_score = {spot:float("inf") for row in grid for spot in row} # Starts at float infinity
    f_score[start] = h(start. get_pos(), end.get_pos())           # Distance of end node from start node

    open_set_hash = {start}               # keep track of all the items that are in the priorityQueue and all the items that aren't in the priorityQueue 

    while not open_set.empty():           # This algorithm runs till the open set is empty
        for event in pygame.event.get():  # Way to exit
            if event.type == pygame.QUIT: # Hit the 'X' button to quit
                pygame.quit()

        current = open_set.get()[2]       # Indexing at two means just want current node
        open_set_hash.remove(current)     # Remove current from open_set_hash to avoid any duplicate

        if current == end:                # If current node is the end node we founnd the shortest path

             # including exception handling
             try:
                 pygame.mixer.init()            # initializing music in pygame 
                 mixer.music.load("soundeffect3.mp3")  # music plays when we find the path
                 mixer.music.play(1)            
                 pygame.mixer.quit       
             except pygame.error as message:
                 print("Error! can't ecxess to the music file.")
                 
             reconstruct_path(came_from, end, draw) 
             end.make_end()
             return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1  # Add one to the current score for the shortest path

            if temp_g_score < g_score[neighbor]: # If we found a better way to reach this neighbor that we didn't found this before update this path score
                came_from[neighbor] = current   
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                
                if neighbor not in open_set_hash: 
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))# We consider neighbor because it has the better path
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
                    
        draw()    # Calling draw function
        
        if current != start: # If the currnt node is not the start node make it close
            current.make_closed()
            
    return False  # Says that we did not find the path 
    
# holds all the spots in the grid
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([]) # making list of list
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    return grid

# draw the grid lines
def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows): # horizontal lines
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows): # vertical lines
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

# main draw function which draws everything
def draw(win, grid, rows, width):
    win.fill(WHITE) # fills the entire screen with white color

    for row in grid:
        for spot in row:
            spot.draw(win) # draw the spots

    draw_grid(win, rows, width)
    pygame.display.update() # displays that we draw and update

# mouse position that figure out what cube or spot we clicked
def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos         # to figure out what is the position of x and y 

    row = y // gap     # divide the position by the width of the cubes
    col = x // gap     # this describes where we are

    return row, col

# main loops determines all of the checks 
def main(win, width):
    ROWS = 40                    # cubes in a row and coloumn
    grid = make_grid(ROWS, width)# generate grid gives us the 2D ray spots

    start = None # starting position is none
    end = None   # end psotion is also none

    run = True   
    started = False
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                    # if we press the 'X' button at the top right of the screen stop the game
                run = False

            if pygame.mouse.get_pressed()[0]:                # Left mouse button
                pos = pygame.mouse.get_pos()                 # gives the position of mouse on the pygame screen
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]                        # indexing row coloumn in the grid
                
                if not start and spot != end:
                    start = spot
                    start.make_start()
                    
                elif not end and spot != start:
                    end = spot
                    end.make_end()

                elif spot != end and spot != start:
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]:              # Right mouse button 
                 pos = pygame.mouse.get_pos()                # gives the position of mouse on the pygame screen
                 row,col = get_clicked_pos(pos,ROWS,width) 
                 spot = grid[row][col]                       # indexing row coloumn in the grid
                 spot.reset()
                 if spot == start:
                     start = None
                 elif spot == end:
                     end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    try:
                        pygame.mixer.init()            # initializing music in pygame 
                        mixer.music.load("soundeffect.WAV") # music plays when we press space key
                        mixer.music.play(-1)            
                        pygame.mixer.quit       
                        
                    except pygame.error as message:
                        print("Error! can't ecxess to the music file.")    
                    
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)   
                            
                        
                    # lambda means pass a function as an argument to another function and call there directly        
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
                    
                    
                      
                if event.key == pygame.K_c: # clear the entire screen makes everything white
                    start = None
                    end = None
                    grid = make_grid(ROWS,width)

    pygame.quit() # exits the pygame window

main(WIN, WIDTH)
    
#     ~~~~~~REFERENCE~~~~~~
#  https://youtu.be/JtiK0DOeI4A
