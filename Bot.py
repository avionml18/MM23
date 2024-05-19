"""
File:           Bot.py
Author:         Avion Lowery
Date (Start):   10/20/23
Date (Update):  4/27/24
Date (Done):
Email:          alowery1@umbc.edu or loweryavion@gmail.com
Description:    This program will have the class Bot for discover.py program.
"""
from Colors import *
from Map import *
from enum import Enum
from motorCode5 import *


class Orientation(Enum):
    """
    Probably a better way to indicate orientations rather than using enumeration but
    used in algorithms for logic in directions uses
    """
    # The reason for the associations are to make going right +1 and left -1.
    #   think of each number starting a north as reading the unit circle from left to right.
    NORTH = 1
    SOUTH = 3
    EAST = 2
    WEST = 4


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
        self.orientation = Orientation.NORTH.value

        """ bot_map is where the bot is finding a route. It does not know of walls until it hits one """
        self.bot_map: Map = Map()
        self.bot_map.make_bot_map()

    def move(self, bot_new_x, bot_new_y) -> None:
        """
            Move will actually move the bot in the algorithm then in the actual maze
            :param bot_new_x: x coordinate point for where the bot will move to (int)
            :param bot_new_y: y coordinate point for where the bot will move to (int)
            :param maze: maze object that represents the maze in the real world (Map())
            :return: None
            """
        # This is for telling the motors to start going for a certain amount.
        # self.go = True

        move_motor('f', 1)  # duration for 1 second

        # Gather original location data and update the next square location
        bot_org_x, bot_org_y = self.bot_map.get_bot_loc()
        x_y_coor = bot_new_x, bot_new_y
        self.bot_map[bot_org_x, bot_org_y].set_bot_here(False)
        self.bot_map[bot_new_x, bot_new_y].set_bot_here(True)
        """Does overwriting take long?"""
        self.bot_map[bot_new_x, bot_new_y].set_explore(True)
        self.bot_map.set_bot_loc(x_y_coor)

    # def move(self, bot_new_x, bot_new_y, maze) -> None:
    #     """
    #     Move will actually move the bot in the algorithm then in the actual maze
    #     :param bot_new_x: x coordinate point for where the bot will move to (int)
    #     :param bot_new_y: y coordinate point for where the bot will move to (int)
    #     :param maze: maze object that represents the maze in the real world (Map())
    #     :return: None
    #     """
    #     # This is for telling the motors to start going for a certain amount.
    #     # self.go = True
    #
    #     move_motor('f', 1) # duration for 1 second
    #
    #     # Gather original location data and update the next square location
    #     bot_org_x, bot_org_y = self.bot_map.get_bot_loc()
    #     x_y_coor = bot_new_x, bot_new_y
    #     self.bot_map[bot_org_x, bot_org_y].set_bot_here(False)
    #     self.bot_map[bot_new_x, bot_new_y].set_bot_here(True)
    #     """Does overwriting take long?"""
    #     self.bot_map[bot_new_x, bot_new_y].set_explore(True)
    #     self.bot_map.set_bot_loc(x_y_coor)
    #
    #     # Repeat what you did in the algorithm for moving in the actual maze
    #     maze.map[bot_org_x][bot_org_y].set_bot_here(False)
    #     maze.map[bot_new_x][bot_new_y].set_bot_here(True)
    #     maze.map[bot_new_x][bot_new_y].set_explore(True)  # Technically isn't necessary
    #     maze.set_bot_loc(x_y_coor)

    # Once direction is set, then tell the algo you're ready to go by calling function move
    def set_dir(self, up, down, left, right):
        self.up = up
        self.down = down
        self.left = left
        self.right = right

    def call_set_square(self, dir_tuple, explored, distance, x_y_coor):
        """
        This method takes in wall, explore, distance, and x & y coordinate values
        to set/update square objects to what arguments are passed in.

        The algorithm will pass in all parameters!!!

        :param dir_tuple: holds north, south, west, east values (4 bool tuple)
        :param explored: if the bot has explored the current square (bool)
        :param distance: represents how far the square is from the destination square(s) (int)
        :param x_y_coor: a coordinate pair to represent the square to be set (2 int tuple)
        :return: None
        """
        map_object = self.bot_map
        x_coor, y_coor = x_y_coor
        square_obj = map_object.map[x_coor][y_coor]
        square_obj.set_square(dir_tuple, explored, distance)

    def set_orientation(self, orientate):
        """
        This method will set the bot's orientation to one of the four cardinal directions
        :param orientate: holds what orientation the bot is currently in (ENUM of Orientation_
        :return: None
        """
        self.orientation = orientate

    def get_orientation(self):
        """
        This method will return  the bot's orientation to one of the four cardinal directions
        :return: bot's current orienation (self.orientation)
        """
        return self.orientation

    def turn_right(self):
        # print(fg.red + "Rotate RIGHT" + Colors.reset)
        self.orientation += 1
        if self.orientation > Orientation.WEST.value:
            self.orientation = Orientation.NORTH.value

        move_motor('R', 1)  # Duration is in seconds (1 second)

    def turn_left(self):
        self.orientation -= 1
        # print(fg.red + "Rotate LEFT" + Colors.reset)

        if self.orientation < Orientation.NORTH.value:
            self.orientation = Orientation.WEST.value

        move_motor('L', 1)  # Duration is in seconds (1 second)

    def print_orientation(self):
        if self.orientation == Orientation.NORTH.value:
            print(Orientation.NORTH.name)
        elif self.orientation == Orientation.SOUTH.value:
            print(Orientation.SOUTH.name)
        elif self.orientation == Orientation.WEST.value:
            print(Orientation.WEST.name)
        elif self.orientation == Orientation.EAST.value:
            print(Orientation.EAST.name)
        else:
            print("Error: Very Bad - Bot.py in print_orientation")

    def __str__(self):
        """
        Printing out the distance numbers of the maze in the format of a grid for Bot class
        :return: a string to indicate what maze has been outputted and location of bot (str)
        """
        for i in range(DEFAULT_SIZE):
            for j in range(DEFAULT_SIZE):
                print(self.bot_map.map[i][j].get_distance(), end=' ')
            print()

        loc_x, loc_y = self.bot_map.get_bot_loc()
        str_bot = (f"Above is the bot's starting grid"
                   f"\nCurrent location of bot is row:{loc_x}\tcol:{loc_y}")

        return str_bot
