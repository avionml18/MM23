# MM23
CPU Pseudocoding
2 sections: robot operation (interfacing with motors/sensors) and solving/map building
robot op

can be C or Python. timing not super critical, so python may be easier

each square of maze, take measurement of wall locations and store in text file memory. use discover algorithm to move to next square

at center change to return to start mode
different algorithm to find another path?

reversing original algorithm will likely lead to taking same path back to start
take same measurements on way back to beginning

in speedrun mode
no measurements. read text file of instructions and operate as fast as possible

Algorithms

Discover: Flood Algorithm
Each square has a distance away from the goal. when faced with a decision, take square that is closer to finish, if hit dead end, retrace back to last open decision

Return to Start: Whole Maze
we can pick up bot without penalty, may as well let it explore as much as possible until we decide its discovered enough

Ideal Route/Speedrun: Dynamic Programming
optimal substructure
optimal route to end consists of optimal route to earlier squares
n^2 runtime to solve maze
