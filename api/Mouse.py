# -*- coding: utf-8 -*-

import pygame

class Mouse(object):

    mInstance = None
    mInitialized = False

    mLeftPressed = False
    mRightPressed = False
    mCenterPressed = False

    mLeftPressedPreviousFrame = False

    def __new__(self, *args, **kargs):
        if (Mouse.mInstance is None):
            Mouse.mInstance = object.__new__(self, *args, **kargs)
            self.init(Mouse.mInstance)
        else:
            print ("Cuidado: Mouse(): No se debería instanciar más de una vez esta clase. Usar Mouse.inst().")
        return Mouse.mInstance

    @classmethod
    def inst(cls):
        if (not cls.mInstance):
            return cls()
        return cls.mInstance
    
    def init(self):
        if (Mouse.mInitialized):
            return
        Mouse.mInitialized = True
        
        Mouse.mLeftPressed = False
        Mouse.mRightPressed = False
        Mouse.mCenterPressed = False
        Mouse.mLeftPressedPreviousFrame = False

    def update(self):
        Mouse.mLeftPressedPreviousFrame = Mouse.mLeftPressed
        Mouse.mLeftPressed = pygame.mouse.get_pressed()[0]
        Mouse.mRightPressed = pygame.mouse.get_pressed()[2]
        Mouse.mCenterPressed = pygame.mouse.get_pressed()[1]

    def leftPressed(self):
        return Mouse.mLeftPressed

    def rightPressed(self):
        return Mouse.mRightPressed

    def centerPressed(self):
        return Mouse.mCenterPressed

    def click(self):
        return Mouse.mLeftPressed == False and Mouse.mLeftPressedPreviousFrame == True

    def getPos(self):
        return pygame.mouse.get_pos()
    
    def getX(self):
        return pygame.mouse.get_pos()[0]
    
    def getY(self):
        return pygame.mouse.get_pos()[1]

    def destroy(self):
        Mouse.mInstance = None
