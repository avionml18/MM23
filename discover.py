"""
File:           discover.py
Author:         Avion Lowery
Date (Start):   10/20/23
Date (Update):  4/27/24
Email:          alowery1@umbc.edu or avion.m.lowery@gmail.com
Description:    This file will simulate the bot traversing to the center of the maze through terminal
"""
import os.path
from Bot import *
from SpeedRun import *
from return_to_start import *


def run_flood_algo(bot, maze):
    """
    This is where the Flood-Fill algorithm and the arithmetic behind it is housed

    Flood-Fill Algo:
        Bot looks through all adjacent cells which aren't blocked by walls and choose the lowest distance values
        Turning take time thus if you have two choices, choose the one where the bot will not have to move much
        If run into a wall, update wall and distance values

    Flood-Fill Algorithm being used: Modified
    (There are better Flood-Fill Algorithms)

    :param bot: the bot object
    :param maze: the maze object (of the actual maze)
    :return: None(for now)
    """

    # Summary (in detail) of Flood-Fill Algo:
    #   Every time the mouse moves:
    #   Update the wall map
    #   Flood the maze with new distance values -> a Modified version = flood the necessary values
    #   Decide which neighboring cell has the lowest distance value
    #   Move to the neighboring cell with the lowest distance value

    string_flood_title = "\nFLOOD FILL ALGORITHM\n"
    # print(string_flood_title)
    write_to_file(string_flood_title + NEWLINE)

    ###############################    Algorithm Set Up     ###############################

    bot_map_obj = bot.bot_map
    bot_map = bot_map_obj.map
    # Starting location of bot (5, 5) with seed = "random"
    x, y = bot_map_obj.get_bot_loc()
    write_to_file(f"Starting location: ({x},{y})" + NEWLINE)
    """Assume it's in position to go straight from the start # Orientation Matters!!!"""
    distance = bot_map[x][y].get_distance()
    dir_to_go = ""

    ###############################    Bot's Maze Logic     ###############################

    while distance != 0:
        possible_dir = []
        north, south, west, east = bot_map[x][y].get_walls()

        # Analyze possible directions (based on distance numbers):
        if -1 < (x - 1) and not north:
            if bot_map_obj[x - 1, y].get_distance() < distance:
                possible_dir.append(Direction.UP.name)
        if (x + 1) < DEFAULT_SIZE and not south:
            if bot_map_obj[x + 1, y].get_distance() < distance:
                possible_dir.append(Direction.DOWN.name)
        if -1 < (y - 1) and not west:
            if bot_map_obj[x, y - 1].get_distance() < distance:
                possible_dir.append(Direction.LEFT.name)
        if (y + 1) < DEFAULT_SIZE and not east:
            if bot_map_obj[x, y + 1].get_distance() < distance:
                possible_dir.append(Direction.RIGHT.name)

        # Based on orientation determine if you have a direction to choose from the possible directions
        if bot.get_orientation() == Orientation.NORTH.value and Direction.UP.name in possible_dir:
            dir_to_go = Direction.UP.name
        elif bot.get_orientation() == Orientation.SOUTH.value and Direction.DOWN.name in possible_dir:
            dir_to_go = Direction.DOWN.name
        elif bot.get_orientation() == Orientation.WEST.value and Direction.LEFT.name in possible_dir:
            dir_to_go = Direction.LEFT.name
        elif bot.get_orientation() == Orientation.EAST.value and Direction.RIGHT.name in possible_dir:
            dir_to_go = Direction.RIGHT.name
        # If not, choose at random which direction to go
        else:
            dir_to_go = random.choice(possible_dir)

        # Printing output to see bot's value and bot's map distance values
        # print_distance_outputs(bot_map, x, y)
        # write_distance_outputs(bot_map, x, y)

        # print_info(bot_map, x, y, possible_dir, distance, dir_to_go, NOT_END)
        # write_info(bot_map, x, y, [], distance, dir_to_go, END)

        ###############################    Actual Maze Interaction     ###############################

        # Orientate the bot to properly go to it's next square
        # UP and NORTH
        if dir_to_go == Direction.UP.name and bot.get_orientation() != Orientation.NORTH.value:
            if bot.get_orientation() == Orientation.WEST.value:
                bot.turn_right()
            elif bot.get_orientation() == Orientation.EAST.value:
                bot.turn_left()
            elif bot.get_orientation() == Orientation.SOUTH.value:
                choice = random.choice((True, False))
                if choice:
                    bot.turn_right()
                    bot.turn_right()
                else:
                    bot.turn_left()
                    bot.turn_left()

        # DOWN and SOUTH
        elif dir_to_go == Direction.DOWN.name and bot.get_orientation() != Orientation.SOUTH.value:
            if bot.get_orientation() == Orientation.WEST.value:
                bot.turn_left()
            elif bot.get_orientation() == Orientation.EAST.value:
                bot.turn_right()
            elif bot.get_orientation() == Orientation.NORTH.value:
                choice = random.choice((True, False))
                if choice:
                    bot.turn_right()
                    bot.turn_right()
                else:
                    bot.turn_left()
                    bot.turn_left()

        # LEFT and WEST
        elif dir_to_go == Direction.LEFT.name and bot.get_orientation() != Orientation.WEST.value:
            if bot.get_orientation() == Orientation.NORTH.value:
                bot.turn_left()
            elif bot.get_orientation() == Orientation.SOUTH.value:
                bot.turn_right()
            elif bot.get_orientation() == Orientation.EAST.value:
                choice = random.choice((True, False))
                if choice:
                    bot.turn_right()
                    bot.turn_right()
                else:
                    bot.turn_left()
                    bot.turn_left()

        # RIGHT and EAST
        elif dir_to_go == Direction.RIGHT.name and bot.get_orientation() != Orientation.EAST.value:
            if bot.get_orientation() == Orientation.NORTH.value:
                bot.turn_right()
            elif bot.get_orientation() == Orientation.SOUTH.value:
                bot.turn_left()
            elif bot.get_orientation() == Orientation.WEST.value:
                choice = random.choice((True, False))
                if choice:
                    bot.turn_right()
                    bot.turn_right()
                else:
                    bot.turn_left()
                    bot.turn_left()

        # Look in the actual maze for walls
        north_maze, south_maze, west_maze, east_maze = maze.map[x][y].get_walls()

        # Then tell the bot where to go in the actual maze
        # DIRECTION = UP
        if dir_to_go == Direction.UP.name:
            # If you don't hit the north wall -> move to that location in the algorithm
            if not north_maze:
                # Go bot
                x -= 1
                bot.move(x, y, maze)

            # If you hit the north wall -> update the north wall on the bot's map
            else:
                bot_map[x][y].set_north(north_maze)
                dir_tuple = bot_map[x][y].get_walls()
                x_y_coor = x, y
                bot_map_obj.check_set_walls(dir_tuple, x_y_coor)

                # Update distance numbers for the bot and go again
                bot_map_obj.set_distance_nums(x, y)

        # DIRECTION = DOWN
        elif dir_to_go == Direction.DOWN.name:
            # If you don't hit the south wall -> move to that location in the algorithm
            if not south_maze:
                x += 1
                bot.move(x, y, maze)

            # If you hit the south wall -> update the south wall on the bot's map
            else:
                bot_map[x][y].set_south(south_maze)
                dir_tuple = bot_map[x][y].get_walls()
                x_y_coor = x, y
                bot_map_obj.check_set_walls(dir_tuple, x_y_coor)

                # Update distance numbers for the bot and go again
                bot_map_obj.set_distance_nums(x, y)

        # DIRECTION = LEFT
        elif dir_to_go == Direction.LEFT.name:
            # If you don't hit the west wall -> move to that location in the algorithm
            if not west_maze:
                y -= 1
                bot.move(x, y, maze)

            # If you hit the west wall -> update the west wall on the bot's map
            else:
                bot_map[x][y].set_west(west_maze)
                dir_tuple = bot_map[x][y].get_walls()
                x_y_coor = x, y
                bot_map_obj.check_set_walls(dir_tuple, x_y_coor)

                # Update distance numbers for the bot and go again
                bot_map_obj.set_distance_nums(x, y)

        # DIRECTION = RIGHT
        elif dir_to_go == Direction.RIGHT.name:
            # If you don't hit the east wall -> move to that location in the algorithm
            if not east_maze:
                y += 1
                bot.move(x, y, maze)

            # If you hit the west wall -> update the west wall on the bot's map
            else:
                bot_map[x][y].set_east(east_maze)
                dir_tuple = bot_map[x][y].get_walls()
                x_y_coor = x, y
                bot_map_obj.check_set_walls(dir_tuple, x_y_coor)

                # Update distance numbers for the bot and go again
                bot_map_obj.set_distance_nums(x, y)

        distance = bot_map[x][y].get_distance()
        """Not sure if we need this since you can't get out of the while loop without distance being equal to 0
        Propose solution: put this if statement outside the while loop and get rid of the if condidtion."""
        if distance == 0:
            bot_map[x][y].is_dest = True
            """When you find the destination square, you can populate the other walls
            and declare the other destination squares as explored."""

    # print_distance_outputs(bot_map, x, y)
    write_distance_outputs(bot_map, x, y)

    # print_info(bot_map, x, y, possible_dir, distance, dir_to_go, END)
    write_info(bot_map, x, y, [], distance, dir_to_go, END)


