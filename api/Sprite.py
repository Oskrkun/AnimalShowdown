# -*- coding: utf-8 -*-

import pygame
from api.GameObject import *
from api.Math import *


class Sprite(GameObject):
    TOP_LEFT = 0
    CENTER = 1

    def __init__(self):

        GameObject.__init__(self)

        self.mImg = None

        self.mImgMaster = None

        self.mWidth = 0
        self.mHeight = 0

        self.mVisible = True

        self.mScore = 0

        self.mAngle = 0

        self.mRegistration = Sprite.CENTER

        self.mRadius = 0

        self.mFlipH = False

        self.mBoundingBoxOffsetX = 0
        self.mBoundingBoxOffsetY = 0
        self.mBoundingBoxWidth = 0
        self.mBoundingBoxHeight = 0

        self.mType = 0

    def setType(self, aType):
        self.mType = aType

    def getType(self):
        return self.mType

    def setRegistration(self, aRegistration):
        self.mRegistration = aRegistration

    def setImage(self, aImg):
        self.mImg = aImg
        self.mImgMaster = aImg

        self.mWidth = self.mImg.get_width()
        self.mHeight = self.mImg.get_height()

        if self.mRegistration == Sprite.CENTER:
            self.updateImage()
        else:
            if self.mBoundingBoxWidth == 0 and self.mBoundingBoxHeight == 0:
                self.mBoundingBoxWidth = self.mWidth
                self.mBoundingBoxHeight = self.mHeight

    def setAlpha(self, aAlpha):
        # no funciona
        # Color color = mSpriteRenderer.material.color;
        # mSpriteRenderer.material.color = new Color (color.r, color.g, color.b, aAlpha);
        pass

    def updateImage(self):
        self.mImg = pygame.transform.rotate(self.mImgMaster, self.mAngle)
        self.mWidth = self.mImg.get_width()
        self.mHeight = self.mImg.get_height()
        self.setRadius(self.getWidth() / 2)

    def update(self):
        GameObject.update(self)

    def render(self, aScreen):
        if self.mImg != None:
            if self.mVisible:
                img = self.mImg
                if self.mFlipH:
                    img = pygame.transform.flip(img, True, False)
                if self.mRegistration == Sprite.TOP_LEFT:
                    aScreen.blit(img, (self.getX(), self.getY()))
                elif self.mRegistration == Sprite.CENTER:
                    aScreen.blit(img, (self.getX() - self.getWidth() / 2, self.getY() - self.getHeight() / 2))

    def getWidth(self):
        return self.mWidth

    def getHeight(self):
        return self.mHeight

    def distance(self, aSprite):
        return Math.distance(self.getX(), self.getY(), aSprite.getX(), aSprite.getY())

    def collides(self, aSprite):
        if self.mRegistration == self.CENTER:
            x1 = self.getX() - self.getWidth() / 2
            y1 = self.getY() - self.getHeight() / 2
        else:  # self.mRegistration == self.TOP_LEFT
            x1 = self.getX()
            y1 = self.getY()
        w1 = self.getWidth()
        h1 = self.getHeight()

        if aSprite.mRegistration == aSprite.CENTER:
            x2 = aSprite.getX() - aSprite.getWidth() / 2
            y2 = aSprite.getY() - aSprite.getHeight() / 2
        else:  # aSprite.mRegistration == aSprite.TOP_LEFT
            x2 = aSprite.getX()
            y2 = aSprite.getY()
        w2 = aSprite.getWidth()
        h2 = aSprite.getHeight()

        if ((((x1 + w1) > x2) and (x1 < (x2 + w2))) and (((y1 + h1) > y2) and (y1 < (y2 + h2)))):
            return True
        else:
            return False

    def willCollide(self, aSprite):
        if self.mRegistration == self.CENTER:
            x1 = self.getX() - self.getWidth() / 2 + self.getVelX()
            y1 = self.getY() - self.getHeight() / 2 + self.getVelY()
        else:  # self.mRegistration == self.TOP_LEFT
            x1 = self.getX() + self.getVelX()
            y1 = self.getY() + self.getVelY()
        w1 = self.getWidth()
        h1 = self.getHeight()

        if aSprite.mRegistration == aSprite.CENTER:
            x2 = aSprite.getX() - aSprite.getWidth() / 2
            y2 = aSprite.getY() - aSprite.getHeight() / 2
        else:  # aSprite.mRegistration == aSprite.TOP_LEFT
            x2 = aSprite.getX()
            y2 = aSprite.getY()
        w2 = aSprite.getWidth()
        h2 = aSprite.getHeight()

        if ((((x1 + w1) > x2) and (x1 < (x2 + w2))) and (((y1 + h1) > y2) and (y1 < (y2 + h2)))):
            return True
        else:
            return False

    def collidesPoint(self, aSprite):
        x1 = self.getX() - self.getWidth() / 2
        y1 = self.getY() - self.getHeight() / 2
        w1 = self.getWidth()
        h1 = self.getHeight()

        x2 = aSprite.getX() - aSprite.getWidth() / 2
        y2 = aSprite.getY()
        w2 = aSprite.getWidth()
        h2 = aSprite.getHeight() / 2

        if ((((x1 + w1) > x2) and (x1 < (x2 + w2))) and (((y1 + h1) > y2) and (y1 < (y2 + h2)))):
            return True
        else:
            return False

    def turnLeft(self, aAngle):
        self.mAngle = self.mAngle + aAngle
        self.mAngle = Math.clampDeg(self.mAngle)
        self.updateImage()

    def turnRight(self, aAngle):
        self.mAngle = self.mAngle - aAngle
        self.mAngle = Math.clampDeg(self.mAngle)
        self.updateImage()

    def turnAngle(self, aAngle):
        self.mAngle = self.mAngle + aAngle
        self.mAngle = Math.clampDeg(self.mAngle)
        self.updateImage()

    def setAngle(self, aAngle):
        self.mAngle = Math.clampDeg(aAngle)
        self.updateImage()

    def lookAt(self, aX, aY):
        dx = aX - self.getX()
        dy = aY - self.getY()
        dy *= -1
        radians = math.atan2(dy, dx)
        self.setAngle(Math.radToDeg(radians))

    def getAngle(self):
        return self.mAngle

    def setVisible(self, aVisible):
        self.mVisible = aVisible

    def isVisible(self):
        return self.mVisible

    def setScore(self, aScore):
        self.mScore = aScore

    def getScore(self):
        return self.mScore

    def setRadius(self, aRadius):
        self.mRadius = aRadius

    def getRadius(self):
        return self.mRadius

    def setFlipH(self, aFlipH):
        self.mFlipH = aFlipH

    def setBoundingBox(self, aBoundingBoxOffsetX, aBoundingBoxOffsetY, aBoundingBoxWidth, aBoundingBoxHeight):
        self.mBoundingBoxOffsetX = aBoundingBoxOffsetX
        self.mBoundingBoxOffsetY = aBoundingBoxOffsetY
        self.mBoundingBoxWidth = aBoundingBoxWidth
        self.mBoundingBoxHeight = aBoundingBoxHeight

    def getBoundingBoxOffsetX(self):
        return self.mBoundingBoxOffsetX

    def getBoundingBoxOffsetY(self):
        return self.mBoundingBoxOffsetY

    def getBoundingBoxWidth(self):
        return self.mBoundingBoxWidth

    def getBoundingBoxHeight(self):
        return self.mBoundingBoxHeight

    def destroy(self):
        GameObject.destroy(self)
        self.mImg = None
        self.mImgMaster = None
