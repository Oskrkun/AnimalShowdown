# -*- coding: utf-8 -*-

import pygame
from api.Manager import *

class ParticleManager(Manager):

    mInstance = None
    mInitialized = False

    def __new__(self, *args, **kargs):
        if (ParticleManager.mInstance is None):
            ParticleManager.mInstance = object.__new__(self, *args, **kargs)
            self.init(ParticleManager.mInstance)
        else:
            print ("Cuidado: ParticleManager(): No se debería instanciar más de una vez esta clase. Usar ParticleManager.inst().")
        return self.mInstance

    @classmethod
    def inst(cls):
        if (not cls.mInstance):
            return cls()
        return cls.mInstance
    
    def init(self):
        if (ParticleManager.mInitialized):
            return
            ParticleManager.mInitialized = True

        Manager.__init__(self)

    def update(self):
        Manager.update(self)

    def render(self, aScreen):
        Manager.render(self, aScreen)

    def addParticle(self, aParticle):
        Manager.add(self, aParticle)
      
    def destroy(self):
        Manager.destroy(self)

        ParticleManager.mInstance = None
