# speedrun
# inputs:
# x-coord: x-coordinate of current square
# y-coord: y-coordinate of current square
# currpath: shortest path to the current square
# output: updated ShortestPath value of all explored squares
from motor1.1 import *
from time import sleep
from discover import *
#MUST BE COMPILED ON RPI, IMPORT WITHIN motor1.py WILL ERROR OUT

def speedrun(xcoord, ycoord, currpath, maze, direction, instruction):
    straight_weight = 1
    turn_weight = 2
    # base case to ensure the ShortestPath is bigger than the current path
    if maze[ycoord, xcoord].shortest_route > currpath + 1:
        # initialize shortest path to start (0)
        if maze[ycoord, xcoord].is_start == 1:
            maze[ycoord, xcoord].shortest_route = 0

        # every other square besides the start
        else:
            if instruction == "straight":
                maze[ycoord, xcoord].shortest_route = currpath + straight_weight
            elif instruction == "turn":
                maze[ycoord, xcoord].shortest_route = currpath + turn_weight
        # is the current square is not the finish...
        if maze[ycoord, xcoord].is_dest == 0:
            # checks each square around the current square and recalls the function
            if (not maze[ycoord, xcoord].w_north) and maze[ycoord - 1, xcoord].is_explore:
                if direction == "north":
                    speedrun(xcoord, ycoord - 1, maze[ycoord, xcoord].shortest_route, maze, "north", "straight")
                else:
                    speedrun(xcoord, ycoord - 1, maze[ycoord, xcoord].shortest_route, maze, "north", "turn")
            if (not maze[ycoord, xcoord].w_south) and maze[ycoord + 1, xcoord].is_explore:
                if direction == "south":
                    speedrun(xcoord, ycoord + 1, maze[ycoord, xcoord].shortest_route, maze, "south", "straight")
                else:
                    speedrun(xcoord, ycoord + 1, maze[ycoord, xcoord].shortest_route, maze, "south", "turn")
            if (not maze[ycoord, xcoord].w_east) and maze[ycoord, xcoord + 1].is_explore:
                if direction == "east":
                    speedrun(xcoord + 1, ycoord, maze[ycoord, xcoord].shortest_route, maze, "east", "straight")
                else:
                    speedrun(xcoord + 1, ycoord, maze[ycoord, xcoord].shortest_route, maze, "east", "turn")
            if (not maze[ycoord, xcoord].w_west) and maze[ycoord, xcoord - 1].is_explore:
                if direction == "west":
                    speedrun(xcoord - 1, ycoord, maze[ycoord, xcoord].shortest_route, maze, "west", "straight")
                else:
                    speedrun(xcoord - 1, ycoord, maze[ycoord, xcoord].shortest_route, maze, "west", "turn")


# generate_directions
# inputs:
# x-coord: x-coordinate of the current square
# y-coord: y-coordinate of the current square
# output: optimal list of directions for the mouse
def generate_directions(xcoord, ycoord, maze, directions, index):
    # placeholder numbers
    north = 256
    south = 256
    east = 256
    west = 256

    # if the current square is not the start
    if (maze[ycoord, xcoord].shortest_route > 0):
        # checks the shortest path of the immediate squares around the current square
        if maze[ycoord, xcoord].w_north == 0 and maze[ycoord - 1, xcoord].is_explore == 1:
            north = maze[ycoord - 1, xcoord].shortest_route
        if maze[ycoord, xcoord].w_south == 0 and maze[ycoord + 1, xcoord].is_explore == 1:
            south = maze[ycoord + 1, xcoord].shortest_route
        if maze[ycoord, xcoord].w_east == 0 and maze[ycoord, xcoord + 1].is_explore == 1:
            east = maze[ycoord, xcoord + 1].shortest_route
        if maze[ycoord, xcoord].w_west == 0 and maze[ycoord, xcoord - 1].is_explore == 1:
            west = maze[ycoord, xcoord - 1].shortest_route

        # compares the shortest route of the immediate surrounding squares and generates a direction
        if north <= south and north <= west and north <= east:
            directions[index] = 'south'
            generate_directions(xcoord, ycoord - 1, maze, directions, index-1)
        elif south <= north and south <= west and south <= east:
            directions[index] = 'north'
            generate_directions(xcoord, ycoord + 1, maze, directions, index-1)
        elif east <= south and east <= west and east <= north:
            directions[index] = 'west'
            generate_directions(xcoord + 1, ycoord, maze, directions, index-1)
        elif west <= south and west <= north and west <= east:
            directions[index] = 'east'
            generate_directions(xcoord - 1, ycoord, maze, directions, index-1)


# generate_instructions
# inputs:
# xcoord: xcoordinate of the current sqaure
# ycoord: ycoordinate of the current sqaure
# ouput: list of motor instructions
def generate_instructions(xcoord, ycoord, maze, directions, instructions):
    # loops through the complete list of directions
    duration = 1
    unit_dur = duration
    motors('h')
    for i in range(len(directions)):
        # generates list of motor instructions
        # straight = 0
        # turn left = 1
        # turn right = 2
        # Note: These will be changed to match proper motor control syntax
        if i == 0:
            instructions[i] = 0
        else:
            if directions[i] == directions[i - 1]:
                instructions[i] = 0
                duration = duration+unit_dur
            elif directions[i] == 'north' and directions[i - 1] == 'west':
                instructions[i] = 2
            elif directions[i] == 'north' and directions[i - 1] == 'east':
                instructions[i] = 1
            elif directions[i] == 'south' and directions[i - 1] == 'east':
                instructions[i] = 2
            elif directions[i] == 'south' and directions[i - 1] == 'west':
                instructions[i] = 1
            elif directions[i] == 'east' and directions[i - 1] == 'north':
                instructions[i] = 2
            elif directions[i] == 'east' and directions[i - 1] == 'south':
                instructions[i] = 1
            elif directions[i] == 'west' and directions[i - 1] == 'south':
                instructions[i] = 2
            elif directions[i] == 'west' and directions[i - 1] == 'north':
                instructions[i] = 1


        
        if instructions[i] == 1:
            if instructions[i - 1] == 0:
                print("Move forward for duration " + str(duration))
                motors('f')
                time.sleep(duration)
                duration = unit_dur
            print("Turn Left")
            motors('L', 1)

        if instructions[i] == 2:
            if instructions[i - 1] == 0:
                print("Move forward for duration " + str(duration))
                motors('f')
                time.sleep(duration)
                duration = unit_dur
            print("Turn Right")
            motors('R', 1)
    
    motors('s')
