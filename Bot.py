"""
File:           Bot.py
Author:         Avion Lowery
Date (Start):   10/20/23
Date (Update):  4/27/24
Date (Done):
Email:          alowery1@umbc.edu or loweryavion@gmail.com
Description:    This program will have the class Bot for discover.py program.
"""

from Map import *
from enum import Enum


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

    def move(self, bot_new_x, bot_new_y, maze) -> None:
        """
        Move will actually move the bot in the algorithm then in the actual maze
        :param bot_new_x: x coordinate point for where the bot will move to (int)
        :param bot_new_y: y coordinate point for where the bot will move to (int)
        :param maze: maze object that represents the maze in the real world (Map())
        :return: None
        """
        # This is for telling the motors to start going for a certain amount.
        # self.go = True

        # Gather original location data and update the next square location
        bot_org_x, bot_org_y = self.bot_map.get_bot_loc()
        x_y_coor = bot_new_x, bot_new_y
        self.bot_map[bot_org_x, bot_org_y].set_bot_here(False)
        self.bot_map[bot_new_x, bot_new_y].set_bot_here(True)
        """Does overwriting take long?"""
        self.bot_map[bot_new_x, bot_new_y].set_explore(True)
        self.bot_map.set_bot_loc(x_y_coor)

        # Repeat what you did in the algorithm for moving in the actual maze
        """
        I assume somewhere where here is where we tell the bot to move in a forward direction

        There will be somewhere BEFORE this where we tell the bot to turn or orientate itself to the proper 
            direction
        """
        maze.map[bot_org_x][bot_org_y].set_bot_here(False)
        maze.map[bot_new_x][bot_new_y].set_bot_here(True)
        maze.map[bot_new_x][bot_new_y].set_explore(True)  # Technically isn't necessary
        maze.set_bot_loc(x_y_coor)

    """
    Don't think stop will be needed since in move, we will tell what the motors
    will do and when to stop. However, if we want it to run stop as a NOP or something
    else, that may be a good alternative
    """

    # def stop(self):
    #     # This is for telling the bot to simply stop moving.
    #     self.go = False
    #

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
        self.orientation += 1
        if self.orientation > Orientation.EAST.value:
            self.orientation = Orientation.NORTH.value

    def turn_left(self):
        self.orientation -= 1
        if self.orientation < Orientation.NORTH.value:
            self.orientation = Orientation.EAST.value

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
