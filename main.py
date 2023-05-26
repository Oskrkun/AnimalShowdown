# -*- coding: utf-8 -*-

from api.Game import *
from game.states.MenuState import *
from game.states.MatchManager import *
from game.states.LvConfiguration import *

# ============= Punto de entrada del programa. =============

g = Game()

initState = MenuState()

# initState = LvConfiguration()
#
# initState = MatchManager.inst()
# MatchManager.inst().startMatch(1, 1, 0, True)

g.setState(initState)
    
g.gameLoop()

g.destroy()
