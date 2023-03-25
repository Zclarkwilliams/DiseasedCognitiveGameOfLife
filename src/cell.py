'''
Cognitively Expanding The Game of Life
Spring 2023 Term Project
CS 6795 Intro to Cognitive Science

Team - Swole
Member - Scott Pickthorne
Member - Zackary Clark-Williams
'''

import random
import numpy as np
from dataclasses import dataclass, field

# setting up the values for the grid
LIFE_STATES = [1, 0]    # life or death states life = 1 and death = 0
COLOR_STATE = [255,0,0] # color order as [R, G, B] values 0 - 255

# Automata structure
@dataclass
class cell:
    _life:  int
    _state: list(COLOR_STATE)

    @property
    def life (self) -> int:
        return self._life
    
    @life.setter
    def life (self, life:int) -> None:
        self._life = life
        
    @property
    def state (self) -> list:
        return self._state
    
    @state.setter
    def state (self, state:list) -> None:
        self._state = state

#    def __array__ (self):
#        return np.array(astuple(self))