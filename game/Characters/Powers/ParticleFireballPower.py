# -*- coding: utf-8 -*-


from api.AnimatedSprite import *
from pygame import *
from api.Keyboard import *
from api.GameConstants import *
from api.AudioManager import *
from game.GameData import *
from api.AssetManager import *
from game.states.MatchManager import *
from game.Reference import *
from api.GameConstants import *


class ParticleFireballPower(AnimatedSprite):
    # Máquina de estados.
    NORMAL = 0

    #aRuta1 es la ruta de los frames de la animacion normal aRuta2 son cuando le hacen click se le pasa un ancho y alto a los botones para escalarlos y si es animacion ciclica o no
    def __init__(self, char):
        Sprite.__init__(self)

        self.ciclico = False
        self.delay = 2
        self.char = char
        self.playerSide = char.playerNumber

        self.framePower = AssetManager.inst().PowerParticles[self.playerSide][self.char.charID]

        self.setRegistration(self.CENTER)

        # Tamaño de los botones
        self.mWidth = self.framePower[0].get_width()
        self.mHeight = self.framePower[0].get_height()

        # Estado inicial.
        self.setState(ParticleFireballPower.NORMAL)

    def update(self):
        AnimatedSprite.update(self)

    def render(self, aScreen):
        AnimatedSprite.render(self, aScreen)

    def setState(self, aState):
        AnimatedSprite.setState(self, aState)
        self.initAnimation(self.framePower, 0,len(self.framePower)-1,  self.delay, self.ciclico)

    def destroy(self):
        AnimatedSprite.destroy(self)

        i = len(self.framePower)
        while i > 0:
            self.framePower[i - 1] = None
            self.framePower.pop(i - 1)
            i = i - 1