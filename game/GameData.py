# -*- coding: utf-8 -*-

import pygame
class GameData(object):

    mInstance = None
    mInitialized = False

    mPuntajeJugador1 = 0
    mPuntajeJugador2 = 0

    mTipoJugador1 = 0
    mTipoJugador2 = 1

    mEstadio = 1

    mPerfil = []

    def __new__(self, *args, **kargs):
        if (GameData.mInstance is None):
            GameData.mInstance = object.__new__(self, *args, **kargs)
            self.init(GameData.mInstance)
        else:
            print ("Cuidado: GameData(): No se debería instanciar más de una vez esta clase. Usar GameData.inst().")
        return self.mInstance

    @classmethod
    def inst(cls):
        if (not cls.mInstance):
            return cls()
        return cls.mInstance

    def init(self):
        if (GameData.mInitialized):
            return
        GameData.mInitialized = True


        GameData.mPuntajeJugador1 = 0
        GameData.mPuntajeJugador2 = 0

        GameData.mTipoJugador1 = 1
        GameData.mTipoJugador2 = 2
        GameData.mEstadio = 1


#--------------------------jugador 1-----------------------------------------------------------------------------
    def setPuntajeJugador1(self, aScore):
        GameData.mPuntajeJugador1 += aScore
        self.controlScores()

    def getScoreJugador1(self):
        return GameData.mPuntajeJugador1

    def setPersonajeJugador1(self,atype):
        GameData.mTipoJugador1 = atype

    def getTypePersonaje1(self):
        return GameData.mTipoJugador1


#----------------------------------------------------------------------------------------------------------------

#---------------------------jugador 2----------------------------------------------------------------------------
    def setPuntajeJugador2(self, aScore):
        GameData.mPuntajeJugador2 += aScore
        self.controlScores()

    def getScoreJugador2(self):
        return GameData.mPuntajeJugador2

    def setPersonajeJugador2(self,atype):
        GameData.mTipoJugador2 = atype

    def getTypePersonaje2(self):
        return GameData.mTipoJugador2
#----------------------------------------------------------------------------------------------------------------

#--------------------------Estadio-------------------------------------------------------------------------------
    def setEstadio(self,aType):
        GameData.mEstadio = aType

#----------------------------------------------------------------------------------------------------------------

#--------------------------PefilPersonajes-----------------------------------------------------------------------




    def restartInst(self):
        GameData.mPuntajeJugador1 = 0
        GameData.mPuntajeJugador2 = 0

        GameData.mTipoJugador1 = 1
        GameData.mTipoJugador2 = 2
        GameData.mEstadio = 1



    def destroy(self):
        GameData.mInstance = None