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

COLOR_BIAS = [0, 0.4, 0.1]

def generateWorld(N):
    ##
    # Randomize cell initialize structure:
    #  Cell [ [Alive or Dead],
    #         [Iterations Been Alive],
    #         [Average Lifespan],
    #         [R_Color_State, G_Color_State, B_Color_State] ]
    ## 
    return [[cell(cell.rndLife(), 0, 0, cell.rndColorState()) for i in range(N)] for k in range(N)]

def getGrid(grid, N):
    livecount = 0
    newGrid = np.zeros(shape=(N,N,3))
    for i in range(N):
        for j in range(N):
            for k in range(3):
                if grid[i][j].life == ALIVE:
                    newGrid[i,j,k] = grid[i][j].state[k]
    if k == 0:
        livecount += 1
    return newGrid

def update(frameNum, img, N, grid):
    #plt.pause(1)
    # Copy grid to generate the image to print vs. the data packed cell world
    newImg = np.zeros(shape=(N,N,3))
    # For calculation and we go line by line
    for i in range(N):
        for j in range(N):
            # compute 8-neighbor sum
            # using toroidal boundary conditions - x and y wrap around
            # so that the simulation takes place on a toroidal surface.
            total = grid[i][(j-1)%N].life + grid[i][(j+1)%N].life +             \
                    grid[(i-1)%N][j].life + grid[(i+1)%N][j].life +             \
                    grid[(i-1)%N][(j-1)%N].life + grid[(i-1)%N][(j+1)%N].life + \
                    grid[(i+1)%N][(j-1)%N].life + grid[(i+1)%N][(j+1)%N].life

            # apply Conway's rules
            if grid[i][j].life == ALIVE:
                if total in {2, 3}:
                    newImg[i,j,:3]     = grid[i][j].state
                else:
                    newImg[i, j, :3]   = DEAD
            else:
                if total == 3:
                    newImg[i,j,:3]     = grid[i][j].state
                '''
                        if grid[i][j].state[k] != 255:
                            grid[i][j].state[k] = (grid[i][(j-1)%N].life * (grid[i][(j-1)%N].state[k] * COLOR_BIAS[k]) + \
                                                grid[i][(j+1)%N].life * (grid[i][(j+1)%N].state[k] * COLOR_BIAS[k]) + \
                                                grid[(i-1)%N][j].life * (grid[(i-1)%N][j].state[k] * COLOR_BIAS[k]) + \
                                                grid[(i+1)%N][j].life * (grid[(i+1)%N][j].state[k] * COLOR_BIAS[k]) + \
                                                grid[(i-1)%N][(j-1)%N].life * (grid[i][j].state[k] * COLOR_BIAS[k]) + \
                                                grid[(i-1)%N][(j+1)%N].life * (grid[i][j].state[k] * COLOR_BIAS[k]) + \
                                                grid[(i+1)%N][(j-1)%N].life * (grid[i][j].state[k] * COLOR_BIAS[k]) + \
                                                grid[(i+1)%N][(j+1)%N].life * (grid[i][j].state[k] * COLOR_BIAS[k])) / 3
                        '''
    for i in range(N):
        for j in range(N):
            if int(newImg[i, j].sum(0)) == 0:
                grid[i][j].life     = DEAD
                # Update average lifespan
                grid[i][j].avgLifespan = round ((grid[i][j].avgLifespan + grid[i][j].lifespan) / 2)
            else:
                grid[i][j].life     = ALIVE
                # Accumulate lifespan tracker
                grid[i][j].lifespan += 1
	
	# update data
    img.set_data(newImg)
    #img.set_data(np.clip(newGrid, 0, 1))
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
    if args.frames and int(args.frames) >= 100:
        frames = int(args.frames)
    
    # set grid size
    N = 100
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
    #print('\n'.join(['\t'.join([str(cl) for cl in row]) for row in grid]))
    #print('\n'.join(['\t'.join([str(cll) for cll in row1]) for row1 in imgGrid]))

    # set up animation
    matplotlib.use('TkAgg')
    fig, ax = plt.subplots()
    img = ax.imshow(imgGrid, interpolation='nearest')

    ani = animation.FuncAnimation(fig,
                                  update, 
                                  fargs     = (img, N, grid,),
                                  frames    = frames,
                                  interval  = updateInterval,
                                  blit      = True,
                                  repeat    = False)

    # # of frames?
    # set output file
    if args.movfile:
        ani.save(args.movfile, fps=30, extra_args=['-vcodec', 'libx264'])
    plt.show(block=True)

    conclusion.getAverageLifeSpan (grid)

# call main
if __name__ == '__main__':
    main()
