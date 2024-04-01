from discover import *
if __name__ == "__main__":
    """ Things below this main will eventually be in the *driver.py" program. """

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

    # Run the flood fill algorithm
    run_flood_algo(bot_1, maze_1)
    finishx, finishy = maze_1.get_bot_loc()

    # Run the whole maze algorithm
    # run_whole_maze_algo(bot_1, maze_1)

    # Run the depth-first search fill algorithm
    run_depth_search_algo(bot_1, maze_1)


    # SpeedRun
    speedrun(starty, startx, 0, bot_map_obj, "north", "straight")  # call from starting square with curr-path 0

    for i in range(DEFAULT_SIZE):
        # for j in range(4):
        print(i, end=": ")
        for j in range(DEFAULT_SIZE):
            if (bot_map_obj[i, j].shortest_route) < 10:
                print(f" {bot_map_obj[i, j].shortest_route}", end='   |  ')
            elif (bot_map_obj[i, j].shortest_route) < 100:
                print(f" {bot_map_obj[i, j].shortest_route}", end='  |  ')
            else:
                print(f" {bot_map_obj[i, j].shortest_route}", end=' |  ')
        print()
        print("    ------------------------------------------------------------------------------------------")

    directions = ['X'] * bot_map_obj[finishx, finishy].shortest_route

    generate_directions(finishy, finishx, bot_map_obj, directions, len(directions)-1)
    startIndex = 0
    while directions[startIndex] == 'X':
        startIndex += 1
    directionsNew = ['X'] * (len(directions) - startIndex)
    for i in range(len(directions)-startIndex):
        directionsNew[i] = directions[startIndex+i]

    instructions = ['X'] * len(directionsNew)
    generate_instructions(finishy, finishx, bot_map_obj, directionsNew, instructions)

    # prints shortest path of each square in the maze

    print(directionsNew)
    print(instructions)