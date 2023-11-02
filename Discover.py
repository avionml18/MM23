"""
File:           discover.py
Author:         Avion Lowery
Date (Start):   10/20/23
Date (Update):  11/1/23
Date (Done):
Email:          alowery1@umbc.edu or loweryavion@gmail.com
Description:    This file will simulate the algorithms through terminal
"""
from enum import Enum
import random

# Default size has to greater than 2
# nxn -> Ex: DEFAULT_SIZE = 2 means 2x2 or only four squares (destination squares)
# CAN'T BE AN ODD NUMBER -> Mazes never are

# DEFAULT_SIZE = 4
DEFAULT_SIZE = 6
# DEFAULT_SIZE = 8
# DEFAULT_SIZE = 16

MAKE_WALLS_USER = False

# Consistent location of starting location and anywhere random is used (Depth First Search Algo)
random.seed("random")


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class Map:
    """
    This is where the map of the bot and where the user can choose to make a starting map are housed
    """

    def __init__(self, bool_t_f=False):
        """
        self.map = [[Square()] * DEFAULT_SIZE for i in range(DEFAULT_SIZE)]
        
        This does not work the way I need it to because this populates a square object with a specific 
        memory address for DEFAULT_SIZE in one row. As in, you change one attribute of square at 0,0, it
        will change it for all square objects in the row since they all "point" to the same object.
        
        Think of it as pointers...What really happens is you have different pointers in the row that point
        to the same object. Thus, you change a value where one pointer is pointing to, then all values are changed.
        
        """
        # Default map -> Clean slate
        self.map = [[Square(bool_t_f) for i in range(DEFAULT_SIZE)] for i in range(DEFAULT_SIZE)]
        self.bot_loc_x, self.bot_loc_y = 0, 0

    def make_maze_map(self):
        """
        Method for making a simulated maze for the bot to traverse in.
        :return: None
        """
        self.make_starting_square()
        self.make_out_walls()
        if MAKE_WALLS_USER:
            self.make_walls_user()
        else:
            self.make_walls_file()

    def make_bot_map(self):
        """
        Method for making a bot's  maze that is used for maze solving and route choosing
        :return: None
        """
        self.make_distance_nums()
        self.make_out_walls()

    def make_distance_nums(self):
        """
        Filling in the distance numbers of the maze for the bot's map
        :return: None
        """

        max_dist_index = DEFAULT_SIZE - 1
        half_dist_index = DEFAULT_SIZE // 2
        curr_dist = max_dist_index

        # Logic that populates the distance numbers to the maze
        for i in range(DEFAULT_SIZE):
            # use the previous starting row values if it's not the 1st iteration since the 1st iteration has a 0 at
            # my_map[0][0]
            if i != 0:
                curr_dist = self.map[i - 1][0].get_distance()
            for j in range(DEFAULT_SIZE):
                # Populating the first quadrant of the maze with the proper numbers
                square_obj = self.map[i][j]
                if i < half_dist_index:
                    if j < half_dist_index:
                        curr_dist -= 1
                        square_obj.set_distance(curr_dist)
                    # Copy all column numbers before the halfway column of the maze
                    else:
                        cpy_distance_cols = self.map[i][max_dist_index - j].get_distance()
                        square_obj.set_distance(cpy_distance_cols)
                # Copy all rows above the halfway row of the maze
                else:
                    cpy_distance_rows = self.map[max_dist_index - i][j].get_distance()
                    square_obj.set_distance(cpy_distance_rows)

    def make_starting_square(self):
        # Choice are (1) Top Left, (2) Bottom Left, (3) Top Right, (4) Bottom Right
        list_loc = [(0, 0), (0, DEFAULT_SIZE - 1), (DEFAULT_SIZE - 1, 0), (DEFAULT_SIZE - 1, DEFAULT_SIZE - 1)]

        x, y = random.choice(list_loc)
        # ****Should I make this a setter?
        self.map[x][y].is_start = True
        self.map[x][y].set_explore(True)
        # ****Should I make this a setter?
        self.map[x][y].bot_here = True

        # Saving bot's starting location in x and y coordinates
        self.bot_loc_x, self.bot_loc_y = x, y

    def make_walls_file(self):
        """
        This method makes a maze from a file. Currently, there's a maze stored on a machine
        called maze1.txt that housed the input or sequence of numbers to populate a 6x6 maze.
        :return: None
        """
        print(self.__str__())
        # Use distance numbers as a way to describe the number of walls you've changed per square

        filename = "maze1.txt"
        file1 = open(filename, "r")

        for line in file1.readlines():
            x, y, north_file, south_file, west_file, east_file = line.strip('\n').split()
            x = int(x)
            y = int(y)
            north_file = bool(int(north_file))
            south_file = bool(int(south_file))
            west_file = bool(int(west_file))
            east_file = bool(int(east_file))

            x_y_corr = x, y
            sq_obj = self.map[x][y]

            # Update dir_tuple to also contain any walls that may already be "True" from previous iteration
            north_og, south_og, west_og, east_og = sq_obj.get_walls()
            if north_og:
                north_file = north_og
            if south_og:
                south_file = south_og
            if west_og:
                west_file = west_og
            if east_og:
                east_file = east_og
            dir_tuple = north_file, south_file, west_file, east_file

            sq_obj.set_square(dir_tuple, False, 1)
            self.check_set_walls(dir_tuple, x_y_corr)

        file1.close()

    def make_walls_user(self):
        """
        A method to make a maze manually through user input. This can be prone to error
        if typing in incorrectly. Not built for error-avoidance.
        :return: None
        """
        print(self.__str__())
        # Use distance numbers as a way to describe the number of walls you've changed per square

        filename = ""
        file1 = open(filename, "a")

        user_input = input("What walls would you like to change (\"s\" or \"stop\" to stop)?\n"
                           "(Ex: x y north:[1\\0] south:[1\\0] west:[1\\0] east:[1\\0])\n"
                           "(1 means to put a wall, 0 means to remove a wall):\n")

        while user_input not in ["s", "stop"]:
            file1.write(user_input)
            file1.write("\n")
            user_list = user_input.split()

            x_y_corr = int(user_list[0]), int(user_list[1])
            x, y = x_y_corr
            dir_tuple = bool(int(user_list[2])), bool(int(user_list[3])), bool(int(user_list[4])), bool(
                int(user_list[5]))

            sq_obj = self.map[x][y]
            sq_obj.set_square(dir_tuple, False, 1)
            self.check_set_walls(dir_tuple, x_y_corr)

            print()
            print(self.__str__())
            print(f"You've changed: coordinate: {x}{y}\n\n{sq_obj}\n")

            user_input = input("What walls would you like to change (\"s\" or \"stop\" to stop)?\n"
                               "(Ex: x y north:[1\\0] south:[1\\0] west:[1\\0] east:[1\\0])\n"
                               "(1 means to put a wall, 0 means to remove a wall):\n")

        file1.close()

    def make_out_walls(self):
        """
        This will edit the maze's map to have squares that will
        have outside walls in its values

        :return: None
        """

        max_dist_index = DEFAULT_SIZE - 1

        # Condition for the outside walls
        num_squares = 0

        # Iteration happens by going in a clockwise direction but to do this you need to
        #   adjust the iterators for rows and columns as you go through it
        min_iterator_i = -1
        i = 0
        max_iterator_i = DEFAULT_SIZE
        flag_i = True

        min_iterator_j = -1
        j = 0
        max_iterator_j = 1
        flag_j = True

        # This flag is needed to skip over the first iteration so that it
        #   sets j = 0 when necessary.
        flag_j_zero = True

        # Skip over code if you're ready to exit
        flag_exit = False

        while num_squares < DEFAULT_SIZE ** 2 - (DEFAULT_SIZE - 2) ** 2:

            while min_iterator_i < i < max_iterator_i:
                if flag_j_zero:
                    j = 0
                elif j > max_dist_index:
                    j = max_dist_index
                while min_iterator_j < j < max_iterator_j:

                    north, south, west, east = False, False, False, False

                    # Top Left corner -> (0, 0)
                    if num_squares == 0:
                        north = True
                        west = True

                    # j will not change when going down the left outer wall
                    elif (max_dist_index * 0) < num_squares < (max_dist_index * 1):
                        west = True

                    # Bottom Left corner -> (5, 0)
                    elif num_squares == (max_dist_index * 1):
                        west = True
                        south = True
                        # update iterators
                        max_iterator_j = DEFAULT_SIZE
                        flag_j_zero = False

                    # The squares between Bottom Left corner -> Bottom Right corner
                    elif (max_dist_index * 1) < num_squares < (max_dist_index * 2):
                        south = True

                    # Bottom Right corner -> (5, 5)
                    elif num_squares == (max_dist_index * 2):
                        south = True
                        east = True
                        # update iterators
                        flag_i = not flag_i

                    # The squares between Bottom Right corner -> Top Right corner
                    elif (max_dist_index * 2) < num_squares < (max_dist_index * 3):
                        east = True

                    # Top Right corner -> (0, 5)
                    elif num_squares == (max_dist_index * 3):
                        east = True
                        north = True
                        # update iterators
                        flag_j = not flag_j

                    # The squares between Top Right corner -> Top Left corner
                    elif (max_dist_index * 3) < num_squares < (max_dist_index * 4):
                        north = True

                    else:
                        flag_exit = True

                    if not flag_exit:
                        dir_tuple = north, south, west, east
                        square_obj = self.map[i][j]
                        square_obj.set_walls(dir_tuple)
                        num_squares += 1

                    if flag_j:
                        j += 1
                    else:
                        j -= 1

                if flag_i:
                    i += 1
                else:
                    i -= 1

    def check_set_walls(self, dir_tuple, x_y_coor):
        """
        Check to see if the wall that is parallel to the set one is within bounds
            If it is, set the wall so the two parallel walls are true -> thus are one wall

        :param dir_tuple: direction tuple that holds as "north, south, west, east"
        :param x_y_coor: x and y coordinate tuple that will unpack to x, y
        :return: None
        """
        x, y = x_y_coor
        north, south, west, east = dir_tuple

        if north and -1 < (x - 1):
            square_obj_above = self.map[x - 1][y]
            square_obj_above.set_south(north)

        if south and (x + 1) < DEFAULT_SIZE:
            square_obj_below = self.map[x + 1][y]
            square_obj_below.set_north(south)

        if west and -1 < (y - 1):
            square_obj_left = self.map[x][y - 1]
            square_obj_left.set_east(west)

        if east and (y + 1) < DEFAULT_SIZE:
            square_obj_right = self.map[x][y + 1]
            square_obj_right.set_west(east)

    def set_distance_nums(self, bot_x, bot_y):
        """
        Recursion function for Flood-Fill Algorithm. This is for when the bot hits a wall
        and has to update its current square, and most likely, the square it could go to.
        :param bot_x: x or row location of the bot (int)
        :param bot_y: y or col location of the bot (int)
        :return: None
        """

        """
        If a cell is not the destination cell, its value should
        be one plus the minimum value of its open neighbors

        current cell/loc = min(neighbors not block by walls) + 1
        if change: check my neighbors not block by walls and repeat above
        else: return to previous square 
        """

        bot_map = self.map
        curr_sq = bot_map[bot_x][bot_y]
        curr_dist = curr_sq.get_distance()

        # dist_list -> distance list
        dist_list = []
        north, south, west, east = curr_sq.get_walls()

        # if there isn't a wall, then there's a neighboring cell to be checked thus add to dist_list
        if not north:
            dist_list.append(bot_map[bot_x - 1][bot_y].get_distance())
        if not south:
            dist_list.append(bot_map[bot_x + 1][bot_y].get_distance())
        if not west:
            dist_list.append(bot_map[bot_x][bot_y - 1].get_distance())
        if not east:
            dist_list.append(bot_map[bot_x][bot_y + 1].get_distance())

        # min function to determine minimum distance, even if there's repeats
        new_dist = min(dist_list) + 1

        # change is a variable to indicate if where the program is at, has a change square if so,
        #   then you need to check available neighboring squares;
        #   if not, return to previous square.
        change = True
        if curr_dist != new_dist:
            curr_sq.set_distance(new_dist)
        else:
            change = False

        # BASE CASE
        if not change:
            return
        # RECURSIVE CASES
        if not north:
            self.set_distance_nums(bot_x - 1, bot_y)
        if not south:
            self.set_distance_nums(bot_x + 1, bot_y)
        if not west:
            self.set_distance_nums(bot_x, bot_y - 1)
        if not east:
            self.set_distance_nums(bot_x, bot_y + 1)

    def set_bot_loc(self, bot_loc):
        self.bot_loc_x, self.bot_loc_y = bot_loc

    def get_bot_loc(self):
        return self.bot_loc_x, self.bot_loc_y

    def __str__(self):
        """
        Printing out the distance numbers of the maze in the format of a grid for Map class
        :return: a string to indicate what maze has been outputted (str)
        """
        for i in range(DEFAULT_SIZE):
            for j in range(DEFAULT_SIZE):
                print(self.map[i][j].get_distance(), end=' ')
            print()
        # Compiler yells for not returning string type
        return "Above is the maze's grid\n"

    def __getitem__(self, index_x_y):
        """
        Returns a square object at index_x and index_y location
        :param index_x_y: row and col value (tuple)
        :return: a square object (Square())
        """
        index_x, index_y = index_x_y
        return self.map[index_x][index_y]


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

    def get_walls(self):
        return self.w_north, self.w_south, self.w_west, self.w_east

    def get_explore(self):
        return self.is_explore

    def get_distance(self):
        return self.distance

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
        self.bot_map: Map = Map()
        self.bot_map.make_bot_map()

    def move(self, bot_new_x, bot_new_y, maze):
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
        maze.map[bot_new_x][bot_new_y].set_explore(True)
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


