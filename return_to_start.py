"""
File:           return-to-start.py
Author:         Avion Lowery
Date (Start):   11/29/23
Date (Update):  1/20/24
Date (Done):
Email:          alowery1@umbc.edu or avion.m.lowery@gmail.com
Description:    This file will simulate the bot traversing back from the center to either the
                start of the maze or seeing all the maze through terminal
"""
from Map import *
from Colors import *
from discover import Direction

def run_depth_search_algo(bot, maze):
    """
    This is where the Depth First Search algorithm and the arithmetic behind it is housed Depth first search,
    bot goes -> intersection -> random direction -- if deadened --> go back to intersection -> repeat

    :param bot: the bot object
    :param maze: the maze object (of the actual maze)
    :return: None(for now)
    """

    print("\nRUN DEPTH SEARCH ALGORITHM\n")

    ###############################    Algorithm Set Up     ###############################

    bot_map_obj = bot.bot_map
    bot_map = bot_map_obj.map
    # Starting location of bot at a destination square
    x, y = bot_map_obj.get_bot_loc()
    # Add backtracking variable
    backtrack_dir = ""
    backtracking = False
    ctr_intersection = 0
    possible_dir = []
    intersections = []

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

        # Format for intersections list: (Square object of intersection, backtrack_directions list)
        """Do I only use the walls when I'm not backtracking"""
        north, south, west, east = bot_map[x][y].get_walls()

        # Determine if you're at a deadend here
        if not backtracking:
            ctr_deadend = 0
            if north:
                ctr_deadend += 1
            if south:
                ctr_deadend += 1
            if west:
                ctr_deadend += 1
            if east:
                ctr_deadend += 1

            # Toggling whether you're at a deadend or not
            if ctr_deadend == 3:
                backtracking = True

        # If you aren't backtracking as a result of reaching a deadend, continue normally
        if backtracking:
            dir_to_go = intersections[ctr_intersection][1].pop()

            # No more directions to go
            if not intersections[ctr_intersection][1]:
                backtracking = False
                backtrack_dir = ""

                # Block off the wall that led to the deadend by making an invisible wall
                x, y = intersections[ctr_intersection][0]
                string = ""
                if dir_to_go == Direction.UP.name:
                    bot_map[x][y].set_south(True)
                    string = "South"
                elif dir_to_go == Direction.DOWN.name:
                    bot_map[x][y].set_north(True)
                    string = "North"
                elif dir_to_go == Direction.RIGHT.name:
                    bot_map[x][y].set_west(True)
                    string = "West"
                elif dir_to_go == Direction.LEFT.name:
                    bot_map[x][y].set_east(True)
                    string = "East"

                # Indicate to the user you've added an invisible wall (because you most likely went through it
                # or at least it seems that way in the output)
                print("\n "
                      "Added invisible wall at location " + fg.green + f"({x, y})" + Colors.reset +
                      f" with wall at " + fg.green + f"{string}" + Colors.reset +
                      "\n")

                # Popped off the last intersection
                intersections.pop()
                ctr_intersection = len(intersections) - 1

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

            """
            Determine a direction by randomly selecting between two (until orientation is an added attribute of bot
                class). If you do this, make sure there is a maze to test this orientation attribute thoroughly
                  - In reality, we would have a gyro or something to indicate the bot's orientation thus, that
                    would be a factor in this decision        
            """

            # Prioritize unexplored/filtered results (another constraints is to prevent destination repeats)
            unexplore_squares = []
            if Direction.UP.name in possible_dir and not bot_map[x - 1][y].get_explore():
                if bot_map[x - 1][y].is_dest:
                    unexplore_squares.append(Direction.UP.name)
            if Direction.DOWN.name in possible_dir and not bot_map[x + 1][y].get_explore():
                if bot_map[x + 1][y].is_dest:
                    unexplore_squares.append(Direction.DOWN.name)
            if Direction.LEFT.name in possible_dir and not bot_map[x][y - 1].get_explore():
                if bot_map[x][y - 1].is_dest:
                    unexplore_squares.append(Direction.LEFT.name)
            if Direction.RIGHT.name in possible_dir and not bot_map[x][y + 1].get_explore():
                if bot_map[x][y + 1].is_dest:
                    unexplore_squares.append(Direction.RIGHT.name)

            if unexplore_squares:
                dir_to_go = random.choice(unexplore_squares)
            else:
                dir_to_go = random.choice(possible_dir)

            # Intersection storage logic

            # Analyze whether you are at an intersection
            if len(possible_dir) > 1:
                tuple_intersection = ((x, y), [])
                intersections.append(tuple_intersection)
                # If it's the first run, leave it as a zero for the first element
                ctr_intersection = len(intersections) - 1

            # Prevent direction of going backwards
            if dir_to_go == Direction.UP.name:
                backtrack_dir = Direction.DOWN.name
            elif dir_to_go == Direction.DOWN.name:
                backtrack_dir = Direction.UP.name
            elif dir_to_go == Direction.RIGHT.name:
                backtrack_dir = Direction.LEFT.name
            elif dir_to_go == Direction.LEFT.name:
                backtrack_dir = Direction.RIGHT.name

            intersections[ctr_intersection][1].append(backtrack_dir)

        # Printing output to see bot's explored value
        for star in string_stars:
            print(star, end="")
        print()

        for i in range(DEFAULT_SIZE):
            for j in range(DEFAULT_SIZE):
                explore = bot_map[i][j].is_explore
                # E = explored square
                if explore:
                    if (i, j) == (x, y):
                        print(fg.red + "E" + Colors.reset, end='     ')
                    else:
                        print("E", end='     ')
                # U = unexplored square
                else:
                    if (i, j) == (x, y):
                        print(fg.red + "U" + Colors.reset, end='     ')
                    else:
                        print("U", end='     ')
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

        # Printing out directions in a more readable format
        if not possible_dir:
            print("Directions possible: None")
        else:
            print(f"Directions possible: {possible_dir}")

        # Print the direction in more readable format
        print(f"Direction to go: {dir_to_go}")

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

    # Printing output to see bot's explored value
    for star in string_stars:
        print(star, end="")
    print()

    for i in range(DEFAULT_SIZE):
        for j in range(DEFAULT_SIZE):
            explore = bot_map[i][j].is_explore
            # E = explored square
            if explore:
                if (i, j) == (x, y):
                    print(fg.red + "E" + Colors.reset, end='     ')
                else:
                    print("E", end='     ')
            # U = unexplored square
            else:
                if (i, j) == (x, y):
                    print(fg.red + "U" + Colors.reset, end='     ')
                else:
                    print("U", end='     ')
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


def run_whole_maze_algo(bot, maze):
    """
    This is where the Whole Maze algorithm and the arithmetic behind it is housed whole-maze is similar to depth
    first search...We want to search as many possible paths and ideally get back to the start

    Looks for intersection and keeps looking for unexplored mazes

    :param bot: the bot object
    :param maze: the maze object (of the actual maze)
    :return: None(for now)
    """
    pass


def unexplore(map_obj):
    """
    This will determine whether there's still unexplored squares within the maze.

    :param map_obj: bot's map object (Bot(Map())
    :return: true if there are still unexplored squares and false if there isn't (bool)
    """
    # You may be able to dynamically shorten the length and width of the maze you're looking at
    # Once you find at least 1 unexplored square, immediately return True.
    for i in range(DEFAULT_SIZE):
        for j in range(DEFAULT_SIZE):
            if not map_obj[i][j].get_explore():
                return True
    return False
