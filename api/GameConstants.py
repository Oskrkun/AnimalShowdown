# -*- coding: utf-8 -*-
from api.Keyboard import *

class GameConstants(object):

    mInstance = None
    mInitialized = False

    SCALE = 1

    ResolutionsWIDTH = []
    ResolutionsHEIGHT = []
    ResSelected = 0

    SCREEN_WIDTH = int(1920 * SCALE)
    SCREEN_HEIGHT = int(1080 * SCALE)

    CANTIDADPERSONAJES = 2
    CANTIDADESTADIOS = 4

    Ulimit = int(SCREEN_HEIGHT * 0.332)
    Dlimit = int(SCREEN_HEIGHT * 0.99)
    Llimit = int(SCREEN_WIDTH * 0.06)
    Rlimit = int(SCREEN_WIDTH * 0.94)

    SHOW_REF = False

    def __new__(self, *args, **kargs):
        if (GameConstants.mInstance is None):
            GameConstants.mInstance = object.__new__(self, *args, **kargs)
            self.init(GameConstants.mInstance)
        else:
            print ("Cuidado: GameConstants(): No se debería instanciar más de una vez esta clase. Usar GameConstants.inst().")
        return self.mInstance

    @classmethod
    def inst(cls):
        if (not cls.mInstance):
            return cls()
        return cls.mInstance
    
    def init(self):
        if (GameConstants.mInitialized):
            return

        self.ResolutionsWIDTH.append(1920)
        self.ResolutionsHEIGHT.append(1080)
        self.ResolutionsWIDTH.append(1366)
        self.ResolutionsHEIGHT.append(768)

        GameConstants.mInitialized = True

    def destroy(self):
        GameConstants.mInstance = None

    def changeResolution(self, resSelect):
        self.ResSelected = resSelect
        self.SCALE = self.ResolutionsWIDTH[self.ResSelected] / 1920
        self.SCREEN_WIDTH = int(self.ResolutionsWIDTH[self.ResSelected] * self.SCALE)
        self.SCREEN_HEIGHT = int(self.ResolutionsHEIGHT[self.ResSelected] * self.SCALE)
