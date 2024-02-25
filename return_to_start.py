"""
File:           return-to-start.py
Author:         Avion Lowery
Date (Start):   11/29/23
Date (Update):  2/25/24
Email:          alowery1@umbc.edu or avion.m.lowery@gmail.com
Description:    This file will simulate the bot traversing back from the center to either the
                start of the maze or seeing all the maze through the terminal
"""
# import os.path
from Map import *
from Colors import *
from enum import Enum

# Constants
END = "end"
NOT_END = ""
NEWLINE = "\n"
# FILENAME_OUTPUT = "Flood_Whole_Explored.txt"
# FILENAME_OUTPUT = "Flood_Whole.txt"
# FILENAME_OUTPUT = "Flood_DPS.txt"
FILENAME_OUTPUT = "MM23_log.txt"


class Direction(Enum):
    """
    Probably a better way to indicate directions rather than using enumeration but
    used in algorithms for logic in directions uses
    """
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


def run_depth_search_algo(bot, maze):
    """
    This is where the Depth First Search algorithm and the arithmetic behind it is housed Depth-first search,
    bot goes -> intersection -> random direction -- if deadened --> go back to intersection -> repeat

    :param bot: The bot object
    :param maze: the maze object (of the actual maze)
    :return: None(for now)
    """
    string_depth_title = "\nRUN DEPTH SEARCH ALGORITHM\n"
    # print(string_depth_title)
    write_to_file(string_depth_title + NEWLINE)

    ###############################    Algorithm Set Up     ###############################

    bot_map_obj = bot.bot_map
    bot_map = bot_map_obj.map
    # Starting location of bot at a destination square
    x, y = bot_map_obj.get_bot_loc()
    # Add backtracking variables
    backtrack_dir = ""
    backtracking = False
    backtracked = False
    index_last_intersection = 0
    possible_dir = []
    # Format for intersections list: (x,y coordinate of the intersection, backtrack_directions list)
    intersections = []
    dir_to_go = ""

    """
    If the bot stops when it arrives in the destination square pointing away from the exit of the destination 
    squares then rotate the bot 180 degrees.
    """
    """Enter Code for checking orientation + if it's not in the right orientation, then change it"""
    """Assume it's in position to go straight from the start #Orientation Matters!!!"""

    ###############################    Bot's Maze Logic     ###############################

    while unexplore(bot_map) and not bot_map[x][y].get_start():
        """ Possibility -> Implement this using recursion for every _intersection_ you reach 
            Base case is the while loop condition """

        north, south, west, east = bot_map[x][y].get_walls()
        # move - boolean flag - whenever the bot moves to another square, this turns true
        move = False

        # Determine if you're at a deadend here
        if not backtracking:

            # Toggling whether you're at a deadend or not
            if (north, south, west, east).count(True) == 3:
                backtracking = True

        # If you aren't backtracking as a result of reaching a deadend, continue normally
        if backtracking:
            # Only extract the direction if it exists
            if intersections[index_last_intersection][1]:
                dir_to_go = intersections[index_last_intersection][1].pop()

            # If the direction doesn't exist -> potential intersection was actually a deadend
            #   thus pop off the last (empty) intersection tuple and then extract the one that exists (before the empty)
            else:
                # Popped off the last intersection
                intersections.pop()
                index_last_intersection = len(intersections) - 1
                dir_to_go = intersections[index_last_intersection][1].pop()

            # No more directions to go
            if not intersections[index_last_intersection][1]:
                backtracking = False
                backtrack_dir = ""

                # Block off the wall that led to the deadend by making an invisible wall
                x_block, y_block = intersections[index_last_intersection][0]
                string = ""
                if dir_to_go == Direction.UP.name:
                    bot_map[x_block][y_block].set_south(True)
                    string = "South"
                elif dir_to_go == Direction.DOWN.name:
                    bot_map[x_block][y_block].set_north(True)
                    string = "North"
                elif dir_to_go == Direction.RIGHT.name:
                    bot_map[x_block][y_block].set_west(True)
                    string = "West"
                elif dir_to_go == Direction.LEFT.name:
                    bot_map[x_block][y_block].set_east(True)
                    string = "East"

                # ? Kinda useless since you should never be on that side of the wall
                # dir_tuple = bot_map[x_block][y_block].get_walls()
                # x_y_coor = x_block, y_block
                # bot_map_obj.check_set_walls(dir_tuple,
                #                             x_y_coor)

                # Indicate to the user you've added an invisible wall (because you most likely went through it
                # or at least it seems that way in the output)
                # print(NEWLINE +
                #       " Added invisible wall at location " + fg.green + f"({x_block, y_block})" + Colors.reset +
                #       f" with wall at " + fg.green + f"{string}" + Colors.reset +
                #       NEWLINE + Colors.bold)
                # write_to_file(NEWLINE +
                #               f" Added invisible wall at location ({x_block, y_block}) with wall at {string}" +
                #               NEWLINE)

                # Popped off the last intersection
                intersections.pop()
                index_last_intersection = len(intersections) - 1
                # boolean variable for backtracking to control when to start looking at a backtracked direction
                backtracked = True

        else:
            possible_dir = []

            # Analyze choices:
            if -1 < (x - 1) and not north and Direction.UP.name != backtrack_dir:
                possible_dir.append(Direction.UP.name)
            if (x + 1) < DEFAULT_SIZE and not south and Direction.DOWN.name != backtrack_dir:
                possible_dir.append(Direction.DOWN.name)
            if -1 < (y - 1) and not west and Direction.LEFT.name != backtrack_dir:
                possible_dir.append(Direction.LEFT.name)
            if (y + 1) < DEFAULT_SIZE and not east and Direction.RIGHT.name != backtrack_dir:
                possible_dir.append(Direction.RIGHT.name)

            # Prioritize unexplored/filtered results (another constraint is to prevent destination repeats)
            unexplore_squares = []
            if Direction.UP.name in possible_dir and not bot_map[x - 1][y].get_explore():
                if bot_map[x - 1][y].distance:
                    unexplore_squares.append(Direction.UP.name)
            if Direction.DOWN.name in possible_dir and not bot_map[x + 1][y].get_explore():
                if bot_map[x + 1][y].distance:
                    unexplore_squares.append(Direction.DOWN.name)
            if Direction.LEFT.name in possible_dir and not bot_map[x][y - 1].get_explore():
                if bot_map[x][y - 1].distance:
                    unexplore_squares.append(Direction.LEFT.name)
            if Direction.RIGHT.name in possible_dir and not bot_map[x][y + 1].get_explore():
                if bot_map[x][y + 1].distance:
                    unexplore_squares.append(Direction.RIGHT.name)

            if unexplore_squares:
                dir_to_go = random.choice(unexplore_squares)
            else:
                dir_to_go = random.choice(possible_dir)

            # Intersection storage logic

            # Analyze whether you are at an intersection and do not make a new entry if it's the most recent entry
            if len(possible_dir) > 1 and (not intersections or (x, y) != intersections[index_last_intersection][0]):
                list_intersection = [(x, y), []]
                intersections.append(list_intersection)
                index_last_intersection = len(intersections) - 1

        # print_explore_outputs(bot_map, x, y)
        # write_explore_outputs(bot_map, x, y)

        # print_info(bot_map, x, y, possible_dir, 0, dir_to_go, NOT_END)
        # write_info(bot_map, x, y, possible_dir, 0, dir_to_go, NOT_END)

        ###############################    Actual Maze Interaction     ###############################

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
                move = True

            # If you hit the north wall -> update the north wall on the bot's map
            else:
                bot_map[x][y].set_north(north_maze)
                dir_tuple = bot_map[x][y].get_walls()
                x_y_coor = x, y
                bot_map_obj.check_set_walls(dir_tuple, x_y_coor)

        # DIRECTION = DOWN
        elif dir_to_go == Direction.DOWN.name:
            # If you don't hit the south wall -> move to that location in the algorithm
            if not south_maze:
                x += 1
                bot.move(x, y, maze)
                move = True

            # If you hit the south wall -> update the south wall on the bot's map
            else:
                bot_map[x][y].set_south(south_maze)
                dir_tuple = bot_map[x][y].get_walls()
                x_y_coor = x, y
                bot_map_obj.check_set_walls(dir_tuple, x_y_coor)

        # DIRECTION = LEFT
        elif dir_to_go == Direction.LEFT.name:
            # If you don't hit the west wall -> move to that location in the algorithm
            if not west_maze:
                y -= 1
                bot.move(x, y, maze)
                move = True

            # If you hit the west wall -> update the west wall on the bot's map
            else:
                bot_map[x][y].set_west(west_maze)
                dir_tuple = bot_map[x][y].get_walls()
                x_y_coor = x, y
                bot_map_obj.check_set_walls(dir_tuple, x_y_coor)

        # DIRECTION = RIGHT
        elif dir_to_go == Direction.RIGHT.name:
            # If you don't hit the east wall -> move to that location in the algorithm
            if not east_maze:
                y += 1
                bot.move(x, y, maze)
                move = True

            # If you hit the west wall -> update the west wall on the bot's map
            else:
                bot_map[x][y].set_east(east_maze)
                dir_tuple = bot_map[x][y].get_walls()
                x_y_coor = x, y
                bot_map_obj.check_set_walls(dir_tuple, x_y_coor)

        # Backtracking storage logic
        if move and not backtracking:
            # This is needed to prevent adding a direction right after backtracking is over (in if a statement of
            # backtracking = False)
            if not backtracked:
                # Prevent directions of going backwards
                if dir_to_go == Direction.UP.name:
                    backtrack_dir = Direction.DOWN.name
                elif dir_to_go == Direction.DOWN.name:
                    backtrack_dir = Direction.UP.name
                elif dir_to_go == Direction.RIGHT.name:
                    backtrack_dir = Direction.LEFT.name
                elif dir_to_go == Direction.LEFT.name:
                    backtrack_dir = Direction.RIGHT.name
                intersections[index_last_intersection][1].append(backtrack_dir)

                # 1. Recheck intersection list that recent "intersections" are actual intersection -> Notes.txt
                ntrsc_ndx = 0
                while ntrsc_ndx < len(intersections):
                    bot_x, bot_y = intersections[ntrsc_ndx][0]
                    if not bot_map[bot_x][bot_y].get_walls().count(True) < 2:
                        pop_intersection = intersections.pop(ntrsc_ndx)
                        intersections[ntrsc_ndx - 1][1] = intersections[ntrsc_ndx - 1][1] + pop_intersection[1]
                        index_last_intersection = len(intersections) - 1
                    else:
                        ntrsc_ndx += 1
            else:
                backtracked = False

    # print_explore_outputs(bot_map, x, y)
    write_explore_outputs(bot_map, x, y)

    # print_info(bot_map, x, y, possible_dir, 0, dir_to_go, END)
    write_info(bot_map, x, y, possible_dir, 0, dir_to_go, END)


