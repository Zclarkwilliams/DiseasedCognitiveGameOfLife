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

class conclusion:
    
    def getAverageLifeSpan (grid):
        colavg = 0
        for i in range(N):
            rowavg = 0
            for j in range(N):
                rowavg += grid[i][j].avgLifespan
            colavg += (rowavg / N)
        colavg = round (colavg / N)
        print(colavg)