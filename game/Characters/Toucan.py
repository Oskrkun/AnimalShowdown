from api.AnimatedSprite import *
from pygame import *
from api.Keyboard import *
from api.GameConstants import *
from api.AudioManager import *
from game.GameData import *
from game.Characters.Character import *
from api.AssetManager import *
from api.AudioManager import *


class Toucan(Character):

    def __init__(self, player):

        self.charID = 2
        Character.__init__(self, player)

        self.Name = "King Doug"
        self.Speed = 16 * self.sc
        self.Strength = 2

        self.changeAnimation(0)
        self.loadCollitionZone(int(self.getWidth() * 0.40 * self.sc), int(self.getHeight() * 0.30 * self.sc))
        self.loadCollitionBody(int(188 * self.sc), int(200 * self.sc))
        self.PowerChargeFrames = 90

        self.playSounds = False

    def update(self):
        Character.update(self)

        if self.getState() == self.STUN:
            if self.PowerObj != None:
                self.PowerObj = None
        else:
            if self.getState() == self.HOLD:
                if self.PowerObj != None:
                    self.PowerObj = None

            if self.PowerObj != None:
                self.PowerObj.update()

            if self.getState() == self.NORMAL:
                if self.B and self.PowerObj == None and self.Energy == 10:
                    self.powerStart()

            if self.getState() == self.POWER:
                if self.PowerObj != None:
                    self.setVelXY(0., 0.)
                    if self.PowerObj.isEnded():
                        self.PowerObj = None
                        self.setState(self.NORMAL)



    def render(self, aScreen):
        Character.render(self, aScreen)

        if self.PowerObj != None:
            self.PowerObj.render(aScreen)

    def powerStart(self):
        self.Energy = 0
        self.setState(self.POWER)
        self.PowerObj = TwisterPower(self)
        self.PowerObj.setXY(self.collidesZoneBody.getX(),self.collidesZoneBody.getY() - self.collidesZoneBody.getHeight() * 0.10)

    def destroy(self):
        Character.destroy(self)

    def power(self):
        Character.power(self)

