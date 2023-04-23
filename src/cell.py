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
import numpy as np
from dataclasses import dataclass, field

# setting up the values for the grid
ALIVE = 1
DEAD  = 0
LIFE_STATES = [ALIVE, DEAD]     # life or death states life = 1 and death = 0
COLOR_STATE = [255, 0, 0]       # color order as [R, G, B] values 0 - 255

# Automata structure
@dataclass
class cell:
    _life:          int
    _lifespan:      int
    _avgLifespan:   int
    _state:         list(COLOR_STATE)

    @property
    def life (self) -> int:
        return self._life
    
    @life.setter
    def life (self, life:int) -> None:
        self._life = life

    @property
    def lifespan (self) -> int:
        return self._lifespan
    
    @lifespan.setter
    def lifespan (self, lifespan:int) -> None:
        self._lifespan = lifespan

    @property
    def avgLifespan (self) -> int:
        return self._avgLifespan
    
    @avgLifespan.setter
    def avgLifespan (self, avgLifespan:int) -> None:
        self._avgLifespan = avgLifespan

    @property
    def state (self) -> list:
        return self._state
    
    @state.setter
    def state (self, state:list) -> None:
        self._state = state

    # Randomize who is alive and bias towards dead
    def rndLife():
        return np.random.choice(LIFE_STATES, p=[0.2, 0.8])

    # Randomize the color state of each cell R, G, or B
    def rndColorState():
        return random.sample(COLOR_STATE, len(COLOR_STATE))