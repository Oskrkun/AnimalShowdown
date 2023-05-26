# -*- coding: utf-8 -*-

import math
from math import *
from api.Math import *

class Vector(object):
    
    x = 0.0
    y = 0.0

    # Constante para no dividir por cero.
    EPSILON = 0.000001

    def __init__(self, aX = 0.0, aY = 0.0):
        self.x = aX
        self.y = aY

    def setX(self, aX):
        self.x = aX

    def setY(self, aY):
        self.y = aY
        
    def setXY(self, aX, aY):
        self.x = aX
        self.y = aY
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y

    def add(self, aVec):
        self.x += aVec.x
        self.y += aVec.y

    def mul(self, aScale):
        self.x *= aScale
        self.y *= aScale

    def mag(self): 
        return math.sqrt(self.x * self.x + self.y * self.y)

    def normalize(self):
        self.m = self.mag();

        if (self.m > self.EPSILON):
            self.x /= self.m;
            self.y /= self.m;
    
    def truncate(self, aLength):
        if (self.mag() > aLength):
            self.normalize()
            self.mul(aLength)

    # Establecer el vector usando ángulo y magnitud.
    def setAngMag(self, aAng, aMag):
        radians = Math.degToRad(aAng)
        self.x = aMag * math.cos(radians)
        self.y = aMag * math.sin(radians)
        self.y *= -1
