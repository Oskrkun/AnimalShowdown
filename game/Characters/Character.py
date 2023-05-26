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
from game.Characters.Particles.Particles import *
from api.ParticleManager import *
import math


class Character(AnimatedSprite):

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

    lastState = 0

    """Tiempos que duran los estados."""
    TIME_HOLD = 40
    TIME_STUN = 60
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
        self.sc = GameConstants.inst().SCALE

        """[ID_Character][Player/Side][State][Animation]"""
        self.mFrames = AssetManager.inst().Characters[self.charID][self.playerNumber][self.NORMAL][self.NORMAL]

        self.mWidth = self.mFrames[0].get_width()
        self.mHeight = self.mFrames[0].get_height()

        self.mState = self.NORMAL


        """-------objeto del stado stun-------"""
        self.PajaritoStun = AssetManager.inst().loadAssets("assets/images/Characters/stun/", "stun_", self.sc)
        self.PajaritoStun = AssetAnimated(self.PajaritoStun, True, 10)
        self.PajaritoStun.setXY(self.getX(), self.getY())
        self.renderStun = False
        """-----------------------------------"""

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

        self.lastState = 0

        self.stateFrames = 0

        self.disk = None
        self.catch = False

        self.newVector = Vector()
        self.loadGiro()

        self.PowerObj = None

        """----------VARIABLES PARA DASH----------"""
        self.xDestDash = None
        self.dashLenght = 180 * self.sc

        self.TIME_KEYBOARD_DASH = 10
        self.mFirstTimeDashPressed = False
        self.mTimeToMakeDash = 0
        self.mCanDash = False

        self.dirDash = 0
        self.preDirDash = 0

        self.destino = 0
        self.retardTimeDash = 0.50
        self.secondPressedDash = False
        self.mTotalTime = 0

        self.beforeMoveDash = 0

        self.velDashMove = 2 * self.sc

        self.sands = False
        """--------------------------------------"""

    def update(self):

        AnimatedSprite.update(self)

        #print(Joystick.inst().UpPressed(1))

        self.PajaritoStun.setXY(self.getX(), self.getY() - self.getHeight() / 2)
        self.PajaritoStun.update()

        self.giro.setXY(self.getX(), self.getY() - int(self.getHeight()*0.25))
        self.collidesZone.setXY(self.getX(), self.getY() - int(self.getHeight()*0.23))
        self.collidesZoneBody.setXY(self.getX(), self.getY() - int(self.getHeight()*0.25))

        """si la tngo agarrada y termino la animacion"""
        if self.getState() == self.THROW:
            self.setVelXY(0., 0.)
            if self.isEnded():
                angRad = self.giro.getAngle() * math.pi / 180
                self.disk.shootDisk(angRad, self.Strength)
                self.stateFrames = 0
                self.setState(self.NORMAL)
                self.disk = None

        """---------------------------TIRO AUTOMATICO----------------------------------"""
        if self.getState() == self.HOLD:
            self.stateFrames += 1
            if self.getState() == self.HOLD:
                if self.stateFrames == self.TIME_HOLD:
                    self.setState(self.THROW)
                    self.stateFrames = 0
        """"---------------------------------------------------------------------------"""

        """---------------------------ESTADO STUN--------------------------------------"""
        if self.getState() != self.STUN:
            if self.renderStun:
                self.renderStun = False
        """----------------------------------------------------------------------------"""

        if self.getState() != self.STUN and self.getState() != self.THROW and self.getState() != self.DASH:
            self.moveKey()
        elif self.getState() == self.STUN:
            self.renderStun = True
            self.setVelXY(0., 0.)
            self.stateFrames += 1
            if self.getState() == self.STUN:
                if self.stateFrames == self.TIME_STUN:
                    self.renderStun = False
                    self.setState(self.NORMAL)
                    self.stateFrames = 0

            if (self.lastState == self.HOLD or self.lastState == self.THROW) and self.disk != None:
                if self.playerNumber == 1:
                    angulos = [0, 15, 30, 45, 60, 345, 330, 315, 300]
                    rand = Math.randNumberBetween(0, len(angulos) - 1)
                    self.giro.setAngle(angulos[rand])
                elif self.playerNumber == 2:
                    angulos = [180, 165, 150, 135, 120, 195, 210, 225, 240]
                    rand = Math.randNumberBetween(0, len(angulos) - 1)
                    self.giro.setAngle(angulos[rand])
                angRad = self.giro.getAngle() * math.pi / 180
                self.disk.shootDisk(angRad, self.Strength)
                self.stateFrames = 0
                self.disk = None

        """-------------------------------DASH-----------------------------------------"""
        self.dashing()

        if self.mFirstTimeDashPressed:
            self.mTotalTime + 1
            if self.mTotalTime == self.retardTimeDash:
                self.mTotalTime = 0
                self.mFirstTimeDashPressed = False
        """"---------------------------------------------------------------------------"""

    def render(self, aScreen):
        self.collidesZoneBody.render(aScreen)
        self.giro.render(aScreen)
        AnimatedSprite.render(self, aScreen)
        self.collidesZone.render(aScreen)

        if self.renderStun:
            self.PajaritoStun.render(aScreen)

    def moveKey(self):
        self.defineKeys(self.playerNumber)

        self.newVector = Vector()

        if self.getState() != self.THROW and self.getState() != self.POWER and self.getState() != self.STUN:
            if not self.PMove_UP and not self.PMove_DOWN and not self.PMove_LEFT and not self.PMove_RIGHT:
                self.setVelXY(0., 0.)
                self.shootAngle(self.NORMAL)
                self.movementAnimation(self.NORMAL)
            else:
                du = 1. * 0.59
                if self.PMove_UP and self.PMove_LEFT:
                    self.newVector.add(Vector(-du, -du))
                    self.shootAngle(self.direccion())
                    self.movementAnimation(self.LEFT)
                elif self.PMove_UP and self.PMove_RIGHT:
                    self.newVector.add(Vector(du, -du))
                    self.shootAngle(self.direccion())
                    self.movementAnimation(self.RIGHT)
                elif self.PMove_DOWN and self.PMove_LEFT:
                    self.newVector.add(Vector(-du, du))
                    self.shootAngle(self.direccion())
                    self.movementAnimation(self.LEFT)
                elif self.PMove_DOWN and self.PMove_RIGHT:
                    self.newVector.add(Vector(du, du))
                    self.shootAngle(self.direccion())
                    self.movementAnimation(self.RIGHT)
                elif self.PMove_UP:
                    self.beforeMoveDash = 4
                    self.newVector.add(Vector(0., -1.))
                    self.lastMoveDir = self.UP
                    if self.playerNumber == 1:
                        self.giro.setAngle(60)
                    elif self.playerNumber == 2:
                        self.giro.setAngle(120)
                    self.shootAngle(self.UP)
                    self.movementAnimation(self.UP)
                elif self.PMove_DOWN:
                    self.beforeMoveDash = 3
                    self.newVector.add(Vector(0., 1.))
                    self.lastMoveDir = self.DOWN
                    if self.playerNumber == 1:
                        self.giro.setAngle(300)
                    elif self.playerNumber == 2:
                        self.giro.setAngle(240)
                    self.shootAngle(self.DOWN)
                    self.movementAnimation(self.DOWN)
                elif self.PMove_LEFT:
                    self.beforeMoveDash = 2
                    self.newVector.add(Vector(-1., 0.))
                    self.lastMoveDir = self.LEFT
                    self.giro.setAngle(180)
                    self.shootAngle(self.LEFT)
                    self.movementAnimation(self.LEFT)
                elif self.PMove_RIGHT:
                    self.beforeMoveDash = 1
                    self.newVector.add(Vector(1., 0.))
                    self.lastMoveDir = self.RIGHT
                    self.giro.setAngle(359)
                    self.shootAngle(self.RIGHT)
                    self.movementAnimation(self.RIGHT)

                self.newVector.mul(self.Speed)
                self.setVelXY(self.newVector.x, self.newVector.y)

        self.stateVerification()

    def setState(self, aState):
        AnimatedSprite.setState(self, aState)

        self.mFirstTimeDashPressed = False
        self.mTotalTime = 0

        """tener guardado el estado anterior antes de estar STUN o DASH para poder volver"""
        if aState != self.STUN and aState != self.DASH:
            self.lastState = aState

        if self.stateFrames != 0:
            self.stateFrames = 0

        if aState == self.THROW:
            if self.playerNumber == 1:
                if self.PMove_LEFT and not self.PMove_RIGHT:
                    self.turnAngle()
                    self.PMove_LEFT = False
                    self.PMove_RIGHT = True
            elif self.playerNumber == 2:
                if self.PMove_RIGHT and not self.PMove_LEFT:
                    self.turnAngle()
                    self.PMove_LEFT = True
                    self.PMove_RIGHT = False
            self.throwAnimation()
        elif aState == self.POWER:
            self.powerAnimation()
        elif aState == self.STUN:
            self.stunAnimation()
        elif aState == self.DASH:
            self.setVelXY(0, 0)
            # aca comprobar los bordes y achicar el destino si pego contra un borde
            # usar getBounds de GameObject
            if self.dirDash == 1:
                #derecha
                # print("entre dash derecha")
                self.destino = self.getX() + self.dashLenght
                if self.destino >= self.getBounds()[1]:
                    self.destino = self.getBounds()[1] - 100 * self.sc
            if self.dirDash == 2:
                #izquierda
                # print("entre dash izquierda")
                self.destino = self.getX() - self.dashLenght
                if self.destino <= self.getBounds()[0]:
                    self.destino = self.getBounds()[0] + 100 * self.sc
            if self.dirDash == 3:
                #arriba
                # print("entre dash arriba")
                self.destino = self.getY() - self.dashLenght
                if self.destino <= self.getBounds()[2]:
                    self.destino = self.getBounds()[2] + 100 * self.sc
            if self.dirDash == 4:
                #abajo
                # print("entre dash abajo")
                self.destino = self.getY() + self.dashLenght
                if self.destino >= self.getBounds()[3]:
                    self.destino = self.getBounds()[3] - 100 * self.sc
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
        if self.PMove_LEFT:
            self.mFrames = AssetManager.inst().Characters[self.charID][self.playerNumber][self.getState()][1]
        elif self.PMove_RIGHT:
            self.mFrames = AssetManager.inst().Characters[self.charID][self.playerNumber][self.getState()][2]
        else:
            self.mFrames = AssetManager.inst().Characters[self.charID][self.playerNumber][self.getState()][0]
        self.initAnimation(self.mFrames, 0, - 1, 3, False)

    def powerAnimation(self):
        """[ID_Character][Player/Side][State][Animation]"""
        if self.PMove_LEFT:
            self.mFrames = AssetManager.inst().Characters[self.charID][self.playerNumber][self.getState()][0]
        elif self.PMove_RIGHT:
            self.mFrames = AssetManager.inst().Characters[self.charID][self.playerNumber][self.getState()][0]
        else:
            self.mFrames = AssetManager.inst().Characters[self.charID][self.playerNumber][self.getState()][0]
        self.initAnimation(self.mFrames, 0, - 1, 3, True)

    def stunAnimation(self):
        """[ID_Character][Player/Side][State][Animation]"""
        if self.PMove_LEFT:
            self.mFrames = AssetManager.inst().Characters[self.charID][self.playerNumber][self.getState()][0]
        elif self.PMove_RIGHT:
            self.mFrames = AssetManager.inst().Characters[self.charID][self.playerNumber][self.getState()][0]
        else:
            self.mFrames = AssetManager.inst().Characters[self.charID][self.playerNumber][self.getState()][0]
        self.initAnimation(self.mFrames, 0, - 1, 3, True)

    def defineKeys(self, playerNumber):
        if playerNumber == 1:
            self.PMove_UP = Keyboard.inst().WPressed()
            self.PMove_DOWN = Keyboard.inst().SPressed()
            self.PMove_LEFT = Keyboard.inst().APressed()
            self.PMove_RIGHT = Keyboard.inst().DPressed()

            self.FPMove_UP = Keyboard.inst().previousW()
            self.FPMove_DOWN = Keyboard.inst().previousS()
            self.FPMove_LEFT = Keyboard.inst().previousA()
            self.FPMove_RIGHT = Keyboard.inst().previousD()

            self.A = Keyboard.inst().CPressed()
            self.B = Keyboard.inst().VPressed()
        elif playerNumber == 2:
            self.PMove_UP = Keyboard.inst().upPressed()
            self.PMove_DOWN = Keyboard.inst().downPressed()
            self.PMove_LEFT = Keyboard.inst().leftPressed()
            self.PMove_RIGHT = Keyboard.inst().rightPressed()

            self.FPMove_UP = Keyboard.inst().previousUp()
            self.FPMove_DOWN = Keyboard.inst().previousDown()
            self.FPMove_LEFT = Keyboard.inst().previousLeft()
            self.FPMove_RIGHT = Keyboard.inst().previousRight()

            self.A = Keyboard.inst().KPressed()
            self.B = Keyboard.inst().LPressed()

    def setDisk(self, disk):
        self.disk = disk
        self.disk.setState(self.disk.HOLD)
        self.setState(self.HOLD)

    def destroy(self):
        AnimatedSprite.destroy(self)

    def direccion(self):
        if (self.lastMoveDir == self.UP or self.lastMoveDir == self.DOWN) and self.PMove_LEFT:
            return self.LEFT
        elif (self.lastMoveDir == self.UP or self.lastMoveDir == self.DOWN) and self.PMove_RIGHT:
            return self.RIGHT
        elif (self.lastMoveDir == self.LEFT or self.lastMoveDir == self.RIGHT) and self.PMove_UP:
            return self.UP
        elif (self.lastMoveDir == self.LEFT or self.lastMoveDir == self.RIGHT) and self.PMove_DOWN:
            return self.DOWN

    def shootAngle(self, move):
        grados = 90 / self.TIME_HOLD

        if move == 0:
            if self.playerNumber == 1:
                self.giro.setAngle(360)
            elif self.playerNumber == 2:
                self.giro.setAngle(180)

        if self.lastMoveDir == self.DOWN:
            if move == self.LEFT:
                if self.playerNumber == 2 and self.giro.getAngle() > 180:
                    self.giro.turnAngle(-grados)
            elif move == self.RIGHT:
                if self.playerNumber == 1 and self.giro.getAngle() < 357:
                    self.giro.turnAngle(grados)
        elif self.lastMoveDir == self.UP:
            if move == self.LEFT:
                if self.playerNumber == 2 and self.giro.getAngle() < 180:
                    self.giro.turnAngle(grados)
            elif move == self.RIGHT:
                if self.playerNumber == 1 and self.giro.getAngle() > 3:
                    self.giro.turnAngle(-grados)
        elif self.lastMoveDir == self.LEFT:
            if move == self.UP:
                if self.giro.getAngle() > 120:
                    self.giro.turnAngle(-grados)
            elif move == self.DOWN:
                if self.giro.getAngle() < 240:
                    self.giro.turnAngle(grados)
        elif self.lastMoveDir == self.RIGHT:
            if move == self.UP:
                if self.giro.getAngle() < 60 or self.giro.getAngle() == 359:
                    self.giro.turnAngle(grados)
            elif move == self.DOWN:
                if self.giro.getAngle() > 300:
                    self.giro.turnAngle(-grados)

    def turnAngle(self):
        if self.playerNumber == 1:
            if self.giro.getAngle() > 90 and self.giro.getAngle() <= 180:
                self.giro.setAngle(90 - (self.giro.getAngle() - 90))
            elif self.giro.getAngle() > 180 and self.giro.getAngle() <= 270:
                self.giro.setAngle(270 + (270 - self.giro.getAngle()))
        elif self.playerNumber == 2:
            if (self.giro.getAngle() >= 0 or self.giro.getAngle() == 360) and self.giro.getAngle() < 90:
                self.giro.setAngle(90 + (90 - self.giro.getAngle()))
            elif self.giro.getAngle() > 270 and self.giro.getAngle() <= 360:
                self.giro.setAngle(270 - (self.giro.getAngle() - 270))

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

    def stateVerification(self):
        from game.states.MatchManager import MatchManager

        """si tngo el disco y estoy en hold y aprete el boton de disparar"""
        if self.getState() == self.HOLD and self.A and self.disk is not None:
            self.setState(self.THROW)

        """aca paso a estado hold si choco contra el disco y estoy en estado normal"""
        if self.collidesZone.collides(MatchManager.inst().Disk) and self.getState() == self.NORMAL:
            if MatchManager.inst().Disk.getState() == MatchManager.inst().Disk.NORMAL:
                MatchManager.inst().Disk.setHold(self)
                self.setState(self.HOLD)

    def dashing(self):
        self.defineKeys(self.playerNumber)

        if self.getState() == self.DASH:
            if self.dirDash == 1:
                self.setVelX((self.destino - self.getX()) / self.velDashMove)
                if self.getVelX() < 5:
                    self.setState(self.lastState)
            if self.dirDash == 2:
                self.setVelX(((self.destino - self.getX()) / self.velDashMove))
                if self.getVelX() > -5:
                    self.setState(self.lastState)
            if self.dirDash == 3:
                self.setVelY(((self.destino - self.getY()) / self.velDashMove))
                if self.getVelY() > -5:
                    self.setState(self.lastState)
            if self.dirDash == 4:
                self.setVelY((self.destino - self.getY()) / self.velDashMove)
                if self.getVelY() < 5:
                    self.setState(self.lastState)
            self.particlesDash(self.dirDash, self.charID)
            return
        else:
            if self.FPMove_RIGHT:
                if self.mFirstTimeDashPressed:
                    self.mCanDash = True
                else:
                    self.mFirstTimeDashPressed = True
                    self.mCanDash = False
            if self.FPMove_LEFT:
                if self.mFirstTimeDashPressed:
                    self.mCanDash = True
                else:
                    self.mFirstTimeDashPressed = True
                    self.mCanDash = False
            if self.FPMove_UP:
                if self.mFirstTimeDashPressed:
                    self.mCanDash = True
                else:
                    self.mFirstTimeDashPressed = True
                    self.mCanDash = False
            if self.FPMove_DOWN:
                if self.mFirstTimeDashPressed:
                    self.mCanDash = True
                else:
                    self.mFirstTimeDashPressed = True
                    self.mCanDash = False

            if self.mTimeToMakeDash >= self.TIME_KEYBOARD_DASH:
                self.mFirstTimeDashPressed = False
                self.beforeMoveDash = 0
                self.mTimeToMakeDash = 0
                self.mCanDash = False

            if self.mFirstTimeDashPressed:
                self.mTimeToMakeDash += 1

            if (self.mCanDash and self.FPMove_RIGHT and self.beforeMoveDash == 1):
                self.dirDash = 1
                self.setState(self.DASH)
                self.mCanDash = False
                return
            if (self.mCanDash and self.FPMove_LEFT and self.beforeMoveDash == 2):
                self.dirDash = 2
                self.setState(self.DASH)
                self.mCanDash = False
                return
            if (self.mCanDash and self.FPMove_UP and self.beforeMoveDash == 4):
                self.dirDash = 3
                self.setState(self.DASH)
                self.mCanDash = False
                return
            if (self.mCanDash and self.FPMove_DOWN and self.beforeMoveDash == 3):
                self.dirDash = 4
                self.setState(self.DASH)
                self.mCanDash = False
                return

    def particlesDash(self, aDirDash, aType):
        p = None
        dir = False

        # si voy arriba y soy player 2 corrigo direcciond e particulas
        if aDirDash == 3 and self.playerNumber == 2:
            dir = True
        elif aDirDash == 2:
            dir = True

        if aType == 1:
            p = Particles(AssetManager.inst().loadAssets("assets/images/Characters/monkey/DASH/particles/", "monkey_30_", self.sc, dir), False, 2)
        elif aType == 2:
            p = Particles(AssetManager.inst().loadAssets("assets/images/Characters/toucan/DASH/particles/", "toucan_30_", self.sc, dir), False, 2)

        p.setXY(self.getX(), self.getY())
        ParticleManager.inst().addParticle(p)



