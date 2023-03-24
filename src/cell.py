import random
import numpy as np
from dataclasses import dataclass, field

# setting up the values for the grid
LIFE_STATES = [True, False]
COLOR_STATE = [255,0,0,0] # color order as R,G,Y,B

# Automata structure
@dataclass
class cell:
    _life:  bool
    _state: list(COLOR_STATE)

    @property
    def life (self) -> bool:
        return self._life
    
    @life.setter
    def life (self, life:bool) -> None:
        self._life = life
        
    @property
    def state (self) -> list:
        return self._state
    
    @state.setter
    def state (self, state:list) -> None:
        self._state = state