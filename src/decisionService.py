'''
Cognitively Expanding The Game of Life
Spring 2023 Term Project
CS 6795 Intro to Cognitive Science

Team - Swole
Member - Scott Pickthorne
Member - Zackary Clark-Williams

@license
 Copyright [2023] [Scott Pickthorn and Zachary Clark-Williams]

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
 
'''

import random
import math
import numpy as np
from cell import *

EXP1_PROB = .60
neighboringCells = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,1],[1,0],[1,-1]]

# base experiment where we pick a random neighbor and a random choice whether to activate the cell or not
def decide():
    return random.choice(neighboringCells), random.choice([0,1])
# use the color of neighboring cells to pick the closest neighbor based n color
# give it a random probability of activating the cell (simulating mating)
def decideV2(currCell, grid):
    shortestDist = math.inf
    closestNeighbor = None
    # for each neighbor calculate the euclidean distance from the 3 dimensional point
    for neighbor in neighboringCells:
        if(grid[neighbor[0]][neighbor[1]].life == DEAD):
            currPoint = np.array(grid[currCell[0]][currCell[1]].state)
            neighborPoint = np.array(grid[neighbor[0]][neighbor[1]].state)
            squared_dist = np.sum((currPoint-neighborPoint)**2, axis=0)
            dist = np.sqrt(squared_dist)
            if dist < shortestDist:
                shortestDist = dist
                closestNeighbor = neighbor
    return closestNeighbor, random.choice([0,1])
