# -*- coding: utf-8 -*-


from api.AnimatedSprite import *
from pygame import *
from api.Keyboard import *
from api.GameConstants import *
from api.AudioManager import *
from game.GameData import *


class Particles(AnimatedSprite):
    # Máquina de estados.
    NORMAL = 0

    #aRuta1 es la ruta de los frames de la animacion normal aRuta2 son cuando le hacen click se le pasa un ancho y alto a los botones para escalarlos y si es animacion ciclica o no
    def __init__(self, aArray, aCiclo, aDelay):

        Sprite.__init__(self)


        self.ciclico = aCiclo
        self.delay = aDelay

        self.mFramesNormal = aArray

        #tamaño de los botones
        self.mWidth = self.mFramesNormal[0].get_width()
        self.mHeight = self.mFramesNormal[0].get_height()

        # Estado inicial.
        self.mState = Particles.NORMAL
        self.setState(Particles.NORMAL)

    def update(self):
        AnimatedSprite.update(self)

        if self.isEnded():
            self.die()

    def render(self, aScreen):
        AnimatedSprite.render(self, aScreen)

    def setState(self, aState):
        AnimatedSprite.setState(self, aState)

        self.initAnimation(self.mFramesNormal, 0, len(self.mFramesNormal)-1,  self.delay, self.ciclico)

    def destroy(self):
        AnimatedSprite.destroy(self)

        i = len(self.mFramesNormal)
        while i > 0:
            self.mFrames[i - 1] = None
            self.mFrames.pop(i - 1)
            i = i - 1