def run_whole_maze_algo(bot, maze):
    """
    This is where the Whole Maze algorithm and the arithmetic behind it is housed whole-maze is similar to
    depth-first search...We want to search as many possible paths and ideally get back to the start

    Looks for intersection and keeps looking for unexplored mazes

    :param bot: The bot object
    :param maze: The maze object (of the actual maze)
    :return: None(for now)
    """

    # Other approaches are in Notes.txt
    # 4th Approach (Difficulty?): Reverse Flood Search - looking for the next unexplored square
    # 1. __Scan__ the maze for unexplored squares (coordinates [to save memory rather than the object itself])
    # and __store__ to a (tuple) list. [(x,y), (x1,y1), ... ,(x_n,y_n)]
    # 2. Randomly __choose__ a coordinate from the tuple list
    #    a. My hope is the randomness will choose squares spread out, thus increasing the chance of hitting
    #    more unexplored squares without focusing on them.
    # 3. __Flood__ Maze with new numbers targeted at the randomly chosen coordinates
    # 4. Repeat steps 1-3 until all unexplored squares are found.

    string_whole_title = "\nRUN WHOLE MAZE ALGORITHM\n"
    # print(string_whole_title)
    write_to_file(string_whole_title + NEWLINE)

    ###############################    Algorithm Set Up     ###############################

    bot_map_obj = bot.bot_map
    bot_map = bot_map_obj.map
    # Starting location of the bot is the destination square it is at flood fill algo: (8, 7)
    x, y = bot_map_obj.get_bot_loc()
    """Assume it's in position to go straight from the start # Orientation Matters!!!"""
    tuple_list = []

    # Step 1: Scan and Store
    ndx = 0
    for i in range(DEFAULT_SIZE):
        for j in range(DEFAULT_SIZE):
            if not bot_map[i][j].get_explore() and not bot_map[i][j].get_walls().count(True) == 4:
                tuple_list.append([(i, j), ndx])
                ndx += 1

    """
    If the bot stops when it arrives in the destination square pointing away from the exit of the destination 
    squares then rotate the bot 180 degrees.
    """
    """Enter Code for checking orientation + if it's not in the right orientation, then change it"""
    """Assume it's in position to go straight from the start #Orientation Matters!!!"""

    ###############################    Bot's Maze Logic     ###############################
    """ Maybe use boolean flag instead of two "bot_map[x][y].get_start()" or a more "code-y" was to do it """
    while tuple_list and not bot_map[x][y].get_start():
        # Step 2: Choose
        coor, ndx_2_pop = random.choice(tuple_list)
        tuple_list.pop(ndx_2_pop)

        # Step 3: Flood
        flood(bot_map, coor)
        # Gather the distance number after you've flooded the maze with new distance numbers
        distance = bot_map[x][y].get_distance()

        dir_to_go = ""

        """Can change to recursion: f(org_x, org_y, dir:int, dest_found/distance)"""
        while distance != 0 and not bot_map[x][y].get_start():
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
            # Update distance numbers so that they correspond to where the bot can actually go
            if not possible_dir:
                bot_map_obj.set_distance_nums(x, y)
                # print(Colors.bold + NEWLINE + fg.green + "Had to update distance numbers due to not having any "
                #                                          "possible direction" + Colors.reset + NEWLINE)
                # write_to_file(NEWLINE + "Had to update distance numbers due to not having any "
                #                         "possible direction" + NEWLINE + NEWLINE)
            else:
                dir_to_go = random.choice(possible_dir)

            # print_distance_outputs(bot_map, x, y)
            # print_explore_outputs(bot_map, x, y)
            # write_distance_outputs(bot_map, x, y)
            # write_explore_outputs(bot_map, x, y)

            # print_info(bot_map, x, y, possible_dir, distance, dir_to_go, NOT_END)
            # write_info(bot_map, x, y, possible_dir, distance, dir_to_go, NOT_END)

            ###############################    Actual Maze Interaction     ###############################

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
    # print_explore_outputs(bot_map, x, y)
    # write_distance_outputs(bot_map, x, y)
    write_explore_outputs(bot_map, x, y)

    # print_info(bot_map, x, y, [], distance, dir_to_go, END)
    write_info(bot_map, x, y, [], 0, "", END)

    """Make sure to wait or sleep before the bot goes back to try to find the start"""


