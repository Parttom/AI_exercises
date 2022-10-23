def astar(graph, start, end):
    start = start
    end = end
    open_list = []
    close_list = []

    #add the start city to the open list

    find the neighbours of the start city
    for all the neighbours
        start with the best guess
        if the neighbour is already open
            if the cost is less
                follow that path
            else disregard it
        if the neighbour is already closed
            disregard it
        if the neighbour has not been seen before
            follow that path

