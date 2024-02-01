"""
File:           discover.py
Author:         Avion Lowery
Date (Start):   10/20/23
Date (Update):  1/26/24
Date (Done):
Email:          alowery1@umbc.edu or avion.m.lowery@gmail.com
Description:    This file will simulate the bot traversing to the center of the maze through terminal
"""
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

    print("\nFLOOD FILL ALGORITHM\n")

    bot_map_obj = bot.bot_map
    bot_map = bot_map_obj.map
    # Starting location of bot (5, 5) with seed = "random"
    x, y = bot_map_obj.get_bot_loc()
    """Assume it's in position to go straight from the start # Orientation Matters!!!"""
    distance = bot_map[x][y].get_distance()
    """Can change to recursion: f(org_x, org_y, dir:int, dest_found/distance)"""
    while distance != 0:
        possible_dir = []

        north, south, west, east = bot_map[x][y].get_walls()

        # Analyze choices:
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
        """
        Determine a direction by randomly selecting between two (until orientation is an added attribute of bot
        class). If you do this, make sure there is a maze to test this orientation attribute thoroughly
            - In reality, we would have a gyro or something to indicate the bot's orientation thus, that
            would be a factor in this decision        
                
            Solution: Handle orientation within the code for the hardware
            Orientation takes time -> changing direction from what you're doing takes time -> thus, instead of
            prioritizing straightness in the code (and recoding a bunch), simply prioritize not going in a different
            direction than what you did before. 
        """

        dir_to_go = random.choice(possible_dir)
        # Printing output to see bot's value and bot's map distance values
        for star in string_stars:
            print(star, end="")
        print()

        for i in range(DEFAULT_SIZE):
            for j in range(DEFAULT_SIZE):
                num = bot_map[i][j].get_distance()
                str_num = str(num)
                # Color to match the location color to track easier
                if (x, y) == (i, j):
                    if len(str_num) == 1:
                        print(fg.red + f" {str_num}" + Colors.reset, end='     ')
                    else:
                        print(fg.red + str(num) + Colors.reset, end='     ')
                else:
                    if len(str_num) == 1:
                        print(f" {str_num}", end='     ')
                    else:
                        print(num, end='     ')
            print()

        # Printing out x and y locations
        print(Colors.bold, end='')
        print("Location: " + fg.red + f"{(x, y)}" + Colors.reset)
        print(Colors.bold, end='')

        # Printing out walls in a more readable format
        north, south, west, east = bot_map[x][y].get_walls()
        dir_list = []
        if north:
            dir_list.append("North")
        if south:
            dir_list.append("South")
        if west:
            dir_list.append("West")
        if east:
            dir_list.append("East")

        if not dir_list:
            print("Walls: None")
        else:
            print(f"Walls: {dir_list}")

        # Printing out directions in a more readable format
        if not possible_dir:
            print("Directions possible: None")
        else:
            print(f"Directions possible: {possible_dir}")

        # Printing distance
        print("Distance: " + fg.red + f"{distance}" + Colors.reset)

        # Print the direction in more readable format
        print(f"Direction to go: {dir_to_go}")

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

    # Printing output to see bot's value and bot's map distance values
    for star in string_stars:
        print(star, end="")
    print()

    for i in range(DEFAULT_SIZE):
        for j in range(DEFAULT_SIZE):
            num = bot_map[i][j].get_distance()
            str_num = str(num)
            # Color to match the location color to track easier
            if (x, y) == (i, j):
                if len(str_num) == 1:
                    print(fg.red + f" {str_num}" + Colors.reset, end='     ')
                else:
                    print(fg.red + str(num) + Colors.reset, end='     ')
            else:
                if len(str_num) == 1:
                    print(f" {str_num}", end='     ')
                else:
                    print(num, end='     ')
        print()

    # Printing out x and y locations
    print("Location: " + fg.red + f"{(x, y)}" + Colors.reset)

    # Printing out walls in a more readable format
    north, south, west, east = bot_map[x][y].get_walls()
    dir_list = []
    if north:
        dir_list.append("North")
    if south:
        dir_list.append("South")
    if west:
        dir_list.append("West")
    if east:
        dir_list.append("East")

    if not dir_list:
        print("Walls: None")
    else:
        print(f"Walls: {dir_list}")

    # Printing distance
    print("Distance: " + fg.red + f"{distance}" + Colors.reset)


"""Make sure to wait or sleep before the bot goes back to try to find the start"""

if __name__ == "__main__":
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

    # Run the flood fill algorithm
    run_flood_algo(bot_1, maze_1)

    # Run the depth-first search fill algorithm
    # run_depth_search_algo(bot_1, maze_1)

    # Run the whole maze algorithm
    run_whole_maze_algo(bot_1, maze_1)

    # SpeedRun
    speedrun(startx, starty, 0, bot_map_obj)  # call from starting square with curr-path 0

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
        print("    ----------------------------------------------")

    directions = ['X'] * bot_map_obj[2, 2].shortest_route
    instructions = ['X'] * bot_map_obj[2, 2].shortest_route

    generate_directions(2, 2, bot_map_obj, directions)
    generate_instructions(2, 2, bot_map_obj, directions, instructions)

    # prints shortest path of each square in the maze

    print(instructions)
