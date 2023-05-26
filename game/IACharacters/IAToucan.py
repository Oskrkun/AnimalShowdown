from api.AnimatedSprite import *
from pygame import *
from api.Keyboard import *
from api.GameConstants import *
from api.AudioManager import *
from game.GameData import *
from game.IACharacters.IACharacter import *
from api.AssetManager import *
from  game.IACharacters.IAPowers.IATwisterPower import *
from game.states.MatchManager import *


class IAToucan(IACharacter):

    def __init__(self, player):

        self.charID = 2
        IACharacter.__init__(self, player)

        self.Name = "King Doug"
        self.Speed = 10 * self.sc
        self.Strength = 2

        self.changeAnimation(0)
        self.loadCollitionZone(int(self.getWidth()*0.20), int(self.getHeight()*0.15))
        self.loadCollitionBody(int(188 * self.sc), int(200 * self.sc))
        self.PowerChargeFrames = 90

        self.IAPowerObj = None

    def update(self):
        from game.states.MatchManager import MatchManager
        IACharacter.update(self)

        if self.getState() != self.STUN or self.getState() != self.THROW:
            self.moveIA()

        if self.getState() == self.HOLD:
            if self.IAPowerObj != None:
                self.IAPowerObj = None

        if self.IAPowerObj is not None:
            self.IAPowerObj.update()

        if Math.randNumberBetween(1, 60) == 2:
            # si apreto la R y estoy en estado normal y no cree el poder y tengo energia
            if self.getState() == self.NORMAL and self.IAPowerObj == None and self.Energy == 10:
                self.Energy = 0
                self.setState(self.POWER)
                self.IAPowerObj = IATwisterPower(self)
                self.IAPowerObj.setXY(self.collidesZoneBody.getX(), self.collidesZoneBody.getY() - self.collidesZoneBody.getHeight() * 0.10)

        if self.getState() == self.POWER:
            if self.IAPowerObj != None:
                self.setVelXY(0., 0.)
                if self.IAPowerObj.isEnded():
                    self.IAPowerObj = None
                    self.setState(self.NORMAL)

    def render(self, aScreen):
        IACharacter.render(self, aScreen)

        if self.IAPowerObj != None:
            self.IAPowerObj.render(aScreen)

    def destroy(self):
        IACharacter.destroy(self)

    def power(self):
        IACharacter.power(self)

    def moveIA(self):
        from game.states.MatchManager import MatchManager

        cordenadaXDestino = MatchManager.inst().Disk.getX() + MatchManager.inst().Disk.getVelX()
        cordenadaYDestino = MatchManager.inst().Disk.getY() + MatchManager.inst().Disk.getVelY()

        """si choco contra un borde y rebota donde va a estar"""
        """parar el loop y que llegue al destino """

        if self.playerNumber == 2:
            if self.collidesZone.distance(MatchManager.inst().Disk) < 300:
                if self.getState() == self.NORMAL:
                    if self.collidesZone.distance(MatchManager.inst().Disk) > self.Speed:
                        if self.collidesZone.getX() < cordenadaXDestino:
                            self.setVelX(self.Speed)
                        elif self.collidesZone.getX() > cordenadaXDestino:
                            self.setVelX(-self.Speed)
                        if self.collidesZone.getY() < cordenadaYDestino:
                            self.setVelY(self.Speed)
                        elif self.collidesZone.getY() > cordenadaYDestino:
                            self.setVelY(-self.Speed)
            else:
                if self.getState() == self.NORMAL:
                    a = Sprite()
                    a.setXY(MatchManager.inst().Stadium.Rlimit - self.screenWidth * 0.20, int((MatchManager.inst().Stadium.Ulimit + MatchManager.inst().Stadium.Dlimit) / 2) + self.collidesZone.getHeight() / 2)

                    if self.distance(a) < self.Speed * 2:
                        self.setXY(a.getX(), a.getY())
                        self.setVelXY(0., 0.)
                    else:
                        if self.getX() >= MatchManager.inst().Stadium.Rlimit - self.screenWidth * 0.20:
                            self.setVelX(-self.Speed)
                        elif self.getX() < MatchManager.inst().Stadium.Rlimit - self.screenWidth * 0.20:
                            self.setVelX(self.Speed)

                        if self.getY() >= int((MatchManager.inst().Stadium.Ulimit + MatchManager.inst().Stadium.Dlimit)/2) + self.collidesZone.getHeight() / 2:
                            self.setVelY(-self.Speed)
                        elif self.getY() < int((MatchManager.inst().Stadium.Ulimit + MatchManager.inst().Stadium.Dlimit)/2) + self.collidesZone.getHeight() / 2:
                            self.setVelY(self.Speed)
        elif self.playerNumber == 1:
            if self.collidesZone.distance(MatchManager.inst().Disk) < 300:
                if self.getState() == self.NORMAL:
                    if self.collidesZone.getX() < cordenadaXDestino:
                        self.setVelX(self.Speed)
                    elif self.collidesZone.getX() > cordenadaXDestino:
                        self.setVelX(-self.Speed)
                    if self.collidesZone.getY() < cordenadaYDestino:
                        self.setVelY(self.Speed)
                    elif self.collidesZone.getY() > cordenadaYDestino:
                        self.setVelY(-self.Speed)
            else:
                if self.getState() == self.NORMAL:
                    a = Sprite()
                    a.setXY(MatchManager.inst().Stadium.Llimit + self.screenWidth * 0.20, int((MatchManager.inst().Stadium.Ulimit + MatchManager.inst().Stadium.Dlimit) / 2) + self.collidesZone.getHeight() / 2)

                    if self.distance(a) < self.Speed * 2:
                        self.setXY(a.getX(), a.getY())
                        self.setVelXY(0., 0.)
                    else:
                        if self.getX() >= MatchManager.inst().Stadium.Llimit + self.screenWidth * 0.20:
                            self.setVelX(-self.Speed)
                        elif self.getX() < MatchManager.inst().Stadium.Llimit + self.screenWidth * 0.20:
                            self.setVelX(self.Speed)

                        if self.getY() >= int((MatchManager.inst().Stadium.Ulimit + MatchManager.inst().Stadium.Dlimit) / 2) + self.collidesZone.getHeight() / 2:
                            self.setVelY(-self.Speed)
                        elif self.getY() < int((MatchManager.inst().Stadium.Ulimit + MatchManager.inst().Stadium.Dlimit) / 2) + self.collidesZone.getHeight() / 2:
                            self.setVelY(self.Speed)