def run_flood_algo(bot, maze):
    """
    This is where the Flood-Fill algorithm and the arithmetic behind it is housed

    Flood-Fill Algo:
        Bot looks through all adjacent cells which aren't blocked by walls and choose the lowest distance values
        Turning take time thus if you have two choices, choose the one where the bot will not have to move much
        If run into a wall, update wall and distance values

    Flood-Fill Algorithm being used: Modified
    (There are better Flood-Fill Algorithms)

    :param bot: the bot object
    :param maze: the maze object
    :return: None(for now)
    """

    # Summary (in detail) of Flood-Fill Algo:
    #   Every time the mouse moves:
    #   Update the wall map
    #   Flood the maze with new distance values -> Modified version = flood the necessary values
    #   Decide which neighboring cell has the lowest distance value
    #   Move to the neighboring cell with the lowest distance value

    bot_map_obj = bot.bot_map
    bot_map = bot_map_obj.map
    # Starting location of bot (5, 5)
    x, y = bot_map_obj.get_bot_loc()
    """Assume it's in position to go straight from the start # Orientation Matters!!!"""
    distance = bot_map_obj[x, y].get_distance()
    """Can change to recursion: f(org_x, org_y, dir:int, dest_found/distance)"""
    while distance != 0:
        possible_dir = []

        north, south, west, east = bot_map_obj[x, y].get_walls()

        # Analyze choices:
        if -1 < (x - 1) and not north:
            if bot_map_obj[x - 1, y].get_distance() < distance:
                possible_dir.append(Direction.UP.value)
        if (x + 1) < DEFAULT_SIZE and not south:
            if bot_map_obj[x + 1, y].get_distance() < distance:
                possible_dir.append(Direction.DOWN.value)
        if -1 < (y - 1) and not west:
            if bot_map_obj[x, y - 1].get_distance() < distance:
                possible_dir.append(Direction.LEFT.value)
        if (y + 1) < DEFAULT_SIZE and not east:
            if bot_map_obj[x, y + 1].get_distance() < distance:
                possible_dir.append(Direction.RIGHT.value)
        """
        Determine a direction by randomly selecting between two (until orientation is an added attribute of bot
            class). If you do this, make sure there is a maze to test this orientation attribute thoroughly
        """
        """
        In reality, we would have a gyro or something to indicate the bot's orientation thus, that
          would be a factor in this decision        
        """

        dir_to_go = random.choice(possible_dir)

        # Printing output to see bot's value and bot's map distance values
        print("******************************************")
        for i in range(DEFAULT_SIZE):
            for j in range(DEFAULT_SIZE):
                num = bot_map_obj[i, j].get_distance()
                str_num = str(num)
                if len(str_num) == 1:
                    print(f" {str_num}", end='     ')
                else:
                    print(num, end='     ')
            print()

        print(f"Location: {(x, y)}")
        print(f"Walls: {bot_map_obj[x, y].get_walls()}")
        print(f"Directions possible: {possible_dir}")
        print(f"Distance: {distance}")
        print(f"Direction to go: {dir_to_go}")

        # Look in the actual maze for walls
        north_maze, south_maze, west_maze, east_maze = maze.map[x][y].get_walls()

        # Then tell the bot where to go in the actual maze
        # DIRECTION = UP
        if dir_to_go == 1:
            # If you don't hit the north wall -> move to that location in the algorithm
            if not north_maze:
                # Go bot
                x -= 1
                bot.move(x, y, maze)

            # If you hit the north wall -> update the north wall on the bot's map
            else:
                bot_map_obj[x, y].set_north(north_maze)
                dir_tuple = bot_map[x][y].get_walls()
                x_y_coor = x, y
                bot_map_obj.check_set_walls(dir_tuple, x_y_coor)

                # Update distance numbers for the bot and go again
                bot_map_obj.set_distance_nums(x, y)

        # DIRECTION = DOWN
        elif dir_to_go == 2:
            # If you don't hit the south wall -> move to that location in the algorithm
            if not south_maze:
                x += 1
                bot.move(x, y, maze)

            # If you hit the south wall -> update the south wall on the bot's map
            else:
                bot_map_obj[x, y].set_south(south_maze)
                dir_tuple = bot_map[x][y].get_walls()
                x_y_coor = x, y
                bot_map_obj.check_set_walls(dir_tuple, x_y_coor)

                # Update distance numbers for the bot and go again
                bot_map_obj.set_distance_nums(x, y)

        # DIRECTION = LEFT
        elif dir_to_go == 3:
            # If you don't hit the west wall -> move to that location in the algorithm
            if not west_maze:
                y -= 1
                bot.move(x, y, maze)

            # If you hit the west wall -> update the west wall on the bot's map
            else:
                bot_map_obj[x, y].set_west(west_maze)
                dir_tuple = bot_map[x][y].get_walls()
                x_y_coor = x, y
                bot_map_obj.check_set_walls(dir_tuple, x_y_coor)

                # Update distance numbers for the bot and go again
                bot_map_obj.set_distance_nums(x, y)

        # DIRECTION = RIGHT
        elif dir_to_go == 4:
            # If you don't hit the east wall -> move to that location in the algorithm
            if not east_maze:
                y += 1
                bot.move(x, y, maze)

            # If you hit the west wall -> update the west wall on the bot's map
            else:
                bot_map_obj[x, y].set_east(east_maze)
                dir_tuple = bot_map[x][y].get_walls()
                x_y_coor = x, y
                bot_map_obj.check_set_walls(dir_tuple, x_y_coor)

                # Update distance numbers for the bot and go again
                bot_map_obj.set_distance_nums(x, y)

        # Check if distances change and if they do, update maze
        # update distance for possible next iteration
        distance = bot.bot_map[x, y].get_distance()

        """Not sure if we need this but interface for Speedrun mode"""
        if distance == 0:
            bot_map_obj[x, y].is_dest = True

    # Printing output to see bot's value and bot's map distance values
    print("******************************************")
    for i in range(DEFAULT_SIZE):
        for j in range(DEFAULT_SIZE):
            num = bot_map_obj[i, j].get_distance()
            str_num = str(num)
            if len(str_num) == 1:
                print(f" {str_num}", end='     ')
            else:
                print(num, end='     ')
        print()

    print(f"Location: {(x, y)}")
    print(f"Walls: {bot_map_obj[x, y].get_walls()}")
    print(f"Distance: {distance}")


