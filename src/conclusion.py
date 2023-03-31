'''
Cognitively Expanding The Game of Life
Spring 2023 Term Project
CS 6795 Intro to Cognitive Science

Team - Swole
Member - Scott Pickthorne
Member - Zackary Clark-Williams


This class is the data form for all the experiments
tracking data.

Information Currently Tracking:
    Average Cellurlar Life Span,
    ...

'''
import numpy as np

class conclusion:
    
    def getMaxLifespan (grid, N):
        max_val = -np.inf
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                max_val = max(max_val, np.max(grid[i][j].avgLifespan))
        print(max_val)
        return max_val
    
    def getAverageLifeSpan (grid, N):
        avg = 0
        iWasAlive = 0
        for i in range(N):
            rowavg = 0
            for j in range(N):
                rowavg += grid[i][j].avgLifespan
                if grid[i][j].avgLifespan > 0: iWasAlive +=1
            avg += (rowavg / iWasAlive)
        avg = round (avg / N)
        print(avg)
        return avg