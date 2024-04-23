# Threading code for MM23; Created/ modified by Kelechi Agommuo

# Purpose: Meant to run motor, discover, RTS, and speedrun functionalities in tandem until GPIO pin is set to HIGH

# Importing required libraries
import threading
import logging
from SpeedRun import *
from discover import *
import time

gpio_enable = 22  # Set enabler to determine when to stop threading, change to your preference
# Rest of GPIO pins below may/ may not be useful, I added them because it might be helpful to assign a pin to indicate
# when to run a functionality
motor_run = 23
enable_speed_run = 24
enable_discover = 25
enable_rts = 26

# GPIO setup(s)
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(forwardPin, GPIO.OUT)
# GPIO.setup(backwardPin, GPIO.OUT)
# GPIO.setup(enable_speed_run, GPIO.IN)
# GPIO.setup(enable_discover, GPIO.IN)
# GPIO.setup(enable_rts, GPIO.IN)

# Made to cancel all threads once particular event happens (in this case, when gpio_enable is set to HIGH)
stop_threads = threading.Event()


# Skeleton Code below, complete to your preference

# def function_one(<param>)
# <param>: GPIO Pin, could be used to send a pin to determine whether to run the Bot's mode
def function_one(pin):
    # Will run as long as gpio_enable is not set to HIGH
    while not stop_threads.is_set():
        print("Function one threading")
        pass


# def function_two(<param>)
# <param>: GPIO Pin, could be used to send a pin to determine whether to run the Bot's mode
def function_two(pin):
    # Will run as long as gpio_enable is not set to HIGH
    while not stop_threads.is_set():
        print("Function two threading")
        pass


# def function_three(<param>)
# <param>: GPIO Pin, could be used to send a pin to determine whether to run the Bot's mode
def function_three(pin):
    # Will run as long as gpio_enable is not set to HIGH
    while not stop_threads.is_set():
        print("Function three threading")
        pass


# def function_four(<param>)
# <param>: GPIO Pin, could be used to send a pin to determine whether to run the Bot's mode
def function_four(pin):
    # Will run as long as gpio_enable is not set to HIGH
    while not stop_threads.is_set():
        print("Function four threading")
        pass


if __name__ == '__main__':
    # Creating threads
    thread_one = threading.Thread(target=function_one, args=(motor_run,))
    thread_two = threading.Thread(target=function_two, args=(enable_speed_run,))
    thread_three = threading.Thread(target=function_three, args=(enable_discover,))
    thread_four = threading.Thread(target=function_four, args=(enable_rts,))

    # Starting threads
    thread_one.start()
    thread_two.start()
    thread_three.start()
    thread_four.start()

    # def gpio_cancel_threads()
    # Checks if gpio_enable is set to HIGH, if it's high then stop_threads is triggered and cancels all threads
    # Otherwise, function waits 0.1ms before checking again
    # def gpio_cancel_threads():
    #     while True:
    #         if GPIO.input(gpio_enable) == GPIO.HIGH:
    #             stop_threads.set()
    #             break
    #             time.sleep(0.1)

    # Creating + Starting cancel thread checker
    gpio_monitor_threads = threading.Thread(target=gpio_enable)
    gpio_monitor_threads.start()

    # Joining all threads, end of threading
    gpio_monitor_threads.join()

    # Join threads
    thread_one.join()
    thread_two.join()
    thread_three.join()
    thread_four.join()

    # GPIO cleanup
    # GPIO.cleanup()
