'''
Created on Oct 25, 2023

@author: Timbo
'''
class Square:
    WallNorth = 0
    WallSouth = 0
    WallWest = 0
    WallEast = 0
    Start = 0
    Finish = 0
    ShortestPath = 14
    Explored = 1   

mazeSize = 4
maze = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
for i in range(4):
    for j in range(4):
        maze[i][j] = Square()
maze[0][0].Start = 1
maze[3][3].Finish = 1
for i in range(4):
    maze[i][0].WallNorth = 1
    maze[i][3].WallSouth = 1
    maze[0][i].WallWest = 1
    maze[3][i].WallEast = 1
maze[0][0].WallSouth = 1
maze[2][0].WallSouth = 1
maze[0][1].WallNorth = 1
maze[0][1].WallEast = 1
maze[1][1].WallWest = 1
maze[1][1].WallSouth = 1
maze[2][1].WallNorth = 1
maze[2][1].WallEast = 1
maze[3][1].WallWest = 1
maze[1][2].WallNorth = 1
maze[1][2].WallSouth = 1
maze[2][2].WallSouth = 1
maze[2][2].WallEast = 1
maze[3][2].WallWest = 1
maze[3][2].WallSouth = 1
maze[1][3].WallNorth = 1
maze[2][3].WallNorth = 1
maze[3][3].WallNorth = 1

directions = ['X']*(mazeSize*mazeSize)
instructions = ['X']*maze[3][3].ShortestPath

if __name__ == '__main__':
    speedrun(0,0,0) #param is starting location and current shortest path (0)
    for i in range(4):
        #for j in range(4):
        print(maze[0][i].ShortestPath, maze[1][i].ShortestPath, maze[2][i].ShortestPath, maze[3][i].ShortestPath)
    generate_directions(3,3)#param is location of finish
    print(directions)
    generate_instructions(3,3)#param is the location of the finish block
    print(instructions)


