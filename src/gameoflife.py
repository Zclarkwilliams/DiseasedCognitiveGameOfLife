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
from conclusion import *
import decisionService
import argparse
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation

COLOR_BIAS = [0.5, 0.2, 0.0] # R, G, B biases against each change in next generation effect

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

def update(frameNum, img, N, grid, additionNum):
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
                if(additionNum > 0 and random.uniform(0,1) > decisionService.EXP1_PROB):
                    if(additionNum == 1):
                        updatedCell, activate = decisionService.decideV2([i,j], grid)
                    if(activate == 1):
                        newI = (i + updatedCell[0]) % N
                        newJ = (j + updatedCell[1]) % N
                        # print(newI, newJ, activate)
                        newImg[newI, newJ, :3] = grid[newI][newJ].state
                        continue
                if total in {2, 3}:
                    newImg[i,j,:3]     = grid[i][j].state
                else:
                    newImg[i, j, :3]   = DEAD
            else:
                if total == 3:
                    # First udate the color of the cell that will be brought to life
                    # Initialize color biasing
                    bias = COLOR_BIAS
                    for k in range (3):
                        # Rotate bias array to match born color to 0 and the other two to their bias setting
                        bias = [bias[-1]] + bias[0:-1]
                        
                        # Loop though neighborhood and average the color change by those that are bringing us to life
                        if grid[i][j].state[k] != 255:
                            grid[i][j].state[k] =  round ((grid[i][(j-1)%N].life * sum([grid[i][(j-1)%N].state[l] * bias[l] for l in range(3)]) + \
                                                           grid[i][(j+1)%N].life * sum([grid[i][(j+1)%N].state[l] * bias[l] for l in range(3)]) + \
                                                           grid[(i-1)%N][j].life * sum([grid[(i-1)%N][j].state[l] * bias[l] for l in range(3)]) + \
                                                           grid[(i+1)%N][j].life * sum([grid[(i+1)%N][j].state[l] * bias[l] for l in range(3)]) + \
                                                           grid[(i-1)%N][(j-1)%N].life * sum([grid[i][j].state[l] * bias[l] for l in range(3)]) + \
                                                           grid[(i-1)%N][(j+1)%N].life * sum([grid[i][j].state[l] * bias[l] for l in range(3)]) + \
                                                           grid[(i+1)%N][(j-1)%N].life * sum([grid[i][j].state[l] * bias[l] for l in range(3)]) + \
                                                           grid[(i+1)%N][(j+1)%N].life * sum([grid[i][j].state[l] * bias[l] for l in range(3)])) / 3)
                    
                    # Set the new image cell RGB color to the updated coloring
                    newImg[i,j,:3] = grid[i][j].state

    # Update the cell world data to match the new life and death setting
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
	
	# Clip image data to fit matlab plot values of 0..255
    for k in range (3):
        newImg[:N, :N, k] = newImg[:N, :N, k] / np.max(newImg[:N, :N, k])
    
    # Set the new world grid to image data
    img.set_data(newImg)
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
    parser.add_argument('--addition', dest='addition', required=False, default=0)
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

    # set up animation
    matplotlib.use('TkAgg')
    fig, ax = plt.subplots()
    img = ax.imshow(imgGrid, interpolation='nearest')
    ani = animation.FuncAnimation(fig,
                                  update, 
                                  fargs     = (img, N, grid, int(args.addition), ),
                                  frames    = frames,
                                  interval  = updateInterval,
                                  blit      = True,
                                  repeat    = False)

    # # of frames?
    # set output file
    if args.movfile:
        ani.save(args.movfile, fps=30, extra_args=['-vcodec', 'libx264'])
    plt.show(block=True)

    conclusion.getAverageLifeSpan (grid, N)
    conclusion.getMaxLifespan (grid, N)

# call main
if __name__ == '__main__':
    main()
