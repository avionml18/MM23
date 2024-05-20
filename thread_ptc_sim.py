# Threading code for MM23; Created/ modified by Kelechi Agommuo

# Purpose: Meant to run motor, discover, RTS, and speedrun functionalities in tandem until GPIO pin is set to HIGH

# Importing required libraries
import threading
import RPi.GPIO as GPIO
import time
from discover import *
from SpeedRun import *
from return_to_start import *

GPIO.setmode(GPIO.BCM)  # Use Broadcom pin-numbering scheme

# setting pins for different operational modes
enable_speed_run = 6
enable_discover = 5
enable_rts_whole = 13
enable_rts_dfs = 12
shutdown = 26

str_start_time = "Starting Program at : " + time.localtime()
write_to_file(str_start_time)

# GPIO setup(s)
print("Setup : Speed Run")
GPIO.setup(enable_speed_run, GPIO.IN)
print("Setup : Discover")
GPIO.setup(enable_discover, GPIO.IN)
print("Setup : RTS_DFS ")
GPIO.setup(enable_rts_dfs, GPIO.IN)
print("Setup : RTS_Whole")
GPIO.setup(enable_rts_whole, GPIO.IN)
print("Setup : Shutdown")
GPIO.setup(shutdown, GPIO.IN)
print("Finish Setup")

# Made to cancel all threads once particular event happens (in this case, when gpio_enable is set to HIGH)
stop_threads = threading.Event()


# def function_one(<param>)
# <param>: GPIO Pin, could be used to send a pin to determine whether to run the Bot's mode
def function_one(pin):
    print("Running flood algo")
    global finishx, finishy
    run_flood_algo(bot_1)
    finishx, finishy = bot_1.get_bot_loc()
    print("Flood Complete")


# def function_two(<param>)
# <param>: GPIO Pin, could be used to send a pin to determine whether to run the Bot's mode
def function_two(pin):
    global starty, startx, bot_map_obj
    print("Running Speedrun")
    speedrun(starty, startx, 0, bot_map_obj, "north", "straight")  # call from starting square with curr-path 0
    new_directions(finishx, finishy, bot_map_obj)
    print("Speedrun Complete")


# def function_three(<param>)
# <param>: GPIO Pin, could be used to send a pin to determine whether to run the Bot's mode
def function_three(pin):
    global bot_1, finishx, finishy
    print("Running Whole Maze Algo")
    run_flood_algo(bot_1)
    finishx, finishy = bot_1.get_bot_loc()
    run_whole_maze_algo(bot_1)
    print("Whole Maze Complete")


# def function_four(<param>)
# <param>: GPIO Pin, could be used to send a pin to determine whether to run the Bot's mode
def function_four(pin):
    global finishx, finishy
    print("Running DFS")
    run_flood_algo(bot_1)
    finishx, finishy = bot_1.get_bot_loc()
    run_depth_search_algo(bot_1)
    print("DFS Compelte")


def thread_loop():    # Creating threads
    # args are your args for target thus motor_run, enable_speed_run, enable_discover, and enable_rts are pins into
    #   their respective targets or functions.
    # args have to be tuple thus the syntax "(arg,)" is meant to denote a tuple with an argument in index 0 and none
    #   in index 1: (arg, None)

    # Starting threads
    lock = 0
    # "Standby Mode" loop. Continuously checks for GPIO mode selection.
    while not GPIO.input(shutdown):
        if GPIO.input(enable_discover) and lock == 0:
            lock = 1
            thread_one = threading.Thread(target=function_one, args=(enable_discover,))
            thread_one.start()

        if GPIO.input(enable_speed_run) and lock == 0:
            lock = 2
            thread_two = threading.Thread(target=function_two, args=(enable_speed_run,))
            thread_two.start()

        if GPIO.input(enable_rts_whole) and lock == 0:
            lock = 3
            thread_three = threading.Thread(target=function_three, args=(enable_rts_whole,))
            thread_three.start()

        if GPIO.input(enable_rts_dfs) and lock == 0:
            lock = 4
            thread_four = threading.Thread(target=function_four, args=(enable_rts_dfs,))
            thread_four.start()

        if lock == 1:
            if not GPIO.input(enable_discover):
                print("Stopping Discover")
                thread_one.join()
                lock = 0
        elif lock == 2:
            if not GPIO.input(enable_speed_run):
                print("Stopping Speedrun")
                thread_two.join()
                lock = 0
        elif lock == 3:
            if not GPIO.input(enable_rts_whole):
                print("Stopping Whole Maze")
                thread_three.join()
                lock = 0
        elif lock == 4:
            if not GPIO.input(enable_rts_dfs):
                print("Stopping DFS")
                thread_four.join()
                lock = 0
        time.sleep(0.5)
    # Creating + Starting cancel thread checker
    gpio_monitor_threads = threading.Thread(target=gpio_enable)
    gpio_monitor_threads.start()

    # Joining all threads, end of threading
    gpio_monitor_threads.join()

    # GPIO cleanup
    GPIO.cleanup()
    print("Cleanup and program completed")
    str_end_time = "Ending Program at : " + time.localtime()
    write_to_file(str_end_time)

thread_loop_sim()