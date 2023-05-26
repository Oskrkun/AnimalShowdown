# -*- coding: utf-8 -*-


from api.AnimatedSprite import *
from pygame import *
from api.Keyboard import *
from api.GameConstants import *
from api.AudioManager import *
from game.GameData import *
from  api.AssetManager import *
from game.states.MatchManager import *
from game.Reference import *


class TwisterPower(AnimatedSprite):
    # Máquina de estados.
    NORMAL = 0

    # aRuta1 es la ruta de los frames de la animacion normal aRuta2 son cuando le hacen click se le pasa un ancho y alto a los botones para escalarlos y si es animacion ciclica o no
    def __init__(self, char):
        Sprite.__init__(self)

        self.ciclico = False
        self.delay = 2
        self.char = char
        self.playerSide = char.playerNumber
        self.framePower = AssetManager.inst().Powers[self.playerSide][2]

        # Tamaño de los botones
        self.mWidth = self.framePower[0].get_width()
        self.mHeight = self.framePower[0].get_height()
        self.loadCollitionZone(20, int(self.mHeight / 2))

        # Estado inicial.
        self.setState(TwisterPower.NORMAL)

    def update(self):
        from game.states.MatchManager import MatchManager
        AnimatedSprite.update(self)

        if self.playerSide == 1:
            self.collidesZone.setXY(self.getX() + self.char.collidesZoneBody.getWidth()*0.50, self.getY())
        elif self.playerSide == 2:
            self.collidesZone.setXY(self.getX() - self.char.collidesZoneBody.getWidth()*0.50, self.getY())

        # aca paso a estado hold si choco contra el disco y estoy en estado normal
        if self.collidesZone.collides(MatchManager.inst().Disk):
            if MatchManager.inst().Disk.getState() == MatchManager.inst().Disk.NORMAL:
                if self.playerSide == 1:
                    MatchManager.inst().Disk.setX(self.collidesZone.getX() + MatchManager.inst().Disk.getWidth() + 1)
                    MatchManager.inst().Disk.invDir()
                elif self.playerSide == 2:
                    MatchManager.inst().Disk.setX(self.collidesZone.getX() - MatchManager.inst().Disk.getWidth() - 1)
                    MatchManager.inst().Disk.invDir()

    def render(self, aScreen):
        AnimatedSprite.render(self, aScreen)
        self.collidesZone.render(aScreen)

    def setState(self, aState):
        AnimatedSprite.setState(self, aState)
        self.initAnimation(self.framePower, 0, len(self.framePower)-1, self.delay, self.ciclico)

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