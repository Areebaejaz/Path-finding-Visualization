# holds all the spots in the grid
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([]) # making list of list
        for j in range(rows):
            node=Node(i, j, gap, rows)
            grid[i].append(spot)
        return grid

# draw the grid lines
def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))
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