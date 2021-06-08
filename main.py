# main loops determines all of the checks 
def main(win, width):
    ROWS = 30  # cubes in a row and coloumn
    grid = make_grid(ROWS, width)# generate grid gives us the 2D ray spots

    start = None # starting position is none
    end = None   # end psotion is also none

    run = True   
    started = False
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #if we press the 'X' button at the top right of the screen stop the game
                run = False

            if pygame.mouse.get_pressed()[0]:# Left mouse button
                pos = pygame.mouse.get_pos() # gives the position of mouse on the pygame screen
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]        # indexing row coloumn in the grid
                
                if not start and spot != end:
                    start = spot
                    start.make_start()
                    
                elif not end and spot != start:
                    end = spot
                    end.make_end()

                elif spot != end and spot != start:
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]:# Right mouse button 
                 pos = pygame.mouse.get_pos()  # gives the position of mouse on the pygame screen
                 row,col = get_clicked_pos(pos,ROWS,width) 
                 spot = grid[row][col]         # indexing row coloumn in the grid
                 spot.reset()
                 if spot == start:
                     start = None
                 elif spot == end:
                     end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                   
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
    
