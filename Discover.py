"""
File:           FloodAlgo
Author:         Avion Lowery
Date (Start):   10/20/23
Date (Update):  10/27/23
Date (Done):
Email:          alowery1@umbc.edu or loweryavion@gmail.com
Description:    This file will simulate the flood algorithm through terminal
                inputs and outputs
"""

from random import randint

# default size has to greater than 2
# nxn -> Ex: DEFAULT_SIZE = 2 means 2x2 or only four squares (destination squares)
# CAN'T BE AN ODD NUMBER -> Mazes never are
DEFAULT_SIZE = 6


class Map:
    """
    """

    def __int__(self):
        self.size = DEFAULT_SIZE
        # Default map -> Clean slate
        self.map = [[Square()] * self.size for i in range(self.size)]
        self.bot = Bot()

    # Filling in the walls of the maze
    def make_map(self):

        max_dist_index = self.size - 1
        half_dist_index = self.size // 2
        curr_dist = max_dist_index

        # Logic that populates the distance numbers to the maze
        for i in range(self.size):
            # use the previous starting row values if it's not the 1st iteration since the 1st iteration has a 0 at my_map[0][0]
            if i != 0:
                curr_dist = self.map[i - 1][0].distance
            for j in range(self.size):
                if i < half_dist_index:
                    if j < half_dist_index:
                        curr_dist -= 1
                        square_obj = self.map[i][j]
                        square_obj.set_distance(curr_dist)
                    else:
                        square_obj = self.map[i][j]
                        cpy_distance_cols = self.map[i][max_dist_index - j].distance
                        square_obj.set_distance(cpy_distance_cols)
                else:
                    square_obj = self.map[i][j]
                    cpy_distance_rows = self.map[max_dist_index - i][j].distance
                    square_obj.set_distance(cpy_distance_rows)

    # Printing out the distance numbers of the maze in the format of a grid
    def __str__(self):
        for i in range(self.size):
            for j in range(self.size):
                print(self.map[i][j], end=' ')
            print()

    # starting square in one of four corners
    def make_starting_square(self):
        # Choice are (1) Top Left, (2) Bottom Left, (3) Top Right, (4) Bottom Right
        corners_list = [self.map[0][0], self.map[0][self.size - 1], self.map[self.size - 1][0],
                        self.map[self.size - 1][self.size - 1]]
        rand_num = randint(0, 3)
        corners_list[rand_num].is_start = True


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

    def set_square(self, w_north, w_south, w_east, w_west, explore, distance):
        self.set_walls(w_north, w_south, w_east, w_west)
        self.set_explore(explore)
        self.set_distance(distance)

    def set_walls(self, w_north, w_south, w_east, w_west):
        self.w_north = w_north
        self.w_south = w_south
        self.w_east = w_east
        self.w_west = w_west

    def set_explore(self, explore):
        self.is_explore = explore

    def set_distance(self, distance):
        self.distance = distance

    def __str__(self):
        return str(self.distance)


class Bot:
    """
    """

    def __init__(self):
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.go = False

        self.loc_x = 0
        self.loc_y = 0

        """ bot_map is where the bot is finding a route. It does not know of walls until it hits one """
        self.bot_map = Map()

    def move(self):
        self.go = True

    def stop(self):
        self.go = False

    # Once direction is set
    def set_dir(self, up, down, left, right):
        self.up = up
        self.down = down
        self.left = left
        self.right = right

    # The algorithm will pass in all parameters!!!
    # Possible error is that it's not passing by reference but by value
    def call_updated_square(self, w_north, w_south, w_east, w_west, explored, distance, x_corr, y_corr):
        map_object = self.bot_map
        square_object = map_object.map[x_corr][y_corr]
        square_object.set_square(w_north, w_south, w_east, w_west, explored, distance)

    def __str__(self):
        return f"location is row:{self.loc_x} col:{self.loc_y}"


"""
"""


def run_flood_algo():
    # do a quick fill in of pseudocode
    pass


"""
"""


def run_whole_maze_algo():
    pass


"""
"""


def run_depth_search_algo():
    pass


if __name__ == "__main__":
    # Make an instance of Map to represent the actual maze

    pass
