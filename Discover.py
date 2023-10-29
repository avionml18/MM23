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

# default size has to greater than 2
# nxn -> Ex: DEFAULT_SIZE = 2 means 2x2 or only four squares (destination squares)
# CAN'T BE AN ODD NUMBER -> Mazes never are
DEFAULT_SIZE = 4


# random.seed("random")


class Map:
    """
    This is where the map of the bot and where the user can choose to make a starting map are housed
    """

    def __init__(self):
        """
        self.map = [[Square()] * DEFAULT_SIZE for i in range(DEFAULT_SIZE)]
        
        This does not work the way I need it to because this populates a square object with a specific 
        memory address for DEFAULT_SIZE in one row. As in, you change one attribute of square at 0,0, it
        will change it for all square objects in the row since they all "point" to the same object.
        
        Think of it as pointers...What really happens is you have different pointers in the row that point
        to the same object. Thus, you change a value where one pointer is pointing to, then all values are changed.
        
        """
        # Default map -> Clean slate
        self.map = [[Square() for i in range(DEFAULT_SIZE)] for i in range(DEFAULT_SIZE)]
        self.bot_loc_x, self.bot_loc_y = 0, 0

    def make_maze_map(self):
        self.make_starting_square()
        self.make_walls()

    # Filling in the distance numbers of the maze
    def make_bot_map(self):

        max_dist_index = DEFAULT_SIZE - 1
        half_dist_index = DEFAULT_SIZE // 2
        curr_dist = max_dist_index

        # Logic that populates the distance numbers to the maze
        for i in range(DEFAULT_SIZE):
            # use the previous starting row values if it's not the 1st iteration since the 1st iteration has a 0 at my_map[0][0]
            if i != 0:
                curr_dist = self.map[i - 1][0].distance
            for j in range(DEFAULT_SIZE):
                # Populating the first quadrant of the maze with the proper numbers
                square_obj = self.map[i][j]
                if i < half_dist_index:
                    if j < half_dist_index:
                        curr_dist -= 1
                        square_obj.set_distance(curr_dist)
                    # Copy all column numbers before the halfway column of the maze
                    else:
                        cpy_distance_cols = self.map[i][max_dist_index - j].distance
                        square_obj.set_distance(cpy_distance_cols)
                # Copy all rows above the halfway row of the maze
                else:
                    cpy_distance_rows = self.map[max_dist_index - i][j].distance
                    square_obj.set_distance(cpy_distance_rows)

    def make_starting_square(self):
        # Choice are (1) Top Left, (2) Bottom Left, (3) Top Right, (4) Bottom Right
        list_loc = [(0, 0), (0, DEFAULT_SIZE - 1), (DEFAULT_SIZE - 1, 0), (DEFAULT_SIZE - 1, DEFAULT_SIZE - 1)]

        x, y = random.choice(list_loc)
        self.map[x][y].is_start = True

        # Saving bot's starting location in x and y coordinates
        self.bot_loc_x, self.bot_loc_y = x, y

    def make_walls(self):
        """
        This will edit the maze's map to have squares that will have walls in its values

        :return: None
        """

        max_dist_index = DEFAULT_SIZE - 1
        half_dist_index = DEFAULT_SIZE // 2

        """ ALWAYS Check to make any adjacent WALLS have the SAME value """

        # Condition for the outside walls
        for i in range(DEFAULT_SIZE):
            for j in range(DEFAULT_SIZE):
                pass

        # Condition for the destination square
        # There's one opening
        total_walls_dest = 8
        for i in range(DEFAULT_SIZE):
            for j in range(DEFAULT_SIZE):
                if (i == half_dist_index or i == half_dist_index - 1) and \
                        (j == half_dist_index or j == half_dist_index - 1):
                    pass
        # Only activate or make walls "True"

    def set_bot_loc(self, bot_loc):
        self.bot_loc_x, self.bot_loc_y = bot_loc

    def get_bot_loc(self):
        return self.bot_loc_x, self.bot_loc_y

    # Printing out the distance numbers of the maze in the format of a grid
    def __str__(self):
        for i in range(DEFAULT_SIZE):
            for j in range(DEFAULT_SIZE):
                print(self.map[i][j].distance, end=' ')
            print()
        # Compiler yells for not returning string type
        return "Above is the maze's grid\n"


class Square:
    """
    A square class, the properties of each square in the maze
    """

    def __init__(self):
        # self.is_dest = 0
        self.is_start = False
        self.w_north = False
        self.w_south = False
        self.w_east = False
        self.w_west = False
        self.is_explore = False
        self.distance = 0
        # Is the mouse supposed to have the shortest route?
        self.shortest_route = 99

    def set_square(self, dir_tuple, explore, distance):
        self.set_walls(dir_tuple)
        self.set_explore(explore)
        self.set_distance(distance)

    def set_walls(self, dir_tuple):
        self.w_north, self.w_south, self.w_east, self.w_west = dir_tuple

    def set_explore(self, explore):
        self.is_explore = explore

    def set_distance(self, distance):
        self.distance = distance

    def get_walls(self):
        return self.w_north, self.w_south, self.w_east, self.w_west

    def get_explore(self):
        return self.is_explore

    def get_distance(self):
        return self.distance

    def check_update_walls(self):
        pass

    def __str__(self):
        return str(self.distance)


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
        self.bot_map = Map()
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
    def call_set_square(self, dir_tuple, explored, distance, x_y_corr):
        map_object = self.bot_map
        x_corr, y_corr = x_y_corr
        square_object = map_object.map[x_corr][y_corr]
        square_object.set_square(dir_tuple, explored, distance)

    def __str__(self):
        for i in range(DEFAULT_SIZE):
            for j in range(DEFAULT_SIZE):
                print(self.bot_map.map[i][j].distance, end=' ')
            print()
        str_bot = (f"Above is the bot's starting grid"
                   f"\nStarting square is row:{self.bot_map.bot_loc_x}\tcol:{self.bot_map.bot_loc_y}")
        return str_bot


def run_flood_algo():
    """
    This is where the Flood-Fill algorithm and the arithmetic behind it is housed
    * There are better Flood-Fill Algorithms
    """
    # do a quick fill in of pseudocode
    pass


def run_depth_search_algo():
    """
    This is where the Depth First Search algorithm and the arithmetic behind it is housed
    Depth first search, bot goes -> intersection -> random direction -- if deadened --> go back to intersection -> repeat
    :return:
    """
    pass


def run_whole_maze_algo():
    """
    This is where the Whole Maze algorithm and the arithmetic behind it is housed
    whole-maze is similar to depth first search...We want to search as many possible paths and ideally get back to the start
    :return:
    """
    pass


if __name__ == "__main__":
    # Make an instance of Map to represent the actual maze
    maze = Map()
    maze.make_maze_map()

    # Make a bot instance to represent the bot itself
    bot = Bot()
    # Set the bot's starting square to the same starting square in the maze
    # Make the bot's map by populating with the distance numbers
    bot.bot_map.set_bot_loc(maze.get_bot_loc())
    bot.bot_map.make_bot_map()
    print(bot)
