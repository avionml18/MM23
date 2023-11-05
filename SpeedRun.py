#speedrun
#inputs: 
# x-coord: x-coordinate of current square
# y-coord: y-coordinate of current square
# currpath: shortest path to the current square
#output: updated ShortestPath value of all explored squares
def speedrun(xcoord, ycoord, currpath, maze):
    #base case to ensure the ShortestPath is bigger than the current path
    mazetemp = maze
    if maze[xcoord][ycoord].shortest_route > currpath+1:
        #initialize shortest path to start (0)
        if maze[xcoord][ycoord].is_start == 1:
            mazetemp[xcoord][ycoord].shortest_route = 0
            
        #every other square besides the start
        else:
            mazetemp[xcoord][ycoord].shortest_route = currpath+1
        #is the current square is not the finish...    
        if maze[xcoord][ycoord].is_dest == 0:
            #checks each square around the current square and recalls the function
            if maze[xcoord][ycoord].w_north == 0 and maze[xcoord][ycoord-1].is_explore == 1:
                mazetemp = speedrun(xcoord, ycoord-1, maze[xcoord][ycoord].shortest_route, maze)
            if maze[xcoord][ycoord].w_south == 0 and maze[xcoord][ycoord+1].is_explore == 1:
                mazetemp = speedrun(xcoord, ycoord+1, maze[xcoord][ycoord].shortest_route, maze)
            if maze[xcoord][ycoord].w_east == 0 and maze[xcoord+1][ycoord].is_explore == 1:
                mazetemp = speedrun(xcoord+1, ycoord, maze[xcoord][ycoord].shortest_route, maze)
            if maze[xcoord][ycoord].w_west == 0 and maze[xcoord-1][ycoord].is_explore == 1:
                mazetemp = speedrun(xcoord-1, ycoord, maze[xcoord][ycoord].shortest_route, maze)
                
    return mazetemp
#generate_directions
#inputs:
#x-coord: x-coordinate of the current square
#y-coord: y-coordinate of the current square
#output: optimal list of directions for the mouse
def generate_directions(xcoord, ycoord, maze, mazeSize):
    #placeholder numbers
    north = 256
    south = 256
    east = 256
    west = 256
    directions = ['X']*(mazeSize*mazeSize)

    #if the current square is not the start
    if maze[xcoord][ycoord].is_start == 0:
        #checks the shortest path of the immediate squares around the current square 
        if maze[xcoord][ycoord].w_north == 0 and ycoord > 0:
            if maze[xcoord][ycoord-1].is_explore == 1:
                north = maze[xcoord][ycoord-1].shortest_route
        if maze[xcoord][ycoord].w_south == 0 and ycoord < 3:
            if maze[xcoord][ycoord+1].is_explore == 1:
                south = maze[xcoord][ycoord+1].shortest_route
        if maze[xcoord][ycoord].w_east == 0 and  xcoord < 3:
            if maze[xcoord+1][ycoord].is_explore == 1:
                east = maze[xcoord+1][ycoord].shortest_route
        if maze[xcoord][ycoord].w_west == 0 and xcoord > 0:
            if maze[xcoord-1][ycoord].is_explore == 1:
                west = maze[xcoord-1][ycoord].shortest_route
                
        #compares the shortest route of the immediate surrounding squares and generates a direction
        if north <= south and north <= west and north <= east:
            directions[maze[xcoord][ycoord-1].shortest_route] = 'south'
            generate_directions(xcoord,ycoord-1,maze,mazeSize)
        elif south <= north and south <= west and south <= east:
            directions[maze[xcoord][ycoord+1].shortest_route] = 'north'
            generate_directions(xcoord,ycoord+1,maze,mazeSize)
        elif east <= south and east <= west and east <= north:
            directions[maze[xcoord+1][ycoord].shortest_route] = 'west'
            generate_directions(xcoord+1,ycoord,maze,mazeSize)
        elif west <= south and west <= north and west <= east:
            directions[maze[xcoord-1][ycoord].shortest_route] = 'east'
            generate_directions(xcoord-1,ycoord,maze,mazeSize)
    
    return directions
    
#generate_instructions
#inputs:
#xcoord: xcoordinate of the current sqaure
#ycoord: ycoordinate of the current sqaure
#ouput: list of motor instructions
def generate_instructions(xcoord,ycoord, maze, mazeSize, directions):
    #loops through the complete list of directions
    instructions = ['X']*maze[mazeSize/2][mazeSize/2].shortest_route
    for i in range(maze[xcoord][ycoord].shortest_route):
        #generates list of motor instructions
        #straight = 0
        #turn left = 1
        #turn right = 2
        #Note: These will be changed to match proper motor contol syntax
        if i == 0:
            instructions[i] = 0
        else :
            if directions[i] == directions[i-1]:
                instructions[i] = 0
            elif directions[i] == 'north' and directions[i-1] == 'west':
                instructions[i] = 2
            elif directions[i] == 'north' and directions[i-1] == 'east':
                instructions[i] = 1
            elif directions[i] == 'south' and directions[i-1] == 'east':
                instructions[i] = 2
            elif directions[i] == 'south' and directions[i-1] == 'west':
                instructions[i] = 1
            elif directions[i] == 'east' and directions[i-1] == 'north':
                instructions[i] = 2
            elif directions[i] == 'east' and directions[i-1] == 'south':
                instructions[i] = 1
            elif directions[i] == 'west' and directions[i-1] == 'south':
                instructions[i] = 2
            elif directions[i] == 'west' and directions[i-1] == 'north':
                instructions[i] = 1
    return instructions
