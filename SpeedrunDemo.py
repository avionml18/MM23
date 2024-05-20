# speedrun
# inputs:
# x-coord: x-coordinate of current square
# y-coord: y-coordinate of current square
# currpath: shortest path to the current square
# output: updated ShortestPath value of all explored squares
from Map import *

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
    for i in range(len(directions)):
        # generates list of motor instructions
        # straight = 0
        # turn left = 1
        # turn right = 2
        # Note: These will be changed to match proper motor control syntax
        if i == 0:
            instructions[i] = 'f'
        else:
            if directions[i] == directions[i - 1]:
                instructions[i] = 'f'
            elif directions[i] == 'north' and directions[i - 1] == 'west':
                instructions[i] = 'r'
            elif directions[i] == 'north' and directions[i - 1] == 'east':
                instructions[i] = 'l'
            elif directions[i] == 'south' and directions[i - 1] == 'east':
                instructions[i] = 'r'
            elif directions[i] == 'south' and directions[i - 1] == 'west':
                instructions[i] = 'l'
            elif directions[i] == 'east' and directions[i - 1] == 'north':
                instructions[i] = 'r'
            elif directions[i] == 'east' and directions[i - 1] == 'south':
                instructions[i] = 'l'
            elif directions[i] == 'west' and directions[i - 1] == 'south':
                instructions[i] = 'r'
            elif directions[i] == 'west' and directions[i - 1] == 'north':
                instructions[i] = 'l'


def new_directions(finishx, finishy, bot_map_obj):
    # global finishx, finishy, DEFAULT_SIZE, bot_map_obj
    for i in range(DEFAULT_SIZE):
        # for j in range(4):
        print(i, end=": ")
        for j in range(DEFAULT_SIZE):
            if (bot_map_obj[i, j].shortest_route) < 10:
                print(f" {bot_map_obj[i, j].shortest_route}", end='   |  ')
            elif (bot_map_obj[i, j].shortest_route) < 100:
                print(f" {bot_map_obj[i, j].shortest_route}", end='  |  ')
            else:
                print(f" {bot_map_obj[i, j].shortest_route}", end=' |  ')
        print()
        print("    ------------------------------------------------------------------------------------------")

    directions = ['X'] * bot_map_obj[finishx, finishy].shortest_route

    generate_directions(finishy, finishx, bot_map_obj, directions, len(directions)-1)
    startIndex = 0
    while directions[startIndex] == 'X':
        startIndex += 1
    directionsNew = ['X'] * (len(directions) - startIndex)
    for i in range(len(directions)-startIndex):
        directionsNew[i] = directions[startIndex+i]

    instructions = ['X'] * len(directionsNew)
    generate_instructions(finishy, finishx, bot_map_obj, directionsNew, instructions)

    # prints shortest path of each square in the maze

    print(directionsNew)
    print(instructions)

    i = 0
    j = 0
    dur = 1
    newinstructions = [0] * (len(instructions))
    durations = [0] * (len(instructions))
    while i < len(instructions):
        newinstructions[j] = instructions[i]
        while i+1 < len(instructions) and instructions[i+1] == newinstructions[j]:
            i += 1
            dur += 1
        durations[j] = dur
        dur = 1
        j += 1
        i += 1

    i = 0

    while i < len(newinstructions) and newinstructions[i] != 0:
        i+= 1

    newinstructionsfinalforreal = [0] * i
    durationsfinalforread = [0] * i

    i = 0
    while i < len(newinstructions) and newinstructions[i] != 0:
        newinstructionsfinalforreal[i] = newinstructions[i]
        durationsfinalforread[i] = durations[i]
        i+= 1

    print(newinstructionsfinalforreal)
    print(durationsfinalforread)
    i = 0
