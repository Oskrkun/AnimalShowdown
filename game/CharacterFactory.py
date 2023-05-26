# -*- coding: utf-8 -*-

import pygame
from api.Manager import *
from game.Characters.Monkey import *
from game.Characters.Toucan import *
from api.Game import *
from game.IACharacters.IAMonkey import *
from game.IACharacters.IAToucan import *


class CharacterFactory(object):

    mInstance = None
    mInitialized = False

    TYPE_MONKEY = 1
    TYPE_TOUCAN = 2

    screenWidth = GameConstants.inst().SCREEN_WIDTH
    screenHeight = GameConstants.inst().SCREEN_HEIGHT

    def __new__(self, *args, **kargs):
        if (CharacterFactory.mInstance is None):
            CharacterFactory.mInstance = object.__new__(self, *args, **kargs)
            self.init(CharacterFactory.mInstance)
        return self.mInstance

    @classmethod
    def inst(cls):
        if (not cls.mInstance):
            return cls()
        return cls.mInstance

    def init(self):
        if (CharacterFactory.mInitialized):
            return
            CharacterFactory.mInitialized = True

    def createCharacter(self, charID, playerNumber):
        char = None

        if charID > 0:
            if charID == self.TYPE_MONKEY:
                char = Monkey(playerNumber)
            elif charID == self.TYPE_TOUCAN:
                char = Toucan(playerNumber)
        else:
            if charID == self.TYPE_MONKEY * -1:
                char = IAMonkey(playerNumber)
            elif charID == self.TYPE_TOUCAN * -1:
                char = IAToucan(playerNumber)

        return char
