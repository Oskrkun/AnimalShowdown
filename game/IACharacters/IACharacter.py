# -*- coding: utf-8 -*-

from api.AnimatedSprite import *
from pygame import *
from api.Keyboard import *
from api.GameConstants import *
from api.AudioManager import *
from game.GameData import *
from api.Vector import *
from api.AssetManager import *
from api.Console import *
from game.states.MatchManager import *
from game.Reference import *
from game.Characters.Powers.TwisterPower import *
from api.AssetAnimated import *
import math

class IACharacter(AnimatedSprite):

    AFTER_STATE = 0
    NORMAL = 0
    HOLD = 1
    THROW = 2
    DASH = 3
    STUN = 4
    CHEER = 5
    POWER = 6

    LEFT = 1.1
    RIGHT = 2.1
    UP = 3.1
    DOWN = 4.1

    """Tiempos que duran los estados."""
    TIME_HOLD = 10
    TIME_STUN = 90
    stateFrames = 0

    """Controles"""
    Move_UP = None
    Move_DOWN = None
    Move_LEFT = None
    Move_RIGHT = None
    A = None
    B = None

    charID = 0
    Speed = 10

    def __init__(self, playerNumber):

        AnimatedSprite.__init__(self)

        self.playerNumber = playerNumber

        """[ID_Character][Player/Side][State][Animation]"""
        self.mFrames = AssetManager.inst().Characters[self.charID][self.playerNumber][self.NORMAL][self.NORMAL]

        self.mWidth = self.mFrames[0].get_width()
        self.mHeight = self.mFrames[0].get_height()

        self.mState = self.NORMAL

        self.screenWidth = GameConstants.inst().SCREEN_WIDTH
        self.screenHeight = GameConstants.inst().SCREEN_HEIGHT
        self.sc = GameConstants.inst().SCALE

        """-------objeto del stado stun-------"""
        self.PajaritoStun = AssetManager.inst().loadAssets("assets/images/Characters/stun/", "stun_", self.sc)
        self.PajaritoStun = AssetAnimated(self.PajaritoStun, True, 10)
        self.PajaritoStun.setXY(self.getX(), self.getY())
        self.renderStun = False
        """-----------------------------------"""

        self.joystick = None

        self.Name = ""
        self.mState = self.NORMAL
        self.lastMove = self.NORMAL
        self.lastMoveDir = self.RIGHT
        self.v = Vector()
        self.setXY(self.v.getX(), self.v.getY())
        self.setBoundAction(GameObject.STOP)
        self.Strength = 5

        self.Energy = 0
        self.PowerChargeFrames = 0
        self.EnergyFrames = 0

        self.AFTER_STATE = 0

        self.disk = None
        self.catch = False

        self.newVector = Vector()
        self.loadGiro()

        self.PowerObj = None

        if self.playerNumber == 2:
            self.giro.setAngle(180)
            self.angulos = [180, 165, 150, 135, 120, 195, 210, 225, 240]
        if self.playerNumber == 1:
            self.giro.setAngle(180)
            self.angulos = [0, 15, 30, 45, 60, 345, 330, 315, 300]

    def update(self):
        from game.states.MatchManager import MatchManager
        AnimatedSprite.update(self)

        self.PajaritoStun.setXY(self.getX(), self.getY() - self.getHeight() / 2)
        self.PajaritoStun.update()

        self.giro.setXY(self.getX(), self.getY() - int(self.getHeight()*0.25))
        self.collidesZone.setXY(self.getX(), self.getY() - int(self.getHeight()*0.25))
        self.collidesZoneBody.setXY(self.getX(), self.getY() - int(self.getHeight()*0.25))

        if self.getState() == self.NORMAL:
            if self.getVelX() > 0:
                self.movementAnimation(self.RIGHT)
            elif self.getVelX() < 0:
                self.movementAnimation(self.LEFT)
            elif self.getVelY() > 0:
                self.movementAnimation(self.DOWN)
            elif self.getVelY() < 0:
                self.movementAnimation(self.UP)
            else:
                if self.getState() == self.NORMAL:
                    self.movementAnimation(self.NORMAL)


        """si la tngo agarrada y termino la animacion"""
        if self.getState() == self.THROW:
            self.setVelXY(0., 0.)
            if self.isEnded():
                anguloTiro = Math.randNumberBetween(0, len(self.angulos) - 1)
                self.giro.setAngle(self.angulos[anguloTiro])

                angRad = self.giro.getAngle() * math.pi / 180
                self.disk.shootDisk(angRad, self.Strength)
                self.stateFrames = 0
                self.setState(self.NORMAL)
                self.disk = None

        """---------------------------TIRO AUTOMATICO---------------------------------"""
        if self.getState() == self.HOLD:
            self.stateFrames += 1
            if self.getState() == self.HOLD:
                if self.stateFrames == self.TIME_HOLD:
                    self.setState(self.THROW)
                    self.stateFrames = 0
        """"---------------------------------------------------------------------------"""

        """---------------------------ESTADO STUN---------------------------------"""
        if self.getState() == self.STUN:
            self.renderStun = True
            self.setVelXY(0., 0.)
            self.stateFrames += 1
            if self.getState() == self.STUN:
                if self.stateFrames == self.TIME_STUN:
                    self.renderStun = False
                    self.setState(self.AFTER_STATE)
                    self.stateFrames = 0

        if self.getState() != self.STUN:
            if self.renderStun:
                self.renderStun = False
        """---------------------------------------------------------------------------"""

        """aca paso a estado hold si choco contra el disco y estoy en estado normal"""
        if self.collidesZone.collides(MatchManager.inst().Disk) and self.getState() == self.NORMAL:
            if MatchManager.inst().Disk.getState() == MatchManager.inst().Disk.NORMAL:
                MatchManager.inst().Disk.setHold(self)
                self.setState(self.HOLD)

    def render(self, aScreen):
        self.collidesZoneBody.render(aScreen)
        self.giro.render(aScreen)
        AnimatedSprite.render(self, aScreen)
        self.collidesZone.render(aScreen)

        if self.renderStun:
            self.PajaritoStun.render(aScreen)

    def setState(self, aState):
        AnimatedSprite.setState(self, aState)

        """tener guardado el estado anterior antes de estar STUN para poder volver"""
        if aState != self.STUN:
            self.AFTER_STATE = aState

        if self.stateFrames != 0:
            self.stateFrames = 0

        if aState == self.THROW:
            self.throwAnimation()
        elif aState == self.POWER:
            self.powerAnimation()
        elif aState == self.STUN:
            self.stunAnimation()
        else:
            self.movementAnimation(self.getState())
            self.changeAnimation(0)



    def movementAnimation(self, mov):
        if self.lastMove != mov:
            self.changeAnimation(mov)
        self.lastMove = mov

    def stateAnimation(self, newState):
        if self.getState() != newState:
            self.mFrames = AssetManager.inst().Characters[self.charID][self.playerNumber][self.getState()][0]
            self.initAnimation(self.mFrames, 0, len(self.mFrames) - 1, 5, True)

    def changeAnimation(self, anim):
        """[ID_Character][Player/Side][State][Animation]"""
        self.mFrames = AssetManager.inst().Characters[self.charID][self.playerNumber][self.getState()][int(anim)]
        self.initAnimation(self.mFrames, 0, len(self.mFrames) - 1, 5, True)

    def throwAnimation(self):
        """[ID_Character][Player/Side][State][Animation]"""
        if self.Move_LEFT:
            self.mFrames = AssetManager.inst().Characters[self.charID][self.playerNumber][self.getState()][1]
        elif self.Move_RIGHT:
            self.mFrames = AssetManager.inst().Characters[self.charID][self.playerNumber][self.getState()][2]
        else:
            self.mFrames = AssetManager.inst().Characters[self.charID][self.playerNumber][self.getState()][0]
        self.initAnimation(self.mFrames, 0, - 1, 3, False)

    def powerAnimation(self):
        """[ID_Character][Player/Side][State][Animation]"""
        if self.Move_LEFT:
            self.mFrames = AssetManager.inst().Characters[self.charID][self.playerNumber][self.getState()][0]
        elif self.Move_RIGHT:
            self.mFrames = AssetManager.inst().Characters[self.charID][self.playerNumber][self.getState()][0]
        else:
            self.mFrames = AssetManager.inst().Characters[self.charID][self.playerNumber][self.getState()][0]
        self.initAnimation(self.mFrames, 0, - 1, 3, True)

    def stunAnimation(self):
        """[ID_Character][Player/Side][State][Animation]"""
        if self.Move_LEFT:
            self.mFrames = AssetManager.inst().Characters[self.charID][self.playerNumber][self.getState()][0]
        elif self.Move_RIGHT:
            self.mFrames = AssetManager.inst().Characters[self.charID][self.playerNumber][self.getState()][0]
        else:
            self.mFrames = AssetManager.inst().Characters[self.charID][self.playerNumber][self.getState()][0]
        self.initAnimation(self.mFrames, 0, - 1, 3, True)

    def setDisk(self, disk):
        self.disk = disk
        self.disk.setState(self.disk.HOLD)
        self.setState(self.HOLD)

    def destroy(self):
        AnimatedSprite.destroy(self)

    def direccion(self):
        if (self.lastMoveDir == self.UP or self.lastMoveDir == self.DOWN) and self.Move_LEFT:
            return self.LEFT
        elif (self.lastMoveDir == self.UP or self.lastMoveDir == self.DOWN) and self.Move_RIGHT:
            return self.RIGHT
        elif (self.lastMoveDir == self.LEFT or self.lastMoveDir == self.RIGHT) and self.Move_UP:
            return self.UP
        elif (self.lastMoveDir == self.LEFT or self.lastMoveDir == self.RIGHT) and self.Move_DOWN:
            return self.DOWN

    def loadGiro(self):
        sc = GameConstants.inst().SCALE
        self.imgAngulo = pygame.image.load("assets/images/giro.png")
        self.imgAngulo = pygame.transform.scale(self.imgAngulo, (int(self.imgAngulo.get_width() * sc), int(self.imgAngulo.get_height() * sc))).convert_alpha()
        self.giro = Reference()
        self.giro.setImage(self.imgAngulo)
        self.giro.show = True
        self.giro.setXY(self.getX(), self.getY())

    def loadCollitionZone(self, czW, czH):
        self.collidesZone = Reference()
        self.collidesZone.setImage(pygame.transform.scale(self.collidesZone.mImg, (czW, czH)))
        self.collidesZone.setXY(self.getX(), self.getY())

    def loadCollitionBody(self, czW, czH):
        self.collidesZoneBody = Reference(3)
        self.collidesZoneBody.setImage(pygame.transform.scale(self.collidesZoneBody.mImg, (czW, czH)))
        self.collidesZoneBody.setXY(self.getX(), self.getY())

    def addEnergy(self):
        if self.Energy < 10:
            self.Energy += 1

    def power(self):
        self.setState(self.POWER)
        self.Energy = 0

