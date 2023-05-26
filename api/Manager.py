# -*- coding: utf-8 -*-

import pygame

class Manager(object):

    def __init__(self):
        
        self.mArray = []

    def update(self):
        for e in self.mArray:
            e.update()

        i = len(self.mArray)
        while i > 0:
            if self.mArray[i-1].isDead():
                self.mArray[i-1].destroy()
                self.mArray.pop(i-1)
            i = i - 1

    def render(self, aScreen):
        for e in self.mArray:
            e.render(aScreen)

    def add(self, aElement):
        self.mArray.append(aElement)

    # Determina si el sprite que se recibe como parámetro choca con alguno de los sprites de la lista.
    # Retorna el sprite si colisiona con alguno (el primero que colisione) y None si no colisiona con ninguno.
    def collides(self, aSprite):
        i = 0
        while i < len(self.mArray):
            if aSprite.collides(self.mArray[i]):
                return self.mArray[i]
            i = i + 1
        return None

    def getLength(self):
        return len(self.mArray)
    
    def destroy(self):
        i = len(self.mArray)
        while i > 0:
            self.mArray[i-1].destroy()
            self.mArray.pop(i-1)
            i = i - 1
