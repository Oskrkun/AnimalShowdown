# -*- coding: utf-8 -*-

import pygame
from api.Sprite import *

class TextSprite(Sprite):

    def __init__(self, aText = "", aFontSize = 10, aFontName = "", aColor = (0xFF, 0xFF, 0xFF)):

        Sprite.__init__(self)

        self.mText = aText
        self.mFontSize = aFontSize
        self.mFontName = aFontName
        self.mColor = aColor
        self.updateImageTxt()

    # Función genérica para dibujar un texto en una superficie.
    @classmethod
    def drawText(self, aScreen, aX, aY, aMsg, aFontName, aFontSize, aColor=(0,0,0)):
        font = pygame.font.Font(aFontName, aFontSize)
        imgTxt = font.render(aMsg, True, aColor)
        aScreen.blit(imgTxt, (aX, aY))

    def setText(self, aText):
        if self.mText != aText:
            self.mText = aText
            self.updateImageTxt()

    def setFontName(self, aFontName):
        if self.mFontName != aFontName:
            self.mFontName = aFontName
            self.updateImage()
            
    def setSize(self, aFontSize):
        if self.mFontSize != aFontSize:
            self.mFontSize = aFontSize
            self.updateImage()
        
    def setColor(self, aColor):
        if self.mColor != aColor:
            self.mColor = aColor
            self.updateImage()
        
    def updateImageTxt(self):
        if (self.mFontName == ""):
            font = pygame.font.SysFont("Comic Sans MS", self.mFontSize)
        else:
            font = pygame.font.Font(self.mFontName, self.mFontSize)
        imgTxt = font.render(self.mText, True, self.mColor)
        self.setImage(imgTxt)
    
    def update(self):
        Sprite.update(self)
        
    def render(self, aScreen):
        Sprite.render(self, aScreen)

    def destroy(self):
        Sprite.destroy(self)
