import pygame
from api.GameObject import *
from api.GameConstants import *
from api.Sprite import *


class Stadium(GameObject):

    screenWidth = GameConstants.inst().SCREEN_WIDTH
    screenHeight = GameConstants.inst().SCREEN_HEIGHT

    mImg = None

    Pause = False

    ID = 0

    UpperLimit = None
    LowerLimit = None
    LeftLimit1 = None
    LeftLimit2 = None
    RightLimit1 = None
    RightLimit2 = None

    def __init__(self):
        GameObject.__init__(self)

    def update(self):
        GameObject.update(self)

        self.UpperLimit.update()
        self.LowerLimit.update()
        self.LeftLimit1.update()
        self.LeftLimit2.update()
        self.RightLimit1.update()
        self.RightLimit2.update()

    def render(self, aScreen):
        self.UpperLimit.render(aScreen)
        self.LowerLimit.render(aScreen)
        self.LeftLimit1.render(aScreen)
        self.LeftLimit2.render(aScreen)
        self.RightLimit1.render(aScreen)
        self.RightLimit2.render(aScreen)

    def depth(self, disk, p1, p2):
        renderOrder = []

        if p1.getY() < p2.getY():
            renderOrder.append(p1)
            renderOrder.append(p2)
        else:
            renderOrder.append(p2)
            renderOrder.append(p1)

        if disk.getY() < renderOrder[0].getY():
            renderOrder.insert(0, disk)
        elif disk.getY() < renderOrder[1].getY():
            renderOrder.insert(1, disk)
        else:
            renderOrder.append(disk)

        return renderOrder

    def destroy(self):
        GameObject.destroy(self)
