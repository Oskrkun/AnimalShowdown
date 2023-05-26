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
from game.Characters.Character import *
from api.GameConstants import *


class FireballPower(AnimatedSprite):
    # Máquina de estados.
    NORMAL = 0

    #aRuta1 es la ruta de los frames de la animacion normal aRuta2 son cuando le hacen click se le pasa un ancho y alto a los botones para escalarlos y si es animacion ciclica o no
    def __init__(self, char):
        Sprite.__init__(self)

        self.ciclico = True
        self.delay = 2
        self.char = char
        self.playerSide = char.playerNumber
        self.speed = 30 * GameConstants.inst().SCALE
        self.sc = GameConstants.inst().SCALE

        self.setRegistration(self.CENTER)

        self.framePower = AssetManager.inst().Powers[self.playerSide][self.char.charID]

        # Tamaño de los botones
        self.mWidth = self.framePower[0].get_width()
        self.mHeight = self.framePower[0].get_height()

        self.loadCollitionZone(int(30 * GameConstants.inst().SCALE), int(30 * GameConstants.inst().SCALE))

        if self.playerSide == 1:
            self.setXY(char.collidesZoneBody.getX() + 150, char.collidesZoneBody.getY())
        if self.playerSide == 2:
            self.setXY(char.collidesZoneBody.getX() - 150, char.collidesZoneBody.getY())


        # Estado inicial.
        self.setState(FireballPower.NORMAL)


    def update(self):
        from game.states.MatchManager import MatchManager
        AnimatedSprite.update(self)
        self.collidesZone.setXY(self.getX(), self.getY())

        if self.playerSide == 1:
            self.setVelX(self.speed)
        if self.playerSide == 2:
            self.setVelX(-self.speed)

    def render(self, aScreen):
        AnimatedSprite.render(self, aScreen)
        self.collidesZone.render(aScreen)

    def setState(self, aState):
        AnimatedSprite.setState(self, aState)
        self.initAnimation(self.framePower, 0,len(self.framePower)-1,  self.delay, self.ciclico)

    def loadCollitionZone(self, czW, czH):
        self.collidesZone = Reference()
        self.collidesZone.setImage(pygame.transform.scale(self.collidesZone.mImg, (czW, czH)))
        self.collidesZone.setXY(self.getX(), self.getY())

    def destroy(self):
        AnimatedSprite.destroy(self)

        i = len(self.framePower)
        while i > 0:
            self.framePower[i - 1] = None
            self.framePower.pop(i - 1)
            i = i - 1