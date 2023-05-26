# -*- coding: utf-8 -*-

import pygame
import math
import random

class Math(object):

    def __new__(self, *args, **kargs):
        print ("Cuidado: Math(): No se debería instanciar esta clase.")
 
    @classmethod
    def degToRad(cls, aDeg):
        return aDeg * math.pi / 180
    
    @classmethod
    def radToDeg(cls, aRad):
        return aRad * 180 / math.pi

    @classmethod
    def clampDeg(cls, aDeg):
        aDeg = aDeg % 360
        if aDeg < 0:
            aDeg = aDeg + 360
        return aDeg

    @classmethod
    def randNumberBetween(cls, aInt1, aInt2):
        return random.randrange(aInt1, aInt2 + 1)

    @classmethod
    def rectRectCollision(cls, aX1, aY1, aW1, aH1, aX2, aY2, aW2, aH2):
        return ((((aX1 + aW1) > aX2) and (aX1 < (aX2 + aW2))) and (((aY1 + aH1) > aY2) and (aY1 < (aY2 + aH2))))

    @classmethod
    def circleCircleCollision(cls, aX1, aY1, aRadius1, aX2, aY2, aRadius2):
        return Math.distance(aX1, aY1, aX2, aY2) <= (aRadius1 + aRadius2)

    @classmethod
    def distance(cls, aX1, aY1, aX2, aY2):
        return math.sqrt(((aX2 - aX1) ** 2) + ((aY2 - aY1) ** 2))

    @classmethod
    def sign(cls, aN):
        if aN == 0:
            return 0
        elif aN > 0:
            return 1
        else:
            return -1
    
