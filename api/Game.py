# -*- coding: utf-8 -*-



# Ensure that the computer is running Windows Vista or newer
import os, sys
if os.name != "nt" or sys.getwindowsversion()[0] < 6:
    raise NotImplementedError('this script requires Windows Vista or newer')

# Ensure that ctypes is installed. It is included with Python 2.5 and newer,
# but Python 2.4 users must install ctypes manually.
try:
    import ctypes
except ImportError:
    print('install ctypes from http://sourceforge.net/projects/ctypes/files/ctypes')
    raise

user32 = ctypes.windll.user32
user32.SetProcessDPIAware()

#Esto Centra la ventana del juego para que no aparesca en cualquier lado de la pantalla
os.environ['SDL_VIDEO_CENTERED'] = '1'

#-----------------------------------------------------------------------------------------------------

import pygame
from api.Keyboard import *
from api.GameConstants import *
from api.Mouse import *
from game.MousePointer import *
from game.Settings import *
import gc
from api.TextSprite import *

class Game(object):

    mInstance = None
    mInitialized = False

    mScreen = None
    mImgBackground = None
    mClock = None
    mSalir = False
    mMousePointer = None

    mState = None

    SCREEN_WIDTH = 0
    SCREEN_HEIGHT = 0
    RESOLUTION = 0
    mIsFullscreen = False

    mShowGamePointer = False

    mostrarBordesVentana = False

    FPS = 60

    def __new__(self, *args, **kargs):
        if (Game.mInstance is None):
            Game.mInstance = object.__new__(self, *args, **kargs)
            self.init(Game.mInstance)
        else:
            print ("Cuidado: Game(): No se debería instanciar más de una vez esta clase. Usar Game.inst().")
        return self.mInstance

    @classmethod
    def inst(cls):
        if (not cls.mInstance):
            return cls()
        return cls.mInstance

    def init(self):
        if (Game.mInitialized):
            return
        Game.mInitialized = True

        Game.SCREEN_WIDTH = GameConstants.inst().SCREEN_WIDTH
        Game.SCREEN_HEIGHT = GameConstants.inst().SCREEN_HEIGHT
        Game.RESOLUTION = (Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT)

        pygame.mixer.pre_init(44100, -16, 2, 2048)
        # pygame.mixer.init()
        pygame.init()

        if Game.mostrarBordesVentana:
            Game.mScreen = pygame.display.set_mode(Game.RESOLUTION)
        else:
            Game.mScreen = pygame.display.set_mode(Game.RESOLUTION, pygame.NOFRAME)

        pygame.display.set_caption("AnimalJammers")

        Game.mBackground = pygame.Surface(self.mScreen.get_size())
        Game.mBackground = self.mBackground.convert()

        Game.mClock = pygame.time.Clock()
        Game.mSalir = False

        self.mShowGamePointer = True
        self.showGamePointer(True)

        Game.mState = None

    def showGamePointer(self, aShowGamePointer):
        self.mShowGamePointer = aShowGamePointer

        if (aShowGamePointer):
            pygame.mouse.set_visible(False)
            Game.mMousePointer = MousePointer()
        else:
            pygame.mouse.set_visible(True)
            if (Game.mMousePointer != None):
                Game.mMousePointer.destroy()
                Game.mMousePointer = None

    def setState(self, aState):
        if (Game.mState != None):
            Game.mState.destroy()
            Game.mState = None
            print (gc.collect(), " objectos borrados.")

        Game.mState = aState
        Game.mState.init()

    def getState(self):
        return Game.mState

    def gameLoop(self):

        while not self.mSalir:

            Game.mClock.tick(Game.FPS)

            #print(Game.mClock.get_fps())

            AudioManager.inst().update()
            Keyboard.inst().update()
            Mouse.inst().update()

            if (Game.mMousePointer != None):
                Game.mMousePointer.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    Keyboard.inst().keyDown(event.key)
                if event.type == pygame.KEYUP:
                    Keyboard.inst().keyUp(event.key)

            Game.mScreen.blit(self.mBackground, (0, 0))

            Game.mState.update()

            Game.mState.render()

            if (Game.mMousePointer != None):
                Game.mMousePointer.render(self.mScreen)

            pygame.display.flip()

    def setBackground(self, aBackgroundImage):
        Game.mBackground = None
        Game.mBackground = aBackgroundImage
        self.blitBackground(Game.mBackground)

    def blitBackground(self, aBackgroundImage):
        Game.mScreen.blit(aBackgroundImage, (0, 0))

    def getScreen(self):
        return Game.mScreen

    def fullORnot(self):
        if self.mIsFullscreen:
            Game.mScreen = pygame.display.set_mode(Game.RESOLUTION, pygame.FULLSCREEN)
        else:
            if Game.mostrarBordesVentana:
                Game.mScreen = pygame.display.set_mode(Game.RESOLUTION)
            else:
                Game.mScreen = pygame.display.set_mode(Game.RESOLUTION, pygame.NOFRAME)

    def destroy(self):
        if (Game.mState != None):
            Game.mState.destroy()
            Game.mState = None

        Keyboard.inst().destroy()
        Mouse.inst().destroy()
        Settings.inst().destroy()

        if (Game.mMousePointer != None):
            Game.mMousePointer.destroy()
            Game.mMousePointer = None

        pygame.mouse.set_visible(True)

        Game.mInstance = None

        pygame.quit()
