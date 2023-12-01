"""
File:           Square.py
Author:         Avion Lowery
Date (Start):   10/20/23
Date (Update):  11/29/23
Date (Done):
Email:          alowery1@umbc.edu or loweryavion@gmail.com
Description:    This program will have the class Square for discover.py program.
"""


class Square:
    """
    A square class, the properties of each square in the maze
    """

    def __init__(self, bool_t_f=False):
        """is is_dest needed?"""
        self.is_dest = 0
        self.is_start = False
        self.w_north = bool_t_f
        self.w_south = bool_t_f
        self.w_west = bool_t_f
        self.w_east = bool_t_f
        self.is_explore = False
        self.distance = 0
        """Is the mouse supposed to have the shortest route?"""
        self.shortest_route = 99
        self.bot_here = False

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

    def set_bot_here(self, bool_val):
        self.bot_here = bool_val

    def set_explore(self, explore):
        self.is_explore = explore

    def set_distance(self, distance):
        self.distance = distance

    def set_start(self, start):
        self.is_start = start

    def get_north_wall(self):
        return self.w_north

    def get_south_wall(self):
        return self.w_south

    def get_west_wall(self):
        return self.w_west

    def get_east_wall(self):
        return self.w_east

    def get_walls(self):
        return self.w_north, self.w_south, self.w_west, self.w_east

    def get_explore(self):
        return self.is_explore

    def get_distance(self):
        return self.distance

    def get_start(self):
        return self.is_start

    def __str__(self):
        """
        Printing the object square will call this function which will do whatever
        is in the body and will output whatever string is wanted in terminal
        :return: a representation of a square with walls and distance number in the center (str)
        """
        sq_str = f"     {self.w_north}     \n{self.w_west}\t{self.distance}\t{self.w_east}\n     {self.w_south}\n"
        return sq_str

    # def __str__(self, corr):
    #     """
    #     Printing the object square will call this function which will do whatever
    #     is in the body and will output whatever string is wanted in terminal
    #     :return: a representation of a square with walls and coordinate pair in the center (str)
    #     """
    #     sq_str = f"     {self.w_north}     \n{self.w_west}\t{corr}\t{self.w_east}\n     {self.w_south}\n"
    #     return sq_str