def unexplore(map_obj):
    """
    This will determine whether there are still unexplored squares within the maze.

    :param map_obj: Bot's map object (Bot (Map())
    :return: true if there are still unexplored squares and false if there isn't (bool)
    """
    # You may be able to dynamically shorten the length and width of the maze you're looking at
    # Once you find at least 1 unexplored square, immediately return True.
    for i in range(DEFAULT_SIZE):
        for j in range(DEFAULT_SIZE):
            if not map_obj[i][j].get_explore():
                return True
    return False


def flood(map_obj, coor):
    """
    This will re-flood or replace the distance numbers with the proper ones for the change
    in destination square.

    :param map_obj: Bot's map object (Bot(Map())
    :param coor: x,y coordinate that is your destination now
    :return: None
    """
    dest_x, dest_y = coor

    # Iterate around the destination square until all squares are flooded with new values
    for row in range(DEFAULT_SIZE):
        for col in range(DEFAULT_SIZE):
            distance = abs(row - dest_x) + abs(col - dest_y)
            map_obj[row][col].set_distance(distance)


def print_distance_outputs(map_obj, _x, _y):
    # Printing output to see bot's value and bot's map distance values
    print(Colors.bold, end='')
    for star in string_stars:
        print(star, end="")
    print()

    for i in range(DEFAULT_SIZE):
        for j in range(DEFAULT_SIZE):
            num = map_obj[i][j].get_distance()
            str_num = str(num)
            # Color to match the location color to track easier
            if (_x, _y) == (i, j):
                print(Colors.bold, end='')
                if len(str_num) == 1:
                    print(fg.red + f" {str_num}" + Colors.reset, end='     ')
                else:
                    print(fg.red + str(num) + Colors.reset, end='     ')
                print(Colors.bold, end='')
            else:
                print(Colors.bold, end='')
                if len(str_num) == 1:
                    print(f" {str_num}", end='     ')
                else:
                    print(num, end='     ')
                print(Colors.bold, end='')
        print()


