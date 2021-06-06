# Actual shortest past from the starting point to the ending point.
def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()
        
# it is a function which tells where we are and gives the path
def algorithm(draw, grid, start, end):                            # draw is a function
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))                               # put add these to the priority queue.'0' is the start node f_score and 'count' is any number 'start' is the actual node for the spot
    came_from = {}                                                # Tells what node did this node come from.Keep track of the path 
    g_score = {spot:float("inf") for row in grid for spot in row} # Starts at float infinity
    g_score[start] = 0                                            # Start node is 0
    f_score = {spot:float("inf") for row in grid for spot in row} # Starts at float infinity
    f_score[start] = h(start. get_pos(), end.get_pos())           # Distance of end node from start node

    open_set_hash = {start}                                       # keep track of all the items that are in the priorityQueue and all the items that aren't in the priorityQueue 

    while not open_set.empty():           # This algorithm runs till the open set is empty
        for event in pygame.event.get():  # Way to exit
            if event.type == pygame.QUIT: # Hit the 'X' button to quit
                pygame.quit()

        current = open_set.get()[2]       # Indexing at two means just want current node
        open_set_hash.remove(current)     # Remove current from open_set_hash to avoid any duplicate

        if current == end:                # If current node is the end node we founnd the shortest path
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
    