def run_depth_search_algo():
    """
    This is where the Depth First Search algorithm and the arithmetic behind it is housed Depth first search,
    bot goes -> intersection -> random direction -- if deadened --> go back to intersection -> repeat
    :return: None(for now)
    """
    pass


"""
If you were to go through the entire maze and using the flood-fill algorithm, it is guaranteed that you wil
find the SHORTEST path possible. But you would have to analyze the routes for the shortest possible one since,
the shortest route may have a lot of turns and the longest route may have no turns.
"""


def run_whole_maze_algo():
    """
    This is where the Whole Maze algorithm and the arithmetic behind it is housed whole-maze is similar to depth
    first search...We want to search as many possible paths and ideally get back to the start

    Looks for intersection and keeps looking for unexplored mazes

    :return: None(for now)
    """
    pass


if __name__ == "__main__":
    # Make an instance of Map to represent the actual maze
    maze_1 = Map()
    maze_1.make_maze_map()

    # Make a bot instance to represent the bot itself
    bot_1 = Bot()
    # Set the bot's starting square to the same starting square in the maze
    # Make the bot's map by populating with the distance numbers
    bot_map_obj = bot_1.bot_map
    bot_map_obj.set_bot_loc(maze_1.get_bot_loc())

    # Run the flood fill algorithm to test it
    run_flood_algo(bot_1, maze_1)
