#speedrun
#inputs: 
# xcoord: x-coordinate of current sqaure
# ycoord: y-coordinate of current sqaure
# currpath: shortestpath to the current square
#output: updated ShortestPath value of all explored squares
def speedrun(xcoord, ycoord, currpath):
    #base case to ensure the ShortestPath is bigger than the current path
    if maze[xcoord][ycoord].ShortestPath > currpath+1:
        #initialize shortest path to start (0)
        if maze[xcoord][ycoord].Start == 1:
            maze[xcoord][ycoord].ShortestPath = 0
            
        #every other square besides the start
        else:
            maze[xcoord][ycoord].ShortestPath = currpath+1
        #is the current sqaure is not the finish...    
        if maze[xcoord][ycoord].Finish == 0:
            #checks each sqaure around the current sqaure and recalls the function
            if maze[xcoord][ycoord].WallNorth == 0 and maze[xcoord][ycoord-1].Explored == 1:
                speedrun(xcoord, ycoord-1, maze[xcoord][ycoord].ShortestPath)
            if maze[xcoord][ycoord].WallSouth == 0 and maze[xcoord][ycoord+1].Explored == 1:
                speedrun(xcoord, ycoord+1, maze[xcoord][ycoord].ShortestPath)
            if maze[xcoord][ycoord].WallEast == 0 and maze[xcoord+1][ycoord].Explored == 1:
                speedrun(xcoord+1, ycoord, maze[xcoord][ycoord].ShortestPath)
            if maze[xcoord][ycoord].WallWest == 0 and maze[xcoord-1][ycoord].Explored == 1:
                speedrun(xcoord-1, ycoord, maze[xcoord][ycoord].ShortestPath)
#generate_directions
#inputs:
#xcoord: xcoordinate of the current square
#ycoord: ycoordinate of the current sqaure
#output: optimal list of directions for the mouse
def generate_directions(xcoord, ycoord):
    #placeholder numbers
    north = 256
    south = 256
    east = 256
    west = 256

    #if the current square is not the start
    if maze[xcoord][ycoord].Start == 0:
        #checks the shortest path of the immediate squares around the current sqaure 
        if maze[xcoord][ycoord].WallNorth == 0 and ycoord > 0:
            if maze[xcoord][ycoord-1].Explored == 1:
                north = maze[xcoord][ycoord-1].ShortestPath
        if maze[xcoord][ycoord].WallSouth == 0 and ycoord < 3:
            if maze[xcoord][ycoord+1].Explored == 1:
                south = maze[xcoord][ycoord+1].ShortestPath
        if maze[xcoord][ycoord].WallEast == 0 and  xcoord < 3:
            if maze[xcoord+1][ycoord].Explored == 1:
                east = maze[xcoord+1][ycoord].ShortestPath
        if maze[xcoord][ycoord].WallWest == 0 and xcoord > 0:
            if maze[xcoord-1][ycoord].Explored == 1:
                west = maze[xcoord-1][ycoord].ShortestPath
                
        #compares the shortest route of the immediate surrounding sqaures and generates a direction
        if north <= south and north <= west and north <= east:
            directions[maze[xcoord][ycoord-1].ShortestPath] = 'south'
            generate_directions(xcoord,ycoord-1)
        elif south <= north and south <= west and south <= east:
            directions[maze[xcoord][ycoord+1].ShortestPath] = 'north'
            generate_directions(xcoord,ycoord+1)
        elif east <= south and east <= west and east <= north:
            directions[maze[xcoord+1][ycoord].ShortestPath] = 'west'
            generate_directions(xcoord+1,ycoord)
        elif west <= south and west <= north and west <= east:
            directions[maze[xcoord-1][ycoord].ShortestPath] = 'east'
            generate_directions(xcoord-1,ycoord)
    
#generate_instructions
#inputs:
#xcoord: xcoordinate of the current sqaure
#ycoord: ycoordinate of the current sqaure
#ouput: list of motor instructions
def generate_instructions(xcoord,ycoord):
    #loops through the complete list of directions
    for i in range(maze[xcoord][ycoord].ShortestPath):
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
