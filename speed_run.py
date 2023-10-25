def speedrun(xcoord, ycoord, currpath):
    if maze[xcoord][ycoord].ShortestPath > currpath+1:
        if maze[xcoord][ycoord].Start == 1:
            maze[xcoord][ycoord].ShortestPath = 0
        
        else:
            maze[xcoord][ycoord].ShortestPath = currpath+1
            
        if maze[xcoord][ycoord].Finish == 0:
            if maze[xcoord][ycoord].WallNorth == 0 and maze[xcoord][ycoord-1].Explored == 1:
                speedrun(xcoord, ycoord-1, maze[xcoord][ycoord].ShortestPath)
            
            if maze[xcoord][ycoord].WallSouth == 0 and maze[xcoord][ycoord+1].Explored == 1:
                speedrun(xcoord, ycoord+1, maze[xcoord][ycoord].ShortestPath)
        
            if maze[xcoord][ycoord].WallEast == 0 and maze[xcoord+1][ycoord].Explored == 1:
                speedrun(xcoord+1, ycoord, maze[xcoord][ycoord].ShortestPath)
        
            if maze[xcoord][ycoord].WallWest == 0 and maze[xcoord-1][ycoord].Explored == 1:
                speedrun(xcoord-1, ycoord, maze[xcoord][ycoord].ShortestPath)
            
def generate_directions(xcoord, ycoord):
    #placeholder numbers
    north = 99
    south = 99
    east = 99
    west = 99
    
    if maze[xcoord][ycoord].Start == 0:
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
    
#straight = 0
#turn left = 1
#turn right = 2
def generate_instructions(xcoord,ycoord):
    for i in range(maze[xcoord][ycoord].ShortestPath):
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
