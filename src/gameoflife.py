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
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Randomize who is alive and bias towards dead
def rndLife():
    return np.random.choice(LIFE_STATES, p=[0.2, 0.8])

# Randomize the color state of each cell R, G, or B
def rndColorState():
    return random.sample(COLOR_STATE, len(COLOR_STATE))

def generateWorld(N):
    return [[cell(rndLife(), rndColorState()) for i in range(N)] for k in range(N)]

def update(frameNum, img, grid, N):

    # copy grid since we require 8 neighbors
    # for calculation and we go line by line
    newGrid = grid.copy()
    for i in range(N):
        for j in range(N):

            # compute 8-neighbor sum
            # using toroidal boundary conditions - x and y wrap around
            # so that the simulation takes place on a toroidal surface.
            total = int((grid[i, (j-1)%N] + grid[i, (j+1)%N] +
                        grid[(i-1)%N, j] + grid[(i+1)%N, j] +
                        grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, (j+1)%N] +
                        grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N])/255)

            # apply Conway's rules
            if grid[i, j] == ON:
                if (total < 2) or (total > 3):
                    newGrid[i, j] = OFF
            else:
                if total == 3:
                    newGrid[i, j] = ON

    # update data
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img

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
    frames = 1
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
    initGrid = np.random.random((N,N))
    # populate grid with random on/off - more off than on
    grid = generateWorld(N)
    print(grid)

    # set up animation
    fig, ax = plt.subplots()
    img = ax.imshow(initGrid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, ),
                                frames=frames,
                                interval=updateInterval,
                                save_count=50,
                                repeat=False)

    # # of frames?
    # set output file
    if args.movfile:
        ani.save(args.movfile, fps=30, extra_args=['-vcodec', 'libx264'])

    plt.show()

# call main
if __name__ == '__main__':
    main()
