import random

EXP1_PROB = .8

def decide():
    # to start choose a random neighbor, and a random choice whether to activate it or not
    return random.choice([[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,1],[1,0],[1,-1]]), random.choice([0,1])