"""Make sure to wait or sleep before the bot goes back to try to find the start"""

if __name__ == "__main__":
    global finishx, finishy
    """ Things below this main will eventually be in the *driver.py" program. """

    # Make an instance of Map to represent the actual maze
    maze_1 = Map()
    maze_1.make_maze_map()

    # Make a bot instance to represent the bot itself
    bot_1 = Bot()
    # Set the bot's starting square to the same starting square in the maze
    # Make the bot's map by populating with the distance numbers
    bot_map_obj = bot_1.bot_map

    bot_map_obj.set_bot_loc(maze_1.get_bot_loc())
    is_maze = False
    bot_map_obj.make_starting_square(is_maze)
    startx, starty = maze_1.get_bot_loc()

    # Delete MM23_log.txt if it exists
    if os.path.exists("MM23_log.txt"):
        os.remove("MM23_log.txt")

    # Run the flood fill algorithm
    run_flood_algo(bot_1, maze_1)
    finishx, finishy = maze_1.get_bot_loc()

    # Run the whole maze algorithm
    run_whole_maze_algo(bot_1, maze_1)

    # Run the depth-first search fill algorithm
    # run_depth_search_algo(bot_1, maze_1)

    # SpeedRun

    string_depth_title = "\nSPEED RUN ALGORITHM\n"
    # print(string_depth_title)
    write_to_file(string_depth_title + '\n')

    speedrun(starty, startx, 0, bot_map_obj, "north", "straight")  # call from starting square with curr-path 0

    for i in range(DEFAULT_SIZE):
        # for j in range(4):
        # print(i, end=": ")
        write_to_file(str(i) + ": ")
        for j in range(DEFAULT_SIZE):
            if (bot_map_obj[i, j].shortest_route) < 10:
                # print(f" {bot_map_obj[i, j].shortest_route}", end='   |  ')
                write_to_file(f" {bot_map_obj[i, j].shortest_route}   |  ")
            elif (bot_map_obj[i, j].shortest_route) < 100:
                # print(f" {bot_map_obj[i, j].shortest_route}", end='  |  ')
                write_to_file(f" {bot_map_obj[i, j].shortest_route}  |  ")
            else:
                # print(f" {bot_map_obj[i, j].shortest_route}", end=' |  ')
                write_to_file(f" {bot_map_obj[i, j].shortest_route} |  ")
        # print()
        write_to_file(NEWLINE)
        # print("    ------------------------------------------------------------------------------------------")
        write_to_file(
            "    ------------------------------------------------------------------------------------------" + NEWLINE)
    directions = ['X'] * bot_map_obj[finishx, finishy].shortest_route

    generate_directions(finishy, finishx, bot_map_obj, directions, len(directions) - 1)
    startIndex = 0
    while directions[startIndex] == 'X':
        startIndex += 1
    directionsNew = ['X'] * (len(directions) - startIndex)
    for i in range(len(directions) - startIndex):
        directionsNew[i] = directions[startIndex + i]

    instructions = ['X'] * len(directionsNew)
    generate_instructions(finishy, finishx, bot_map_obj, directionsNew, instructions)

    # prints shortest path of each square in the maze

    # print(directionsNew)
    write_to_file(str(directionsNew) + NEWLINE)
    # print(instructions)
    write_to_file(str(instructions) + NEWLINE)
