# -*- coding: utf-8 -*-

from api.Vector import *

class GameObject(object):

    # Comportamientos del objeto al llegar a un borde.
    NONE = 0     # No tiene ninguno, el objeto sigue de largo.
    STOP = 1     # El objeto se detiene al alcanzar un borde.
    WRAP = 2     # El objeto aparece por el lado contrario.
    BOUNCE = 3   # El objeto rebota en el borde.
    DIE = 4      # El objeto se marca para ser eliminado.
    
    def __init__(self):

        self.mPos = Vector(0, 0)

        self.mVel = Vector(0, 0)

        self.mAccel = Vector(0, 0)

        self.mMinX = 0
        self.mMaxX = 0
        self.mMinY = 0
        self.mMaxY = 0

        self.mBoundAction = GameObject.NONE

        self.mIsDead = False

        self.mState = 0

        self.mTimeState = 0

        self.mFriction = 1

        self.mMaxSpeed = 150

        self.mID = 0

    def setX(self, aX):
        self.mPos.setX(aX)

    def setY(self, aY):
        self.mPos.setY(aY)
        
    def setXY(self, aX, aY):
        self.mPos.setX(aX)
        self.mPos.setY(aY)

    def getX(self):
        return int(self.mPos.getX())

    def getY(self):
        return int(self.mPos.getY())

    def setAngMag(self, aAng, aMag):
        self.mPos.setAngMag(aAng, aMag)
    
    def setVelX(self, aVelX):
        self.mVel.setX(aVelX)

        # Controlar la velocidad máxima.
        self.mVel.truncate(self.mMaxSpeed)

    def setVelY(self, aVelY):
        self.mVel.setY(aVelY)

        # Controlar la velocidad máxima.
        self.mVel.truncate(self.mMaxSpeed)

    def setVelXY(self, aVelX, aVelY):
        self.mVel.setX(aVelX)
        self.mVel.setY(aVelY)

        # Controlar la velocidad máxima.
        self.mVel.truncate(self.mMaxSpeed)

    def getVelX(self):
        return self.mVel.getX()

    def getVelY(self):
        return self.mVel.getY()

    def setVelAngMag(self, aAng, aMag):
        self.mVel.setAngMag(aAng, aMag)
        
    def setAccelX(self, aAccelX):
        self.mAccel.setX(aAccelX)

    def setAccelY(self, aAccelY):
        self.mAccel.setY(aAccelY)

    def setAccelXY(self, aAccelX, aAccelY):
        self.mAccel.setX(aAccelX)
        self.mAccel.setY(aAccelY)

    def getAccelX(self):
        return self.mAccel.getX()

    def getAccelY(self):
        return self.mAccel.getY()

    def setAccelAngMag(self, aAng, aMag):
        self.mAccel.setAngMag(aAng, aMag)
        
    def setBounds(self, aMinX, aMinY, aMaxX, aMaxY):
        self.mMinX = aMinX
        self.mMaxX = aMaxX
        self.mMinY = aMinY
        self.mMaxY = aMaxY

    def setBoundAction(self, aBoundAction):
        self.mBoundAction = aBoundAction
        
    def update(self):
        self.setVelXY(round(self.getVelX(), 2), round(self.getVelY(), 2))
        self.setAccelXY(round(self.getAccelX(), 2), round(self.getAccelY(), 2))
        
        self.mTimeState = self.mTimeState + 1

        self.mVel.add(self.mAccel)

        self.mVel.mul(self.mFriction)

        # Controlar la velocidad máxima.
        self.mVel.truncate(self.mMaxSpeed)

        self.mPos.add(self.mVel)

        self.checkBounds()

    def checkBounds(self):
        if self.mBoundAction == GameObject.NONE:
            return

        left = (self.getX() < self.mMinX)
        right = (self.getX() > self.mMaxX)
        up = (self.getY() < self.mMinY)
        down = (self.getY() > self.mMaxY)

        if not (left or right or up or down):
            return

        if (self.mBoundAction == GameObject.WRAP):
            if (left):
                self.setX(self.mMaxX)
            if (right):
                self.setX(self.mMinX)
            if (up):
                self.setY(self.mMaxY)
            if (down):
                self.setY(self.mMinY)
        else:
            if (left):
                self.setX(self.mMinX)
            if (right):
                self.setX(self.mMaxX)
            if (up):
                self.setY(self.mMinY)
            if (down):
                self.setY(self.mMaxY)

        if (self.mBoundAction == GameObject.STOP or self.mBoundAction == GameObject.DIE):
            self.setVelXY(0, 0)

        elif (self.mBoundAction == GameObject.BOUNCE):
            if (right or left):
                self.setVelX(self.getVelX() * -1)
            if (up or down):
                self.setVelY(self.getVelY() * -1)

        if (self.mBoundAction == GameObject.DIE):
            self.mIsDead = True
            return

    def touchesBounds(self):
        left = (self.getX() < self.mMinX)
        right = (self.getX() > self.mMaxX)
        up = (self.getY() < self.mMinY)
        down = (self.getY() > self.mMaxY)

        return left or right or up or down

    def isDead(self):
        return self.mIsDead

    def die(self):
        self.mIsDead = True

    def stopMove(self):
        self.mVel.setXY(0, 0)
        self.mAccel.setXY(0, 0)

    def getState(self):
        return self.mState

    def setState(self, aState):
        self.mState = aState
        self.mTimeState = 0

    def getTimeState(self):
        return self.mTimeState

    def setFriction(self, aFriction):
        self.mFriction = aFriction

    def getFriction(self):
        return self.mFriction

    def setMaxSpeed(self, aMaxSpeed):
        self.mMaxSpeed = aMaxSpeed

    def getMaxSpeed(self):
        return self.mMaxSpeed

    def setID(self, aID):
        self.mID = aID

    def getID(self):
        return self.mID

    def getBounds(self):
        bounds = []
        bounds.append(self.mMinX)  # 0
        bounds.append(self.mMaxX)  # 1
        bounds.append(self.mMinY)  # 2
        bounds.append(self.mMaxY)  # 3
        return bounds

    def destroy(self):   
        self.mPos = None
        self.mVel = None
        self.mAccel = None
