# -*- coding: utf-8 -*-

import pygame
from api.Manager import *

class BulletManager(Manager):

    mInstance = None
    mInitialized = False

    def __new__(self, *args, **kargs):
        if (BulletManager.mInstance is None):
            BulletManager.mInstance = object.__new__(self, *args, **kargs)
            self.init(BulletManager.mInstance)
        else:
            print ("Cuidado: BulletManager(): No se debería instanciar más de una vez esta clase. Usar BulletManager.inst().")
        return self.mInstance

    @classmethod
    def inst(cls):
        if (not cls.mInstance):
            return cls()
        return cls.mInstance
    
    def init(self):
        if (BulletManager.mInitialized):
            return
        BulletManager.mInitialized = True

        Manager.__init__(self)

    def update(self):
        Manager.update(self)

    def render(self, aScreen):
        Manager.render(self, aScreen)

    def addBullet(self, aBullet):
        Manager.add(self, aBullet)
      
    def destroy(self):
        Manager.destroy(self)

        BulletManager.mInstance = None
