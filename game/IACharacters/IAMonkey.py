from api.AnimatedSprite import *
from pygame import *
from api.Keyboard import *
from api.GameConstants import *
from api.AudioManager import *
from game.GameData import *
from game.IACharacters.IACharacter import *
from api.AssetManager import *
from game.IACharacters.IAPowers.IAParticleFireballPower import *
from game.IACharacters.IAPowers.IAFireballPower import *
from api.GameConstants import *
from game.states.MatchManager import *


class IAMonkey(IACharacter):

    def __init__(self, playerNumber):

        self.charID = 1
        IACharacter.__init__(self, playerNumber)

        self.Name = "Elvis"
        self.Speed = 5 * self.sc
        self.Strength = 1.75

        self.changeAnimation(0)
        self.loadCollitionZone(int(self.getWidth()*0.25 * self.sc), int(self.getHeight()*0.25 * self.sc))
        self.loadCollitionBody(int(144 * self.sc), int(130 * self.sc))
        self.PowerChargeFrames = 60

        self.IAParticleFireballPower = None
        self.IAFireballPower = None

    def update(self):
        from game.states.MatchManager import MatchManager
        IACharacter.update(self)

        if self.getState() != self.STUN or self.getState() != self.THROW:
            self.moveIA()

        if self.getState() == self.HOLD:
            if self.IAParticleFireballPower != None:
                self.IAParticleFireballPower = None
            if self.IAFireballPower != None:
                self.IAFireballPower = None

        if self.IAParticleFireballPower != None:
            self.IAParticleFireballPower.update()

        if self.IAFireballPower != None:
            self.IAFireballPower.update()

        if Math.randNumberBetween(1, 2) == 2:
            #si apreto la B y estoy en estado normal y no cree el poder y tengo energia
            bandera = False
            if self.getState() == self.NORMAL and self.PowerObj == None and self.Energy == 10:
                if self.playerNumber == 2:
                    if MatchManager.inst().Player1.collidesZoneBody.getY() - self.getY() < MatchManager.inst().Player1.collidesZoneBody.getHeight():
                        bandera = True
                if self.playerNumber == 1:
                    if MatchManager.inst().Player2.collidesZoneBody.getY() - self.getY() < MatchManager.inst().Player2.collidesZoneBody.getHeight():
                        bandera = True

                    if bandera:
                        self.Energy = 0
                        self.setState(self.POWER)
                        self.IAParticleFireballPower = IAParticleFireballPower(self)

                        if self.playerNumber == 1:
                            self.IAParticleFireballPower.setXY(self.getX() + (150 * self.sc), self.collidesZoneBody.getY())
                        elif self.playerNumber == 2:
                            self.IAParticleFireballPower.setXY(self.getX() - (150 * self.sc), self.collidesZoneBody.getY())

        if self.getState() == self.POWER:
            self.setVelXY(0,0)
            if self.IAParticleFireballPower != None:
                if self.IAParticleFireballPower.getCurrentFrame() == 14:
                    self.IAFireballPower = IAFireballPower(self)
                if self.IAParticleFireballPower.isEnded():
                    self.IAParticleFireballPower = None
                    self.setState(self.NORMAL)

        if self.IAFireballPower != None:
            if self.playerNumber == 1:
                if MatchManager.inst().Player2.collidesZoneBody.collides(self.IAFireballPower.collidesZone):
                    if MatchManager.inst().Player2.getState() != MatchManager.inst().Player2.STUN:
                        MatchManager.inst().Player2.setState(MatchManager.inst().Player2.STUN)
                        self.IAFireballPower = None
            if self.playerNumber == 2:
                if MatchManager.inst().Player1.collidesZoneBody.collides(self.IAFireballPower.collidesZone):
                    if MatchManager.inst().Player1.getState() != MatchManager.inst().Player1.STUN:
                        MatchManager.inst().Player1.setState(MatchManager.inst().Player1.STUN)
                        self.IAFireballPower = None

        if self.getState() == self.STUN:
            self.setVelXY(0, 0)

    def render(self, aScreen):
        IACharacter.render(self, aScreen)

        if self.IAParticleFireballPower != None:
            self.IAParticleFireballPower.render(aScreen)

        if self.IAFireballPower != None:
            self.IAFireballPower.render(aScreen)

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