def print_explore_outputs(map_obj, _x, _y):
    print(Colors.bold, end='')
    for star in string_stars:
        print(star, end="")
    print()

    for i in range(DEFAULT_SIZE):
        for j in range(DEFAULT_SIZE):
            explore = map_obj[i][j].is_explore
            # E = explored square
            if explore:
                print(Colors.bold, end='')
                if (i, j) == (_x, _y):
                    print(fg.red + "E" + Colors.reset, end='     ')
                else:
                    print("E", end='     ')
                print(Colors.bold, end='')
            # U = unexplored square
            else:
                print(Colors.bold, end='')
                if (i, j) == (_x, _y):
                    print(fg.red + "U" + Colors.reset, end='     ')
                else:
                    print("U", end='     ')
                print(Colors.bold, end='')
        print()


def print_info(map_obj, _x, _y, poss_dir, dist, dir_go, end_or_not):
    # Printing out x and y locations
    print(Colors.bold, end='')
    print("Location: " + fg.red + f"{(_x, _y)}" + Colors.reset)

    # Printing out walls in a more readable format
    north, south, west, east = map_obj[_x][_y].get_walls()
    dir_list = []
    if north:
        dir_list.append("North")
    if south:
        dir_list.append("South")
    if west:
        dir_list.append("West")
    if east:
        dir_list.append("East")

    print(Colors.bold, end='')
    if not dir_list:
        print("Walls: None")
    else:
        print(f"Walls: {dir_list}")

    if not end_or_not == END:

        # Printing out possible directions in a more readable format
        if not poss_dir:
            print("Directions possible: None")
        else:
            print(f"Directions possible: {poss_dir}")

        # Printing distance
        print("Distance: " + fg.red + f"{dist}" + Colors.reset)

        # Print the direction to go in more readable format
        print(Colors.bold, end='')
        if dir_go:
            print(f"Direction to go: {dir_go}")
        else:
            print("There was no possible direction to go")


