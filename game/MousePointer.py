# -*- coding: utf-8 -*-

import pygame
from api.AnimatedSprite import *
from api.AnimatedSprite import *
from pygame import *
from api.Mouse import *
from api.AssetManager import *
from game.states.MatchManager import *
from game.Reference import *
from api.GameConstants import *


class MousePointer(AnimatedSprite):
    # Máquina de estados.
    NORMAL = 0
    CLICKED = 2

    mostrarMouse = True

    #aRuta1 es la ruta de los frames de la animacion normal aRuta2 son cuando le hacen click se le pasa un ancho y alto a los botones para escalarlos
    def __init__(self):
        Sprite.__init__(self)

        p = int(10 * GameConstants.inst().SCALE)
        self.punta = Reference()
        self.punta.setImage(pygame.transform.scale(self.punta.mImg, (p, p)))

        self.mFramesNormal = AssetManager.inst().Pointer[0]
        self.mFramesClicked = AssetManager.inst().Pointer[1]

        #tamaño de los botones
        self.mWidth = self.mFramesNormal[0].get_width
        self.mHeight = self.mFramesNormal[0].get_height

        # Estado inicial.
        self.mState = MousePointer.NORMAL
        self.setState(MousePointer.NORMAL)

    def update(self):
        Sprite.update(self)
        self.setXY(Mouse.inst().getX(), Mouse.inst().getY())
        self.punta.setXY(Mouse.inst().getX() - self.mWidth * 0.45, Mouse.inst().getY() - self.mHeight * 0.40)

        if Mouse.inst().leftPressed():
            self.setState(MousePointer.CLICKED)

        if self.getState() == MousePointer.NORMAL:
            pass
        elif self.getState() == MousePointer.CLICKED:
            if self.isEnded():
                self.setState(MousePointer.NORMAL)
            #aca si se levanto el click paso a estado NORMAL

        AnimatedSprite.update(self)

    def render(self, aScreen):
        # Si el juego está en pausa se muestra el mensaje de pausa.
        if self.mostrarMouse:
            AnimatedSprite.render(self, aScreen)
            self.punta.render(aScreen)
        # AnimatedSprite.render(self, aScreen)

    # Establece el estado actual e inicializa las variables correspondientes
    # al estado.
    def setState(self, aState):
        AnimatedSprite.setState(self, aState)
        self.setVisible(True)
        if (self.getState() == MousePointer.NORMAL):
            self.initAnimation(self.mFramesNormal, 0, len(self.mFramesNormal)-1,2, True)
            #el array de frames que se va a reproducir donde empieza el delay si es ciclico o no alto y ancho
        #Cuando le hacen click
        elif self.getState() == MousePointer.CLICKED:
            self.initAnimation(self.mFramesClicked, 0,len(self.mFramesClicked)-1,2, False)

    def getPunta(self):
        return self.punta

    def destroy(self):
        AnimatedSprite.destroy(self)

        i = len(self.mFramesNormal)
        while i > 0:
            self.mFramesNormal[i - 1] = None
            self.mFramesNormal.pop(i - 1)
            i = i - 1

        # i = len(self.mFramesClicked)
        # while i > 0:
        #     self.mFramesClicked[i - 1] = None
        # self.mFramesClicked.pop(i - 1)
        # i = i - 1
