'''
Cognitively Expanding The Game of Life
Spring 2023 Term Project
CS 6795 Intro to Cognitive Science

Team - Swole
Member - Scott Pickthorne
Member - Zackary Clark-Williams

@citation
Referenced basic Game of Life Code -
    <https://www.geeksforgeeks.org/conways-game-life-python-implementation/>
 
'''

# Python code to implement Conway's Game Of Life
from cell import *
import time
import argparse
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation

COLOR_BIAS = [0, 0.4, 0.1]

def generateWorld(N):
    return [[cell(cell.rndLife(), cell.rndColorState()) for i in range(N)] for k in range(N)]

def getGrid(grid, N):
    newGrid = np.zeros(shape=(N,N,3))
    for i in range(len(grid)):
        for j in range(i):
            for k in range(0,2):
                newGrid[i,j,k] = grid[i][j].state[k]
    return newGrid

def update(frameNum, img, imgGrid, N, grid):

    # Copy grid to generate the image to print vs. the data packed cell world
    newGrid = np.zeros(shape=(N,N,3))

    # For calculation and we go line by line
    for i in range(N):
        for j in range(N):
            # compute 8-neighbor sum
            # using toroidal boundary conditions - x and y wrap around
            # so that the simulation takes place on a toroidal surface.
            total = int((grid[i][(j-1)%N].life + grid[i][(j+1)%N].life +
                         grid[(i-1)%N][j].life + grid[(i+1)%N][j].life +
                         grid[(i-1)%N][(j-1)%N].life + grid[(i-1)%N][(j+1)%N].life +
                         grid[(i+1)%N][(j-1)%N].life + grid[(i+1)%N][(j+1)%N].life))

            # apply Conway's rules
            if grid[i][j].life == ALIVE:
                if (total < 2) or (total > 3):
                    newGrid[i, j, :3] = DEAD
                    grid[i][j].life   = DEAD
            else:
                if total == 3:
                    for k in range(0, 3):
                        newGrid[i,j,k]      = grid[i][j].state[k]
                        grid[i][j].life     = ALIVE
                        grid[i][j].state[k] = (grid[i][(j-1)%N].life * grid[i][j].state[k] * COLOR_BIAS[k] + \
                                               grid[i][(j+1)%N].life * grid[i][j].state[k] * COLOR_BIAS[k] + \
                                               grid[(i-1)%N][j].life * grid[i][j].state[k] * COLOR_BIAS[k] + \
                                               grid[(i+1)%N][j].life * grid[i][j].state[k] * COLOR_BIAS[k] + \
                                               grid[(i-1)%N][(j-1)%N].life * grid[i][j].state[k] * COLOR_BIAS[k] + \
                                               grid[(i-1)%N][(j+1)%N].life * grid[i][j].state[k] * COLOR_BIAS[k] + \
                                               grid[(i+1)%N][(j-1)%N].life * grid[i][j].state[k] * COLOR_BIAS[k] + \
                                               grid[(i+1)%N][(j+1)%N].life * grid[i][j].state[k] * COLOR_BIAS[k]) / 3

    # update data
    img.set_data(newGrid)
    #img.set_data(np.clip(newGrid, 0, 1))
    imgGrid[:] = newGrid[:]
    return (img,)

def main():
    # Command line args are in sys.argv[1], sys.argv[2] ..
    # sys.argv[0] is the script name itself and can be ignored
    # parse arguments
    parser = argparse.ArgumentParser(description="Runs Conway's Game of Life simulation.")

    # add arguments
    parser.add_argument('--grid-size', dest='N', required=False)
    parser.add_argument('--mov-file', dest='movfile', required=False)
    parser.add_argument('--interval', dest='interval', required=False)
    parser.add_argument('--frames', dest='frames', required=False)
    args = parser.parse_args()
    
    # set iteration count
    frames = 1000
    if args.frames and int(args.frames) > 100:
        frames = int(args.frames)
    
    # set grid size
    N = 1000
    if args.N and int(args.N) > 8:
        N = int(args.N)
        
    # set animation update interval
    updateInterval = 500
    if args.interval:
        updateInterval = int(args.interval)

    # declare grid
    grid = np.array([])
    # populate grid with random on/off - more off than on
    grid = generateWorld(N)
    imgGrid = getGrid(grid,N)
    print(imgGrid.shape)

    # set up animation
    matplotlib.use('TkAgg')
    fig, ax = plt.subplots()
    img = ax.imshow(imgGrid, interpolation='nearest')
    ani = animation.FuncAnimation(fig,
                                  update, 
                                  fargs=(img, imgGrid, N, grid,),
                                  #frames=frames,
                                  interval=updateInterval,
                                  save_count=100,
                                  blit = True,
                                  repeat=True)

    # # of frames?
    # set output file
    if args.movfile:
        ani.save(args.movfile, fps=30, extra_args=['-vcodec', 'libx264'])

    plt.show(block=True)

# call main
if __name__ == '__main__':
    main()
