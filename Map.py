"""
File:           Map.py
Author:         Avion Lowery
Date (Start):   10/20/23
Date (Update):  1/31/24
Date (Done):
Email:          alowery1@umbc.edu or loweryavion@gmail.com
Description:    This program will have the class Map for discover.py program.
"""

import random
from Square import *

# Default size has to greater than 2
# nxn -> Ex: DEFAULT_SIZE = 2 means 2x2 or only four squares (destination squares)
# CAN'T BE AN ODD NUMBER -> Mazes never are

# DEFAULT_SIZE = 4
# FILENAME = ""

DEFAULT_SIZE = 6
FILENAME = "maze1.txt"

# DEFAULT_SIZE = 8
# FILENAME = ""

# DEFAULT_SIZE = 16
# FILENAME = "maze2.txt"

string_stars = ['*' for i in range(DEFAULT_SIZE)] * 7

MAKE_WALLS_USER = False

# Consistent location of starting location and anywhere random is used (Depth First Search Algo)
# random.seed("random")
# Without an argv in seed(), it'll use the current system time
random.seed()


class Map:
    """
    This is where the map of the bot and where the user can choose to make a starting map are housed
    """

    def __init__(self, bool_t_f=False):
        # Default map -> Clean slate
        self.map = [[Square(bool_t_f) for i in range(DEFAULT_SIZE)] for i in range(DEFAULT_SIZE)]
        self.bot_loc_x, self.bot_loc_y = 0, 0

    def make_maze_map(self):
        """
        Method for making a simulated maze for the bot to traverse in.
        :return: None
        """
        is_maze = True
        self.make_starting_square(is_maze)
        self.make_out_walls()
        if MAKE_WALLS_USER:
            self.make_walls_user()
        else:
            self.make_walls_file()

    def make_bot_map(self):
        """
        Method for making a bot's maze that is used for maze solving and route choosing
        :return: None
        """
        self.make_distance_nums()
        self.make_out_walls()

    def make_distance_nums(self):
        """
        Filling in the distance numbers of the maze for the bot's map
        :return: None
        """

        max_dist_index = DEFAULT_SIZE - 1
        half_dist_index = DEFAULT_SIZE // 2
        curr_dist = max_dist_index

        # Logic that populates the distance numbers to the maze
        for i in range(DEFAULT_SIZE):
            # use the previous starting row values if it's not the 1st iteration since the 1st iteration has a 0 at
            # my_map[0][0]
            if i != 0:
                curr_dist = self.map[i - 1][0].get_distance()
            for j in range(DEFAULT_SIZE):
                # Populating the first quadrant of the maze with the proper numbers
                square_obj = self.map[i][j]
                if i < half_dist_index:
                    if j < half_dist_index:
                        curr_dist -= 1
                        square_obj.set_distance(curr_dist)
                    # Copy all column numbers before the halfway column of the maze
                    else:
                        cpy_distance_cols = self.map[i][max_dist_index - j].get_distance()
                        square_obj.set_distance(cpy_distance_cols)
                # Copy all rows above the halfway row of the maze
                else:
                    cpy_distance_rows = self.map[max_dist_index - i][j].get_distance()
                    square_obj.set_distance(cpy_distance_rows)

    def make_starting_square(self, is_maze):
        if is_maze:
            # Choice are (1) Top Left, (2) Bottom Left, (3) Top Right, (4) Bottom Right
            list_loc = [(0, 0), (0, DEFAULT_SIZE - 1), (DEFAULT_SIZE - 1, 0), (DEFAULT_SIZE - 1, DEFAULT_SIZE - 1)]

            x, y = random.choice(list_loc)
            self.map[x][y].set_start(True)
            self.map[x][y].set_explore(True)
            self.map[x][y].set_bot_here(True)

            # Saving bot's starting location in x and y coordinates
            self.bot_loc_x, self.bot_loc_y = x, y

        # Fill in proper amounts for starting bot in the bot's maze
        else:
            self.map[self.bot_loc_x][self.bot_loc_y].set_start(True)
            self.map[self.bot_loc_x][self.bot_loc_y].set_explore(True)
            self.map[self.bot_loc_x][self.bot_loc_y].set_bot_here(True)

    def make_walls_file(self):
        """
        This method makes a maze from a file. Currently, there's a maze stored on a machine
        called maze1.txt that housed the input or sequence of numbers to populate a 6x6 maze.
        :return: None
        """
        # Use distance numbers as a way to describe the number of walls you've changed per square

        file1 = open(FILENAME, "r")

        for line in file1.readlines():
            x, y, north_file, south_file, west_file, east_file = line.strip('\n').split()
            if DEFAULT_SIZE == 16:
                x = int(x) - 1
                y = int(y) - 1
            else:
                x = int(x)
                y = int(y)
            north_file = bool(int(north_file))
            south_file = bool(int(south_file))
            west_file = bool(int(west_file))
            east_file = bool(int(east_file))

            x_y_corr = x, y
            sq_obj = self.map[x][y]

            # Update dir_tuple to also contain any walls that may already be "True" from previous iteration
            north_og, south_og, west_og, east_og = sq_obj.get_walls()
            if north_og:
                north_file = north_og
            if south_og:
                south_file = south_og
            if west_og:
                west_file = west_og
            if east_og:
                east_file = east_og
            dir_tuple = north_file, south_file, west_file, east_file

            sq_obj.set_square(dir_tuple, False, 1)
            self.check_set_walls(dir_tuple, x_y_corr)

        file1.close()

    def make_walls_user(self):
        """
        A method to make a maze manually through user input. This can be prone to error
        if typing in incorrectly. Not built for error-avoidance.
        :return: None
        """
        print(self.__str__())
        # Use distance numbers as a way to describe the number of walls you've changed per square

        filename = ""
        file1 = open(filename, "a")

        user_input = input("What walls would you like to change (\"s\" or \"stop\" to stop)?\n"
                           "(Ex: x y north:[1\\0] south:[1\\0] west:[1\\0] east:[1\\0])\n"
                           "(1 means to put a wall, 0 means to remove a wall):\n")

        while user_input not in ["s", "stop"]:
            file1.write(user_input)
            file1.write("\n")
            user_list = user_input.split()

            x_y_corr = int(user_list[0]), int(user_list[1])
            x, y = x_y_corr
            dir_tuple = bool(int(user_list[2])), bool(int(user_list[3])), bool(int(user_list[4])), bool(
                int(user_list[5]))

            sq_obj = self.map[x][y]
            sq_obj.set_square(dir_tuple, False, 1)
            self.check_set_walls(dir_tuple, x_y_corr)

            print()
            print(self.__str__())
            print(f"You've changed: coordinate: {x}{y}\n\n{sq_obj}\n")

            user_input = input("What walls would you like to change (\"s\" or \"stop\" to stop)?\n"
                               "(Ex: x y north:[1\\0] south:[1\\0] west:[1\\0] east:[1\\0])\n"
                               "(1 means to put a wall, 0 means to remove a wall):\n")

        file1.close()

    def make_out_walls(self):
        """
        This will edit the maze's map to have squares that will
        have outside walls in its values

        :return: None
        """

        max_dist_index = DEFAULT_SIZE - 1

        # Condition for the outside walls
        num_squares = 0

        # Iteration happens by going in a clockwise direction but to do this you need to
        #   adjust the iterators for rows and columns as you go through it
        min_iterator_i = -1
        i = 0
        max_iterator_i = DEFAULT_SIZE
        flag_i = True

        min_iterator_j = -1
        j = 0
        max_iterator_j = 1
        flag_j = True

        # This flag is needed to skip over the first iteration so that it
        #   sets j = 0 when necessary.
        flag_j_zero = True

        # Skip over code if you're ready to exit
        flag_exit = False

        while num_squares < DEFAULT_SIZE ** 2 - (DEFAULT_SIZE - 2) ** 2:

            while min_iterator_i < i < max_iterator_i:
                if flag_j_zero:
                    j = 0
                elif j > max_dist_index:
                    j = max_dist_index
                while min_iterator_j < j < max_iterator_j:

                    north, south, west, east = False, False, False, False

                    # Top Left corner -> (0, 0)
                    if num_squares == 0:
                        north = True
                        west = True

                    # j will not change when going down the left outer wall
                    elif (max_dist_index * 0) < num_squares < (max_dist_index * 1):
                        west = True

                    # Bottom Left corner -> (5, 0)
                    elif num_squares == (max_dist_index * 1):
                        west = True
                        south = True
                        # update iterators
                        max_iterator_j = DEFAULT_SIZE
                        flag_j_zero = False

                    # The squares between Bottom Left corner -> Bottom Right corner
                    elif (max_dist_index * 1) < num_squares < (max_dist_index * 2):
                        south = True

                    # Bottom Right corner -> (5, 5)
                    elif num_squares == (max_dist_index * 2):
                        south = True
                        east = True
                        # update iterators
                        flag_i = not flag_i

                    # The squares between Bottom Right corner -> Top Right corner
                    elif (max_dist_index * 2) < num_squares < (max_dist_index * 3):
                        east = True

                    # Top Right corner -> (0, 5)
                    elif num_squares == (max_dist_index * 3):
                        east = True
                        north = True
                        # update iterators
                        flag_j = not flag_j

                    # The squares between Top Right corner -> Top Left corner
                    elif (max_dist_index * 3) < num_squares < (max_dist_index * 4):
                        north = True

                    else:
                        flag_exit = True

                    if not flag_exit:
                        dir_tuple = north, south, west, east
                        square_obj = self.map[i][j]
                        square_obj.set_walls(dir_tuple)
                        num_squares += 1

                    if flag_j:
                        j += 1
                    else:
                        j -= 1

                if flag_i:
                    i += 1
                else:
                    i -= 1

    def check_set_walls(self, dir_tuple, x_y_coor):
        """
        Check to see if the wall that is parallel to the set one is within bounds
            If it is, set the wall so the two parallel walls are true -> thus are one wall

        :param dir_tuple: direction tuple that holds as "north, south, west, east"
        :param x_y_coor: x and y coordinate tuple that will unpack to x, y
        :return: None
        """
        x, y = x_y_coor
        north, south, west, east = dir_tuple

        if north and -1 < (x - 1):
            square_obj_above = self.map[x - 1][y]
            square_obj_above.set_south(north)

        if south and (x + 1) < DEFAULT_SIZE:
            square_obj_below = self.map[x + 1][y]
            square_obj_below.set_north(south)

        if west and -1 < (y - 1):
            square_obj_left = self.map[x][y - 1]
            square_obj_left.set_east(west)

        if east and (y + 1) < DEFAULT_SIZE:
            square_obj_right = self.map[x][y + 1]
            square_obj_right.set_west(east)

    def set_distance_nums(self, bot_x, bot_y):
        """
        Recursion function for Flood-Fill Algorithm. This is for when the bot hits a wall
        (or during return-to-start mode, someone has no possible directions)
        and has to update its current square, and most likely, the square it could go to.
        :param bot_x: x or row location of the bot (int)
        :param bot_y: y or col location of the bot (int)
        :return: None
        """

        """
        If a cell is not the destination cell, its value should
        be one plus the minimum value of its open neighbors

        current cell/loc = min(neighbors not block by walls) + 1
        if change: check my neighbors not block by walls and repeat above
        else: return to previous square 
        """

        bot_map = self.map
        curr_sq = bot_map[bot_x][bot_y]
        curr_dist = curr_sq.get_distance()

        # dist_list -> distance list
        dist_list = []
        north, south, west, east = curr_sq.get_walls()

        # if there isn't a wall, then there's a neighboring cell to be checked thus add to dist_list
        if not north:
            dist_list.append(bot_map[bot_x - 1][bot_y].get_distance())
        if not south:
            dist_list.append(bot_map[bot_x + 1][bot_y].get_distance())
        if not west:
            dist_list.append(bot_map[bot_x][bot_y - 1].get_distance())
        if not east:
            dist_list.append(bot_map[bot_x][bot_y + 1].get_distance())

        # min function to determine minimum distance, even if there are repeats
        new_dist = min(dist_list) + 1

        # change is a variable to indicate if where the program is at, has a change square if so,
        #   then you need to check available neighboring squares;
        #   if not, return to the previous square.
        change = True
        if curr_dist != new_dist:
            curr_sq.set_distance(new_dist)
        else:
            change = False

        # BASE CASE
        if not change:
            return
        # RECURSIVE CASES
        if not north:
            self.set_distance_nums(bot_x - 1, bot_y)
        if not south:
            self.set_distance_nums(bot_x + 1, bot_y)
        if not west:
            self.set_distance_nums(bot_x, bot_y - 1)
        if not east:
            self.set_distance_nums(bot_x, bot_y + 1)

    def set_bot_loc(self, bot_loc):
        self.bot_loc_x, self.bot_loc_y = bot_loc

    def get_bot_loc(self):
        return self.bot_loc_x, self.bot_loc_y

    def __str__(self):
        """
        Printing out the distance numbers of the maze in the format of a grid for Map class
        :return: a string to indicate what maze has been outputted (str)
        """
        for i in range(DEFAULT_SIZE):
            for j in range(DEFAULT_SIZE):
                print(self.map[i][j].get_distance(), end=' ')
            print()
        # Compiler yells for not returning string type
        return "Above is the maze's grid\n"

    def __getitem__(self, index_x_y):
        """
        Returns a square object at index_x and index_y location
        :param index_x_y: row and col value (tuple)
        :return: a square object (Square())
        """
        index_x, index_y = index_x_y
        return self.map[index_x][index_y]
