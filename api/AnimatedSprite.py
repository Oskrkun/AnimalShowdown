# -*- coding: utf-8 -*-

import pygame

from api.Sprite import *

class AnimatedSprite(Sprite):

    def __init__(self):

        Sprite.__init__(self)

        self.mFrame = None

        self.mCurrentFrame = 0

        self.mTimeFrame = 0

        self.mDelay = 0

        self.mIsLoop = True

        self.mEnded = False

        self.mEndFrame = 0

        self.mPaused = False

        self.mStartFrame = 0

        self.mOldFrame = 0

    def initAnimation(self, aFramesArray, aStartFrame, aEndFrame, aDelay, aIsLoop):
        self.mPaused = False
        self.mFrame = aFramesArray
        self.mCurrentFrame = aStartFrame
        self.mTimeFrame = 0
        self.mDelay = aDelay
        self.mIsLoop = aIsLoop
        self.mEnded = False
        self.mOldFrame = aStartFrame
        if aEndFrame == -1:
            self.mEndFrame = len(self.mFrame) - 1
        else:
            self.mEndFrame = aEndFrame
        self.mStartFrame = aStartFrame
        self.setImage(self.mFrame[self.mCurrentFrame])
        
    def update(self):
        Sprite.update(self)

        if self.mPaused:
            return

        self.mOldFrame = self.mCurrentFrame

        self.mTimeFrame = self.mTimeFrame + 1
        if (self.mTimeFrame > self.mDelay):
            self.mTimeFrame = 0

            if not self.mEnded:
                self.mCurrentFrame = self.mCurrentFrame + 1
                if self.mCurrentFrame > self.mEndFrame:
                    if self.mIsLoop:
                        self.mCurrentFrame = self.mStartFrame
                    else:
                        self.mCurrentFrame = self.mEndFrame
                        self.mEnded = True
                self.setImage(self.mFrame[self.mCurrentFrame])

    def render(self, aScreen):
        Sprite.render(self, aScreen)

    def isEnded(self):
        return self.mEnded

    def gotoAndStop(self, aFrame):
        if aFrame >= 0 and aFrame <= (len(self.mFrame)-1):
            # Optimización: si el cuadro es el mismo, no se genera la imagen.
            if (self.mCurrentFrame != aFrame):
                self.setImage(self.mFrame[aFrame])

            self.mCurrentFrame = aFrame
            self.mEnded = True

    def gotoAndPlay(self, aFrame):
        self.mPaused = False
        if aFrame >= 0 and aFrame <= (len(self.mFrame)-1):
            self.mCurrentFrame = aFrame
            self.setImage(self.mFrame[self.mCurrentFrame])
            self.mEnded = False
            self.mTimeFrame = 0
            self.mEndFrame = len(self.mFrame)-1

    def getCurrentFrame(self):
        return self.mCurrentFrame

    def getOldFrame(self):
        return self.mOldFrame

    def pauseAnimation(self):
        self.mPaused = True

    def continueAnimation(self):
        self.mPaused = False
            
    def destroy(self):
        Sprite.destroy(self)
        i = len(self.mFrame)
        while i > 0:
            self.mFrame[i-1] = None
            self.mFrame.pop(i-1)
            i = i - 1