def write_distance_outputs(_map, _x, _y):
    # Printing output to see bot's value and bot's map distance values
    for star in string_stars:
        write_to_file(star)
    write_to_file(NEWLINE)

    for i in range(DEFAULT_SIZE):
        for j in range(DEFAULT_SIZE):
            num = _map[i][j].get_distance()
            str_num = str(num)
            # Color to match the location color to track easier
            if (_x, _y) == (i, j):
                if len(str_num) == 1:
                    write_to_file(f" {str_num}" + '     ')
                else:
                    write_to_file(str(num) + '     ')
            else:
                if len(str_num) == 1:
                    write_to_file(f" {str_num}" + '     ')
                else:
                    write_to_file(str_num + '     ')
        write_to_file(NEWLINE)


def write_explore_outputs(_map, _x, _y):
    # Printing output to see bot's value and bot's map distance values
    for star in string_stars:
        write_to_file(star)
    write_to_file(NEWLINE)

    for i in range(DEFAULT_SIZE):
        for j in range(DEFAULT_SIZE):
            explore = _map[i][j].is_explore
            # E = explored square
            if explore:
                if (i, j) == (_x, _y):
                    write_to_file("E" + '     ')
                else:
                    write_to_file("E" + '     ')
            # U = unexplored square
            else:
                if (i, j) == (_x, _y):
                    write_to_file("U" + '     ')
                else:
                    write_to_file("U" + '     ')
        write_to_file(NEWLINE)


def write_info(_map, _x, _y, poss_dir, dist, dir_go, end_or_not):
    # Printing out x and y locations
    write_to_file(f"Location: {(_x, _y)}" + NEWLINE)

    # Printing out walls in a more readable format
    north, south, west, east = _map[_x][_y].get_walls()
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
        write_to_file("Walls: None" + NEWLINE)
    else:
        write_to_file(f"Walls: {dir_list}" + NEWLINE)

    if not end_or_not == END:

        # Printing out possible directions in a more readable format
        if not poss_dir:
            write_to_file("Directions possible: None" + NEWLINE)
        else:
            write_to_file(f"Directions possible: {poss_dir}" + NEWLINE)

        # Printing distance
        write_to_file(f"Distance: {dist}" + NEWLINE)

        # Print the direction to go in more readable format
        if dir_go:
            write_to_file(f"Direction to go: {dir_go}" + NEWLINE)
        else:
            write_to_file("There was no possible direction to go" + NEWLINE)


def write_to_file(string_input):
    # Recording data
    # num = 0
    # while os.path.exists(f"output{num}"):
    #     num += 1
    # file = open(f"output{num}", "w")
    file = open(FILENAME_OUTPUT, "a")
    file.write(string_input)
    file.close()
