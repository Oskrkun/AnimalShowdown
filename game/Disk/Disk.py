# -*- coding: utf-8 -*-
from api.AnimatedSprite import *
from pygame import *
from api.Keyboard import *
from api.GameConstants import *
from api.AudioManager import *
from game.GameData import *
from api.AssetManager import *
from api.Math import *
from game.states.MatchManager import *
from game.Reference import *

class Disk(AnimatedSprite):
    # Máquina de estados.
    NORMAL = 0
    HOLD = 1

    #aRuta1 es la ruta de los frames de la animacion normal aRuta2 son cuando le hacen click se le pasa un ancho y alto a los botones para escalarlos y si es animacion ciclica o no
    def __init__(self):

        Sprite.__init__(self)

        self.sc = GameConstants.inst().SCALE

        self.ciclico = True
        self.delay = 2

        self.mFramesNormal = AssetManager.inst().Disks[0]

        self.mWidth = self.mFramesNormal[0].get_width()
        self.mHeight = self.mFramesNormal[0].get_height()

        self.speed = int(15 * self.sc)

        self.v = Vector()
        self.setMaxSpeed(int(60 * self.sc))

        self.accelBounce = 1.05



        #------------------------------------------------------------------
        #--------------Relacionado al agarre del disco---------------------
        self.char = None
        self.contador = 0
        self.segundos = 0
        #------------------------------------------------------------------

        # Estado inicial.
        self.mState = Disk.NORMAL
        self.setState(Disk.NORMAL)

        self.loadCollitionZone(self.getWidth(), self.getHeight())

        self.bandera = False

    def update(self):
        from game.states.MatchManager import MatchManager

        self.collidesZone.setXY(self.getX(), self.getY())

        if self.getVelX() > 15 or self.getVelY() > 15 or self.getVelX() < -15 or self.getVelY() < -15:
            self.particles()


        if not self.fieldLimitCollisions(MatchManager.inst().Stadium):
            if self.getState() == self.HOLD and self.char != None:
                self.setVelXY(0, 0)
                self.setXY(self.char.collidesZone.getX(), self.char.collidesZone.getY())

            if not MatchManager.inst().Player1.collidesZone.collides(self) and not MatchManager.inst().Player2.collidesZone.collides(self) and self.getState() == self.HOLD:
                self.setState(self.NORMAL)

        AnimatedSprite.update(self)

    def render(self, aScreen):

        self.collidesZone.render(aScreen)
        if self.char is None:
            AnimatedSprite.render(self, aScreen)

    def setState(self, aState):
        AnimatedSprite.setState(self, aState)
        self.initAnimation(self.mFramesNormal, 0, len(self.mFramesNormal)-1,  self.delay, self.ciclico)

    def setHold(self, char):
        self.char = char
        self.char.setDisk(self)
        self.setState(self.HOLD)

    def shootDisk(self, angRad, str=0):
        self.char = None
        vx = (self.speed * str) * math.cos(angRad)
        vy = (self.speed * str) * math.sin(angRad)
        vy *= -1
        self.setVelXY(vx, vy)


    def fieldLimitCollisions(self, stadium):

        bandera = False

        if self.willCollide(stadium.UpperLimit):
            self.setY(int(stadium.UpperLimit.getY() + (stadium.UpperLimit.getHeight() / 2) + 20 * self.sc))
            self.setVelY(self.getVelY() * -self.accelBounce)
            bandera = True

        if self.willCollide(stadium.LowerLimit):
            self.setY(int(stadium.LowerLimit.getY() - (stadium.LowerLimit.getHeight() / 2) - 20 * self.sc))
            self.setVelY(self.getVelY() * -self.accelBounce)
            bandera = True

        if self.willCollide(stadium.RightLimit1) or self.willCollide(stadium.RightLimit2):
            self.setVelX(self.getVelX() * -self.accelBounce)
            bandera = True
        elif self.willCollide(stadium.postR1):
            self.setY(int(stadium.postR1.getY() + (stadium.postR1.getHeight() / 2) + 1))
            self.setVelY(self.getVelY() * -self.accelBounce)
            bandera = True
        elif self.willCollide(stadium.postR2):
            self.setY(int(stadium.postR2.getY() + (stadium.postR2.getHeight() / 2) + 1))
            self.setVelY(self.getVelY() * -self.accelBounce)
            bandera = True

        if self.willCollide(stadium.LeftLimit1) or self.willCollide(stadium.LeftLimit2):
            self.setVelX(self.getVelX() * -self.accelBounce)
            bandera = True
        elif self.willCollide(stadium.postL1):
            self.setY(int(stadium.postL1.getY() + (stadium.postL1.getHeight() / 2) + 1))
            self.setVelY(self.getVelY() * -self.accelBounce)
            bandera = True
        elif self.willCollide(stadium.postL2):
            self.setY(int(stadium.postL2.getY() + (stadium.postL2.getHeight() / 2) + 1))
            self.setVelY(self.getVelY() * -self.accelBounce)
            bandera = True

        return bandera

    def loadCollitionZone(self, czW, czH):
        self.collidesZone = Reference(2)
        self.collidesZone.setImage(pygame.transform.scale(self.collidesZone.mImg, (czW, czH)))
        self.collidesZone.setXY(self.getX(), self.getY())

    def invDir(self):
        self.setVelX(self.getVelX() * -2)

    def particles(self):
        p = Particles(AssetManager.inst().loadAssets("assets/images/Disk/particles/", "disk_00_", self.sc, False), False, 2)
        p.setXY(self.getX(), self.getY())
        ParticleManager.inst().addParticle(p)

    def destroy(self):
        AnimatedSprite.destroy(self)

        i = len(self.mFramesNormal)
        while i > 0:
            self.mFrames[i - 1] = None
            self.mFrames.pop(i - 1)
            i = i - 1
