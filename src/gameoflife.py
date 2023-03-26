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
import argparse
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def getGrid(grid, N):
    newGrid = np.zeros(shape=(N,N,3))
    for i in range(len(grid)):
        for j in range(i):
            for k in range(0,2):
                newGrid[i,j,k] = grid[i][j].state[k]
    return newGrid

# Randomize who is alive and bias towards dead
def rndLife():
    return np.random.choice(LIFE_STATES, p=[0.2, 0.8])

# Randomize the color state of each cell R, G, or B
def rndColorState():
    sample = random.sample(COLOR_STATE, len(COLOR_STATE))
    return (sample[0], sample[1], sample[2])

def generateWorld(N):
    return [[cell(rndLife(), rndColorState()) for i in range(N)] for k in range(N)]

def update(frameNum, img, imgGrid, N, grid):

    # copy grid since we require 8 neighbors
    # for calculation and we go line by line
    newGrid = np.zeros(shape=(N,N,3))
    for i in range(N):
        for j in range(N):

            # compute 8-neighbor sum
            # using toroidal boundary conditions - x and y wrap around
            # so that the simulation takes place on a toroidal surface.
            total = int((grid[i][(j-1)%N].life + grid[i][(j+1)%N].life +
                         grid[(i-1)%N][j].life + grid[(i+1)%N][j].life +
                         grid[(i-1)%N][(j-1)%N].life + grid[(i-1)%N][(j+1)%N].life +
                         grid[(i+1)%N][(j-1)%N].life + grid[(i+1)%N][(j+1)%N].life)/255)

            # apply Conway's rules
            if grid[i][j] == 1:
                if (total < 2) or (total > 3):
                    newGrid[i, j, 0:2] = 0
            else:
                if total == 3:
                    for k in range(0,2):
                        newGrid[i,j,k] = grid[i][j].state[k]

    # update data
    img.set_data(newGrid)
    #img.set_data(np.clip(newGrid, 0, 1))
    print(newGrid)
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
    frames = 100
    if args.frames and int(args.frames) > 100:
        frames = int(args.frames)
    
    # set grid size
    N = 1000
    if args.N and int(args.N) > 8:
        N = int(args.N)
        
    # set animation update interval
    updateInterval = 50
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
                                  frames=1,
                                  interval=updateInterval,
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
