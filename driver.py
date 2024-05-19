"""
File:           discover.py
Authors:        Tim Weir, Avion Lowery
Date (Start):   4/1/24
Date (Update):  4/4/24
Email:          <Tim's Email>, alowery1@umbc.edu or avion.m.lowery@gmail.com
Description:    This file will be what the bot will use to run our programs. 
"""
from discover import *
from thread_ptc_sim import *
# from thread_ptc_sim2 import *

if __name__ == "__main__":
    # global maze_1, bot_1, bot_map_obj, startx, starty, is_maze
    # Make an instance of Map to represent the actual maze
    # maze_1 = Map()
    # maze_1.make_maze_map()

    # Make a bot instance to represent the bot itself
    bot_1 = Bot()
    # Set the bot's starting square to the same starting square in the maze
    # Make the bot's map by populating with the distance numbers
    bot_map_obj = bot_1.bot_map

    bot_map_obj.set_bot_loc(maze_1.get_bot_loc())
    is_maze = False
    bot_map_obj.make_starting_square(is_maze)
    startx, starty = maze_1.get_bot_loc()
    startx, starty = maze_1.get_bot_loc()

    thread_loop()
    # thread_loop_sim()

    # Printing SpeedRun
    # print_speedrun()
