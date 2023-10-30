"""
File:           FloodAlgo
Author:         Avion Lowery
Date (Start):   10/20/23
Date (Update):  10/28/23
Date (Done):
Email:          alowery1@umbc.edu or loweryavion@gmail.com
Description:    This file will simulate the flood algorithm through terminal
                inputs and outputs
"""

import random

# Default size has to greater than 2
# nxn -> Ex: DEFAULT_SIZE = 2 means 2x2 or only four squares (destination squares)
# CAN'T BE AN ODD NUMBER -> Mazes never are

# DEFAULT_SIZE = 4
DEFAULT_SIZE = 6
# DEFAULT_SIZE = 8
# DEFAULT_SIZE = 16

MAKE_WALLS_USER = False

# Consistent location of starting location and anywhere random is used (Depth First Search Algo)
random.seed("random")
from enum import Enum


class Direction(Enum):
    up = 1
    down = 2
    left = 3
    right = 4


class Map:
    """
    This is where the map of the bot and where the user can choose to make a starting map are housed
    """

    def __init__(self, bool_t_f=False):
        """
        self.map = [[Square()] * DEFAULT_SIZE for i in range(DEFAULT_SIZE)]
        
        This does not work the way I need it to because this populates a square object with a specific 
        memory address for DEFAULT_SIZE in one row. As in, you change one attribute of square at 0,0, it
        will change it for all square objects in the row since they all "point" to the same object.
        
        Think of it as pointers...What really happens is you have different pointers in the row that point
        to the same object. Thus, you change a value where one pointer is pointing to, then all values are changed.
        
        """
        # Default map -> Clean slate
        self.map = [[Square(bool_t_f) for i in range(DEFAULT_SIZE)] for i in range(DEFAULT_SIZE)]
        self.bot_loc_x, self.bot_loc_y = 0, 0

    def make_maze_map(self):
        self.make_starting_square()
        self.make_out_walls()
        if MAKE_WALLS_USER:
            self.make_walls_user()
        else:
            self.make_walls_file()

    def make_bot_map(self):
        self.make_distance_nums()
        self.make_out_walls()

    # Filling in the distance numbers of the maze
    def make_distance_nums(self):

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

    def make_starting_square(self):
        # Choice are (1) Top Left, (2) Bottom Left, (3) Top Right, (4) Bottom Right
        list_loc = [(0, 0), (0, DEFAULT_SIZE - 1), (DEFAULT_SIZE - 1, 0), (DEFAULT_SIZE - 1, DEFAULT_SIZE - 1)]

        x, y = random.choice(list_loc)
        # ****Should I make this a setter?
        self.map[x][y].is_start = True
        self.map[x][y].set_explore(True)

        # Saving bot's starting location in x and y coordinates
        self.bot_loc_x, self.bot_loc_y = x, y

    def make_walls_file(self):
        print(self.__str__())
        # Use distance numbers as a way to describe the number of walls you've changed per square

        filename = "maze1.txt"
        file1 = open(filename, "r")

        for line in file1.readlines():
            x, y, north, south, west, east = line.strip('\n').split()
            x = int(x)
            y = int(y)
            north = bool(int(north))
            south = bool(int(south))
            west = bool(int(west))
            east = bool(int(east))

            x_y_corr = x, y
            dir_tuple = north, south, west, east

            sq_obj = self.map[x][y]
            sq_obj.set_square(dir_tuple, False, 1)
            self.check_set_walls(dir_tuple, x_y_corr)

        file1.close()

    def make_walls_user(self):
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
        This will edit the maze's map to have squares that will have outside walls in its values

        :return: None
        """

        max_dist_index = DEFAULT_SIZE - 1
        # half_dist_index = DEFAULT_SIZE // 2

        """ ALWAYS Check to make any adjacent WALLS have the SAME value """

        # Condition for the outside walls
        num_squares = 0

        # bool_list = [True, False]

        min_iterator_i = -1
        i = 0
        max_iterator_i = DEFAULT_SIZE
        flag_i = True
        # flag_i_start = True

        min_iterator_j = -1
        j = 0
        max_iterator_j = 1
        flag_j = True
        flag_j_zero = True

        flag_exit = False

        while num_squares < DEFAULT_SIZE ** 2 - (DEFAULT_SIZE - 2) ** 2:

            while min_iterator_i < i < max_iterator_i:
                if flag_j_zero:
                    j = 0
                elif j > max_dist_index:
                    j = max_dist_index
                while min_iterator_j < j < max_iterator_j:

                    north, south, west, east = False, False, False, False

                    if num_squares == 0:
                        north = True
                        west = True

                    # j will not change when going down the left outer wall
                    elif (max_dist_index * 0) < num_squares < (max_dist_index * 1):
                        west = True

                    elif num_squares == (max_dist_index * 1):
                        west = True
                        south = True
                        # update iterators
                        max_iterator_j = DEFAULT_SIZE
                        flag_j_zero = False
                        # flag_i_start = False

                    elif (max_dist_index * 1) < num_squares < (max_dist_index * 2):
                        south = True

                    elif num_squares == (max_dist_index * 2):
                        south = True
                        east = True
                        # update iterators
                        flag_i = not flag_i

                    elif (max_dist_index * 2) < num_squares < (max_dist_index * 3):
                        east = True

                    elif num_squares == (max_dist_index * 3):
                        east = True
                        north = True
                        # update iterators
                        flag_j = not flag_j

                    elif (max_dist_index * 3) < num_squares < (max_dist_index * 4):
                        north = True

                    else:
                        flag_exit = True

                    if not flag_exit:
                        dir_tuple = north, south, west, east
                        square_obj = self.map[i][j]
                        square_obj.set_walls(dir_tuple)
                        # self.check_set_walls(square_obj.get_walls(), (i, j))
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
        north, south, east, west = dir_tuple

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

    def set_bot_loc(self, bot_loc):
        self.bot_loc_x, self.bot_loc_y = bot_loc

    def get_bot_loc(self):
        return self.bot_loc_x, self.bot_loc_y

    # Printing out the distance numbers of the maze in the format of a grid
    def __str__(self):
        for i in range(DEFAULT_SIZE):
            for j in range(DEFAULT_SIZE):
                print(self.map[i][j].get_distance(), end=' ')
            print()
        # Compiler yells for not returning string type
        return "Above is the maze's grid\n"


class Square:
    """
    A square class, the properties of each square in the maze
    """

    def __init__(self, bool_t_f=False):
        # self.is_dest = 0
        self.is_start = False
        self.w_north = bool_t_f
        self.w_south = bool_t_f
        self.w_west = bool_t_f
        self.w_east = bool_t_f
        self.is_explore = False
        self.distance = 0
        # Is the mouse supposed to have the shortest route?
        self.shortest_route = 99

    def set_square(self, dir_tuple, explore, distance):
        self.set_walls(dir_tuple)
        self.set_explore(explore)
        self.set_distance(distance)

    def set_walls(self, dir_tuple):
        self.w_north, self.w_south, self.w_west, self.w_east = dir_tuple

    def set_north(self, bool_val):
        self.w_north = bool_val

    def set_south(self, bool_val):
        self.w_south = bool_val

    def set_west(self, bool_val):
        self.w_west = bool_val

    def set_east(self, bool_val):
        self.w_east = bool_val

    def set_explore(self, explore):
        self.is_explore = explore

    def set_distance(self, distance):
        self.distance = distance

    def get_walls(self):
        return self.w_north, self.w_south, self.w_west, self.w_east

    def get_explore(self):
        return self.is_explore

    def get_distance(self):
        return self.distance

    def __str__(self):
        sq_str = f"     {self.w_north}\n{self.w_west}\t{self.distance}\t{self.w_east}\n     {self.w_south}"
        return sq_str


class Bot:
    """
    This is where the bot's functionality and attributes are housed
    """

    def __init__(self):
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.go = False

        """ bot_map is where the bot is finding a route. It does not know of walls until it hits one """
        self.bot_map = Map(False)
        self.bot_map.make_bot_map()

    def move(self):
        self.go = True

    def stop(self):
        self.go = False

    # Once direction is set, then tell the algo you're ready to go by calling function move
    def set_dir(self, up, down, left, right):
        self.up = up
        self.down = down
        self.left = left
        self.right = right

    # The algorithm will pass in all parameters!!!
    # Possible error is that it's not passing by reference but by value
    def call_set_square(self, dir_tuple, explored, distance, x_y_coor):
        map_object = self.bot_map
        x_coor, y_coor = x_y_coor
        square_obj = map_object.map[x_coor][y_coor]
        square_obj.set_square(dir_tuple, explored, distance)

    def __str__(self):
        for i in range(DEFAULT_SIZE):
            for j in range(DEFAULT_SIZE):
                print(self.bot_map.map[i][j].get_distance(), end=' ')
            print()

        loc_x, loc_y = self.bot_map.get_bot_loc()
        str_bot = (f"Above is the bot's starting grid"
                   f"\nStarting square is row:{loc_x}\tcol:{loc_y}")

        return str_bot


def run_flood_algo(bot, maze):
    """
    This is where the Flood-Fill algorithm and the arithmetic behind it is housed
    * There are better Flood-Fill Algorithms
    """
    # Bot looks through all adjacent cells which aren't blocked by walls and choose the lowest distance values
    # Turning take time thus if you have two choices, choose the one where the bot will not have to move much
    # If run into a wall, update wall and distance values

    # Every time the mouse moves:
    #   Update the wall map
    #   Flood the maze with new distance values -> Modified version = flood the necessary values
    #   Decide which neighboring cell has the lowest distance value
    #   Move to the neighboring cell with the lowest distance value

    # Starting location of bot (5, 5)
    x, y = maze_1.get_bot_loc()
    # Assume it's in position to go straight from the start # Orientation Matters!!!
    distance = bot.bot_map[x][y].get_distance()
    while distance != 0:
        possible_dir = []
        # Analyze choices:
        if -1 < (x - 1):
            if bot.bot_map[x - 1][y].get_distance() < distance:
                possible_dir.append(Direction.up.value)
        if (x + 1) < DEFAULT_SIZE:
            if bot.bot_map[x + 1][y].get_distance() < distance:
                possible_dir.append(Direction.down.value)
        if -1 < (y - 1):
            if bot.bot_map[x][y - 1].get_distance() < distance:
                possible_dir.append(Direction.left.value)
        if (y + 1) < DEFAULT_SIZE:
            if bot.bot_map[x][y + 1].get_distance() < distance:
                possible_dir.append(Direction.right.value)

        # Determine a direction by randomly selecting between two
        # In reality, we would have a gyro or something to indicate the bot's orientation thus, that
        #   would be a factor in this decision
        dir_to_go = random.choice(possible_dir)

        # Look in the actual maze for walls
        north, south, west, east = maze_1.map[x][y].get_walls()
        # Then tell the bot where to go in the actual maze
        # If you hit a wall -> update the wall on the bot's map and update distance numbers for the bot and go again

        if dir_to_go == 1 and not north:
            x -= 1

            # Go bot
            bot.move()

        elif dir_to_go == 2 and not south:
            x += 1

            # Go bot
            bot.move()

        elif dir_to_go == 3 and not west:
            y -= 1

            # Go bot
            bot.move()

        elif dir_to_go == 4 and not east:
            y += 1

            # Go bot
            bot.move()

        # update distance for possible next iteration
        distance = bot.bot_map[x][y].get_distance()


def run_depth_search_algo():
    """
    This is where the Depth First Search algorithm and the arithmetic behind it is housed Depth first search,
    bot goes -> intersection -> random direction -- if deadened --> go back to intersection -> repeat :return:
    """
    pass


def run_whole_maze_algo():
    """
    This is where the Whole Maze algorithm and the arithmetic behind it is housed whole-maze is similar to depth
    first search...We want to search as many possible paths and ideally get back to the start :return:
    """
    pass


if __name__ == "__main__":
    # Make an instance of Map to represent the actual maze
    maze_1 = Map()
    maze_1.make_maze_map()
    print(maze_1)

    # Make a bot instance to represent the bot itself
    bot_1 = Bot()
    # Set the bot's starting square to the same starting square in the maze
    # Make the bot's map by populating with the distance numbers
    bot_map_obj = bot_1.bot_map
    bot_map_obj.set_bot_loc(maze_1.get_bot_loc())
    print(bot_1)

    run_flood_algo(bot_1, maze_1)
