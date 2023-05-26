from api.AnimatedSprite import *
from pygame import *
from api.Keyboard import *
from api.GameConstants import *
from api.AudioManager import *
from game.GameData import *
from game.Characters.Character import *
from api.AssetManager import *
from game.Characters.Powers.ParticleFireballPower import *
from game.Characters.Powers.FireballPower import *
from api.GameConstants import *
from game.states.MatchManager import *
from game.Characters.Particles.Particles import *

class Monkey(Character):

    def __init__(self, playerNumber):

        self.charID = 1
        Character.__init__(self, playerNumber)

        self.Name = "Elvis"
        self.Speed = 10 * GameConstants.inst().SCALE
        self.Strength = 2.5

        self.changeAnimation(0)
        self.loadCollitionZone(int(self.getWidth()*0.25 * self.sc), int(self.getHeight()*0.25 * self.sc))
        self.loadCollitionBody(int(144 * self.sc), int(130 * self.sc))
        self.PowerChargeFrames = 60



        self.ParticleFireballPower = None
        self.FireballPower = None

    def update(self):
        from game.states.MatchManager import MatchManager
        Character.update(self)

        if self.getState() == self.HOLD:
            if self.PowerObj != None:
                self.PowerObj = None

        if self.getState() == self.NORMAL:
            if self.B and self.PowerObj == None and self.Energy == 10:
                self.powerStart()

        if self.ParticleFireballPower != None:
            self.ParticleFireballPower.update()

        if self.FireballPower != None:
            self.FireballPower.update()
            if self.FireballPower.collidesZone.collides(MatchManager.inst().Stadium.LeftLimit2) or self.FireballPower.collidesZone.collides(MatchManager.inst().Stadium.LeftLimit1):
                self.FireballPower = None
            elif self.FireballPower.collidesZone.collides(MatchManager.inst().Stadium.RightLimit2) or self.FireballPower.collidesZone.collides(MatchManager.inst().Stadium.RightLimit1):
                self.FireballPower = None


        if self.getState() == self.POWER:
            self.setVelXY(0,0)
            if self.ParticleFireballPower != None:
                if self.ParticleFireballPower.getCurrentFrame() == 14:
                    self.FireballPower = FireballPower(self)
                if self.ParticleFireballPower.isEnded():
                    self.ParticleFireballPower = None
                    self.setState(self.NORMAL)

        if self.FireballPower != None:
            if self.playerNumber == 1:
                if MatchManager.inst().Player2.collidesZoneBody.collides(self.FireballPower.collidesZone):
                    if MatchManager.inst().Player2.getState() != MatchManager.inst().Player2.STUN:
                        MatchManager.inst().Player2.setState(MatchManager.inst().Player2.STUN)
                        self.FireballPower = None
            if self.playerNumber == 2:
                if MatchManager.inst().Player1.collidesZoneBody.collides(self.FireballPower.collidesZone):
                    if MatchManager.inst().Player1.getState() != MatchManager.inst().Player1.STUN:
                        MatchManager.inst().Player1.setState(MatchManager.inst().Player1.STUN)
                        self.FireballPower = None


    def render(self, aScreen):
        Character.render(self, aScreen)

        if self.ParticleFireballPower != None:
            self.ParticleFireballPower.render(aScreen)

        if self.FireballPower != None:
            self.FireballPower.render(aScreen)

    def destroy(self):
        Character.destroy(self)

    def powerStart(self):
        self.Energy = 0
        self.setState(self.POWER)
        self.ParticleFireballPower = ParticleFireballPower(self)

        if self.playerNumber == 1:
            self.ParticleFireballPower.setXY(self.getX() + (150 * self.sc), self.collidesZoneBody.getY())
        elif self.playerNumber == 2:
            self.ParticleFireballPower.setXY(self.getX() - (150 * self.sc), self.collidesZoneBody.getY())

    def power(self):
        Character.power(self)

