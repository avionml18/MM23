# Threading code for MM23; Created/ modified by Kelechi Agommuo

# Purpose: Meant to run motor, discover, RTS, and speedrun functionalities in tandem until GPIO pin is set to HIGH

# Importing required libraries
import threading
import time
from discover import *
from SpeedRun import *
from return_to_start import *

enable_speed_run = 6
enable_discover = 5
enable_rts_whole = 13
enable_rts_dfs = 12
shutdown = 26

# testing
# global maze_1, bot_1, bot_map_obj, startx, starty, is_maze
# Make an instance of Map to represent the actual maze
maze_1 = Map()
maze_1.make_maze_map()

# Make a bot instance to represent the bot itself
bot_1 = Bot()
# Set the bot's starting square to the same starting square in the maze
# Make the bot's map by populating with the distance numbers
bot_map_obj = bot_1.bot_map

bot_map_obj.set_bot_loc(maze_1.get_bot_loc())
is_maze = False
bot_map_obj.make_starting_square(is_maze)
startx, starty = maze_1.get_bot_loc()

# end testing

# Made to cancel all threads once particular event happens (in this case, when gpio_enable is set to HIGH)
stop_threads = threading.Event()


# def function_one(<param>)
# <param>: GPIO Pin, could be used to send a pin to determine whether to run the Bot's mode
def function_one(pin):
    print("Running flood algo")
    global finishx, finishy
    run_flood_algo(bot_1, maze_1)
    finishx, finishy = maze_1.get_bot_loc()


# def function_two(<param>)
# <param>: GPIO Pin, could be used to send a pin to determine whether to run the Bot's mode
def function_two(pin):
    # global starty, startx, bot_map_obj
    print("Running Speedrun")
    speedrun(starty, startx, 0, bot_map_obj, "north", "straight")  # call from starting square with curr-path 0
    new_directions(finishx, finishy, bot_map_obj)

# def function_three(<param>)
# <param>: GPIO Pin, could be used to send a pin to determine whether to run the Bot's mode
def function_three(pin):
    # global bot_1, maze_1, finishx, finishy
    print("Running Whole Maze Algo")
    # run_flood_algo(bot_1, maze_1)
    # finishx, finishy = maze_1.get_bot_loc()
    # run_whole_maze_algo(bot_1, maze_1)


# def function_four(<param>)
# <param>: GPIO Pin, could be used to send a pin to determine whether to run the Bot's mode
def function_four(pin):
    global finishx, finishy
    print("Running DFS")
    run_flood_algo(bot_1, maze_1)
    finishx, finishy = maze_1.get_bot_loc()
    run_depth_search_algo(bot_1, maze_1)


def thread_loop_sim():    # Creating threads
    # args are your args for target thus motor_run, enable_speed_run, enable_discover, and enable_rts are pins into
    #   their respective targets or functions.
    # args have to be tuple thus the syntax "(arg,)" is meant to denote a tuple with an argument in index 0 and none
    #   in index 1: (arg, None)

    print("Threading Test Start")
    # Starting threads
    lock = 0
    temp = 0
    # "Standby Mode" loop. Continuously checks for GPIO mode selection.
    while not temp == 10:
        if temp % 4 == 0 and lock == 0:
            lock = 1
            thread_one = threading.Thread(target=function_one, args=(enable_discover,))
            thread_one.start()

        elif temp % 3 == 0 and lock == 0:
            lock = 2
            thread_two = threading.Thread(target=function_two, args=(enable_speed_run,))
            thread_two.start()

        elif temp % 2 == 0 and lock == 0:
            lock = 3
            thread_three = threading.Thread(target=function_three, args=(enable_rts_whole,))
            thread_three.start()

        elif lock == 0:
            lock = 4
            thread_four = threading.Thread(target=function_four, args=(enable_rts_dfs,))
            thread_four.start()

        if lock == 1:
            time.sleep(3)
            print("Stopping Discover")
            thread_one.join()
            lock = 0
        elif lock == 2:
            time.sleep(3)
            print("Stopping Speedrun")
            thread_two.join()
            lock = 0
        elif lock == 3:
            time.sleep(3)
            print("Stopping Whole Maze")
            thread_three.join()
            lock = 0
        elif lock == 4:
            time.sleep(3)
            print("Stopping DFS")
            thread_four.join()
            lock = 0

        temp += 1

    print("Threading Done")


thread_loop_sim()