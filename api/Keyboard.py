# -*- coding: utf-8 -*-

import pygame

class Keyboard(object):


    zeroZone = 0.4
    joysticks = []
    cantJoy = 0

    mInstance = None
    mInitialized = False

    # Arrow Pressed
    mLeftPressed = False
    mRightPressed = False
    mUpPressed = False
    mDownPressed = False

    # Arrow PressedPreviousFrame
    mLeftPressedPreviousFrame = False
    mRightPressedPreviousFrame = False
    mUpPressedPreviousFrame = False
    mDownPressedPreviousFrame = False

    # Alphabet Pressed
    mQPressed = False
    mWPressed = False
    mEPressed = False
    mRPressed = False
    mTPressed = False
    mYPressed = False
    mUPressed = False
    mIPressed = False
    mOPressed = False
    mPPressed = False
    mAPressed = False
    mSPressed = False
    mDPressed = False
    mFPressed = False
    mGPressed = False
    mHPressed = False
    mJPressed = False
    mKPressed = False
    mLPressed = False
    mZPressed = False
    mXPressed = False
    mCPressed = False
    mVPressed = False
    mBPressed = False
    mNPressed = False
    mMPressed = False

    # Alphabet PressedPreviousFrame
    mQPressedPreviousFrame = False
    mWPressedPreviousFrame = False
    mEPressedPreviousFrame = False
    mRPressedPreviousFrame = False
    mTPressedPreviousFrame = False
    mYPressedPreviousFrame = False
    mUPressedPreviousFrame = False
    mIPressedPreviousFrame = False
    mOPressedPreviousFrame = False
    mPPressedPreviousFrame = False
    mAPressedPreviousFrame = False
    mSPressedPreviousFrame = False
    mDPressedPreviousFrame = False
    mFPressedPreviousFrame = False
    mGPressedPreviousFrame = False
    mHPressedPreviousFrame = False
    mJPressedPreviousFrame = False
    mKPressedPreviousFrame = False
    mLPressedPreviousFrame = False
    mZPressedPreviousFrame = False
    mXPressedPreviousFrame = False
    mCPressedPreviousFrame = False
    mVPressedPreviousFrame = False
    mBPressedPreviousFrame = False
    mNPressedPreviousFrame = False
    mMPressedPreviousFrame = False

    # Command Pressesd
    mSpacePressed = False
    mEnterPressed = False
    mEscapePressed = False

    # Command PressesdPrevious
    mSpacePressedPreviousFrame = False
    mEnterPressedPreviousFrame = False
    mEscapePressedPreviousFrame = False

    def __new__(self, *args, **kargs):
        if (Keyboard.mInstance is None):
            Keyboard.mInstance = object.__new__(self, *args, **kargs)
            self.init(Keyboard.mInstance)
        return Keyboard.mInstance

    @classmethod
    def inst(cls):
        if (not cls.mInstance):
            return cls()
        return cls.mInstance

    def init(self):
        if (Keyboard.mInitialized):
            return
        Keyboard.mInitialized = True

        # for al the connected joysticks
        for i in range(0, pygame.joystick.get_count()):
            # create an Joystick object in our list
            Keyboard.joysticks.append(pygame.joystick.Joystick(i))
            # initialize them all (-1 means loop forever)
            Keyboard.joysticks[-1].init()
            # print a statement telling what the name of the controller is
            print("Detected joystick '", Keyboard.joysticks[-1].get_name(), "'")

        Keyboard.cantJoy = len(Keyboard.joysticks)

        # Arrow Pressed
        Keyboard.mLeftPressed = False
        Keyboard.mRightPressed = False
        Keyboard.mUpPressed = False
        Keyboard.mDownPressed = False

        # Arrow PressedPreviousFrame
        Keyboard.mLeftPressedPreviousFrame = False
        Keyboard.mRightPressedPreviousFrame = False
        Keyboard.mUpPressedPreviousFrame = False
        Keyboard.mDownPressedPreviousFrame = False

        # Alphabet Pressed
        Keyboard.mQPressed = False
        Keyboard.mWPressed = False
        Keyboard.mEPressed = False
        Keyboard.mRPressed = False
        Keyboard.mTPressed = False
        Keyboard.mYPressed = False
        Keyboard.mUPressed = False
        Keyboard.mIPressed = False
        Keyboard.mOPressed = False
        Keyboard.mPPressed = False
        Keyboard.mAPressed = False
        Keyboard.mSPressed = False
        Keyboard.mDPressed = False
        Keyboard.mFPressed = False
        Keyboard.mGPressed = False
        Keyboard.mHPressed = False
        Keyboard.mJPressed = False
        Keyboard.mKPressed = False
        Keyboard.mLPressed = False
        Keyboard.mZPressed = False
        Keyboard.mXPressed = False
        Keyboard.mCPressed = False
        Keyboard.mVPressed = False
        Keyboard.mBPressed = False
        Keyboard.mNPressed = False
        Keyboard.mMPressed = False

        # Alphabet PressedPreviousFrame
        Keyboard.mQPressedPreviousFrame = False
        Keyboard.mWPressedPreviousFrame = False
        Keyboard.mEPressedPreviousFrame = False
        Keyboard.mRPressedPreviousFrame = False
        Keyboard.mTPressedPreviousFrame = False
        Keyboard.mYPressedPreviousFrame = False
        Keyboard.mUPressedPreviousFrame = False
        Keyboard.mIPressedPreviousFrame = False
        Keyboard.mOPressedPreviousFrame = False
        Keyboard.mPPressedPreviousFrame = False
        Keyboard.mAPressedPreviousFrame = False
        Keyboard.mSPressedPreviousFrame = False
        Keyboard.mDPressedPreviousFrame = False
        Keyboard.mFPressedPreviousFrame = False
        Keyboard.mGPressedPreviousFrame = False
        Keyboard.mHPressedPreviousFrame = False
        Keyboard.mJPressedPreviousFrame = False
        Keyboard.mKPressedPreviousFrame = False
        Keyboard.mLPressedPreviousFrame = False
        Keyboard.mZPressedPreviousFrame = False
        Keyboard.mXPressedPreviousFrame = False
        Keyboard.mCPressedPreviousFrame = False
        Keyboard.mVPressedPreviousFrame = False
        Keyboard.mBPressedPreviousFrame = False
        Keyboard.mNPressedPreviousFrame = False
        Keyboard.mMPressedPreviousFrame = False

        # Command Pressesd
        Keyboard.mSpacePressed = False
        Keyboard.mEnterPressed = False

        # Command PressesdPrevious
        Keyboard.mSpacePressedPreviousFrame = False
        Keyboard.mEnterPressedPreviousFrame = False

    def keyDown(self, key):
        # If Arrow Pressed
        if (key == pygame.K_LEFT):
            Keyboard.mLeftPressed = True
        if (key == pygame.K_RIGHT):
            Keyboard.mRightPressed = True
        if (key == pygame.K_UP):
            Keyboard.mUpPressed = True
        if (key == pygame.K_DOWN):
            Keyboard.mDownPressed = True

        # If Alphabet Pressed
        if (key == pygame.K_q):
            Keyboard.mQPressed = True
        if (key == pygame.K_w):
            Keyboard.mWPressed = True
        if (key == pygame.K_e):
            Keyboard.mEPressed = True
        if (key == pygame.K_r):
            Keyboard.mRPressed = True
        if (key == pygame.K_t):
            Keyboard.mTPressed = True
        if (key == pygame.K_y):
            Keyboard.mYPressed = True
        if (key == pygame.K_u):
            Keyboard.mUPressed = True
        if (key == pygame.K_i):
            Keyboard.mIPressed = True
        if (key == pygame.K_o):
            Keyboard.mOPressed = True
        if (key == pygame.K_p):
            Keyboard.mPPressed = True
        if (key == pygame.K_a):
            Keyboard.mAPressed = True
        if (key == pygame.K_s):
            Keyboard.mSPressed = True
        if (key == pygame.K_d):
            Keyboard.mDPressed = True
        if (key == pygame.K_f):
            Keyboard.mFPressed = True
        if (key == pygame.K_g):
            Keyboard.mGPressed = True
        if (key == pygame.K_h):
            Keyboard.mHPressed = True
        if (key == pygame.K_j):
            Keyboard.mJPressed = True
        if (key == pygame.K_k):
            Keyboard.mKPressed = True
        if (key == pygame.K_l):
            Keyboard.mLPressed = True
        if (key == pygame.K_z):
            Keyboard.mZPressed = True
        if (key == pygame.K_x):
            Keyboard.mXPressed = True
        if (key == pygame.K_c):
            Keyboard.mCPressed = True
        if (key == pygame.K_v):
            Keyboard.mVPressed = True
        if (key == pygame.K_b):
            Keyboard.mBPressed = True
        if (key == pygame.K_n):
            Keyboard.mNPressed = True
        if (key == pygame.K_m):
            Keyboard.mMPressed = True

        # If Command Pressed
        if (key == pygame.K_RETURN):
            Keyboard.mEnterPressed = True
        if (key == pygame.K_SPACE):
            Keyboard.mSpacePressed = True
        if (key == pygame.K_ESCAPE):
            Keyboard.mEscapePressed = True

    def keyUp(self, key):
        # If Arrow Pressed
        if (key == pygame.K_LEFT):
            Keyboard.mLeftPressed = False
        if (key == pygame.K_RIGHT):
            Keyboard.mRightPressed = False
        if (key == pygame.K_UP):
            Keyboard.mUpPressed = False
        if (key == pygame.K_DOWN):
            Keyboard.mDownPressed = False

        # If Alphabet Pressed
        if (key == pygame.K_q):
            Keyboard.mQPressed = False
        if (key == pygame.K_w):
            Keyboard.mWPressed = False
        if (key == pygame.K_e):
            Keyboard.mEPressed = False
        if (key == pygame.K_r):
            Keyboard.mRPressed = False
        if (key == pygame.K_t):
            Keyboard.mTPressed = False
        if (key == pygame.K_y):
            Keyboard.mYPressed = False
        if (key == pygame.K_u):
            Keyboard.mUPressed = False
        if (key == pygame.K_i):
            Keyboard.mIPressed = False
        if (key == pygame.K_o):
            Keyboard.mOPressed = False
        if (key == pygame.K_p):
            Keyboard.mPPressed = False
        if (key == pygame.K_a):
            Keyboard.mAPressed = False
        if (key == pygame.K_s):
            Keyboard.mSPressed = False
        if (key == pygame.K_d):
            Keyboard.mDPressed = False
        if (key == pygame.K_f):
            Keyboard.mFPressed = False
        if (key == pygame.K_g):
            Keyboard.mGPressed = False
        if (key == pygame.K_h):
            Keyboard.mHPressed = False
        if (key == pygame.K_j):
            Keyboard.mJPressed = False
        if (key == pygame.K_k):
            Keyboard.mKPressed = False
        if (key == pygame.K_l):
            Keyboard.mLPressed = False
        if (key == pygame.K_z):
            Keyboard.mZPressed = False
        if (key == pygame.K_x):
            Keyboard.mXPressed = False
        if (key == pygame.K_c):
            Keyboard.mCPressed = False
        if (key == pygame.K_v):
            Keyboard.mVPressed = False
        if (key == pygame.K_b):
            Keyboard.mBPressed = False
        if (key == pygame.K_n):
            Keyboard.mNPressed = False
        if (key == pygame.K_m):
            Keyboard.mMPressed = False

        # If Command Pressed
        if (key == pygame.K_RETURN):
            Keyboard.mEnterPressed = False
        if (key == pygame.K_SPACE):
            Keyboard.mSpacePressed = False
        if (key == pygame.K_ESCAPE):
            Keyboard.mEscapePressed = False

    def update(self):
        # print(Keyboard.inst().cantJoy)

        Keyboard.mLeftPressedPreviousFrame = Keyboard.mLeftPressed
        Keyboard.mRightPressedPreviousFrame = Keyboard.mRightPressed
        Keyboard.mUpPressedPreviousFrame = Keyboard.mUpPressed
        Keyboard.mDownPressedPreviousFrame = Keyboard.mDownPressed

        # Alphabet PressedPreviousFrame
        Keyboard.mQPressedPreviousFrame = Keyboard.mQPressed
        Keyboard.mWPressedPreviousFrame = Keyboard.mWPressed
        Keyboard.mEPressedPreviousFrame = Keyboard.mEPressed
        Keyboard.mRPressedPreviousFrame = Keyboard.mRPressed
        Keyboard.mTPressedPreviousFrame = Keyboard.mTPressed
        Keyboard.mYPressedPreviousFrame = Keyboard.mYPressed
        Keyboard.mUPressedPreviousFrame = Keyboard.mUPressed
        Keyboard.mIPressedPreviousFrame = Keyboard.mIPressed
        Keyboard.mOPressedPreviousFrame = Keyboard.mOPressed
        Keyboard.mPPressedPreviousFrame = Keyboard.mPPressed
        Keyboard.mAPressedPreviousFrame = Keyboard.mAPressed
        Keyboard.mSPressedPreviousFrame = Keyboard.mSPressed
        Keyboard.mDPressedPreviousFrame = Keyboard.mDPressed
        Keyboard.mFPressedPreviousFrame = Keyboard.mFPressed
        Keyboard.mGPressedPreviousFrame = Keyboard.mGPressed
        Keyboard.mHPressedPreviousFrame = Keyboard.mHPressed
        Keyboard.mJPressedPreviousFrame = Keyboard.mJPressed
        Keyboard.mKPressedPreviousFrame = Keyboard.mKPressed
        Keyboard.mLPressedPreviousFrame = Keyboard.mLPressed
        Keyboard.mZPressedPreviousFrame = Keyboard.mZPressed
        Keyboard.mXPressedPreviousFrame = Keyboard.mXPressed
        Keyboard.mCPressedPreviousFrame = Keyboard.mCPressed
        Keyboard.mVPressedPreviousFrame = Keyboard.mVPressed
        Keyboard.mBPressedPreviousFrame = Keyboard.mBPressed
        Keyboard.mNPressedPreviousFrame = Keyboard.mNPressed
        Keyboard.mMPressedPreviousFrame = Keyboard.mMPressed

        # Command Pressesd
        Keyboard.mSpacePressedPreviousFrame = Keyboard.mSpacePressed
        Keyboard.mEnterPressedPreviousFrame = Keyboard.mEnterPressed
        Keyboard.mEscapePressedPreviousFrame = Keyboard.mEscapePressed

        if Keyboard.inst().cantJoy >= 1:
            Keyboard.inst().JoystickPlayer1()
        if Keyboard.inst().cantJoy >= 2:
            Keyboard.inst().JoystickPlayer2()

    def leftPressed(self):
        return Keyboard.mLeftPressed

    def rightPressed(self):
        return Keyboard.mRightPressed

    def upPressed(self):
        return Keyboard.mUpPressed

    def downPressed(self):
        return Keyboard.mDownPressed

    def QPressed(self):
        return Keyboard.mQPressed

    def WPressed(self):
        return Keyboard.mWPressed

    def EPressed(self):
        return Keyboard.mEPressed

    def RPressed(self):
        return Keyboard.mRPressed

    def TPressed(self):
        return Keyboard.mTPressed

    def YPressed(self):
        return Keyboard.mYPressed

    def UPressed(self):
        return Keyboard.mUPressed

    def IPressed(self):
        return Keyboard.mIPressed

    def OPressed(self):
        return Keyboard.mOPressed

    def PPressed(self):
        return Keyboard.mPPressed

    def APressed(self):
        return Keyboard.mAPressed

    def SPressed(self):
        return Keyboard.mSPressed

    def DPressed(self):
        return Keyboard.mDPressed

    def FPressed(self):
        return Keyboard.mFPressed

    def GPressed(self):
        return Keyboard.mGPressed

    def HPressed(self):
        return Keyboard.mHPressed

    def JPressed(self):
        return Keyboard.mJPressed

    def KPressed(self):
        return Keyboard.mKPressed

    def LPressed(self):
        return Keyboard.mLPressed

    def ZPressed(self):
        return Keyboard.mZPressed

    def XPressed(self):
        return Keyboard.mXPressed

    def CPressed(self):
        return Keyboard.mCPressed

    def VPressed(self):
        return Keyboard.mVPressed

    def BPressed(self):
        return Keyboard.mBPressed

    def NPressed(self):
        return Keyboard.mNPressed

    def MPressed(self):
        return Keyboard.mMPressed

    def space(self):
        return Keyboard.mSpacePressed == True and Keyboard.mSpacePressedPreviousFrame == False

    def spaceQ(self):
        return Keyboard.mQPressed == True and Keyboard.mQPressedPreviousFrame == False

    def escape(self):
        return Keyboard.mEscapePressed == True and Keyboard.mEscapePressedPreviousFrame == False

    def previousRight(self):
        return Keyboard.mRightPressed == True and Keyboard.mRightPressedPreviousFrame == False

    def previousLeft(self):
        return Keyboard.mLeftPressed == True and Keyboard.mLeftPressedPreviousFrame == False

    def previousA(self):
        return Keyboard.mAPressed == True and Keyboard.mAPressedPreviousFrame == False

    def previousB(self):
        return Keyboard.mBPressed == True and Keyboard.mBPressedPreviousFrame == False

    def previousW(self):
        return Keyboard.mWPressed == True and Keyboard.mWPressedPreviousFrame == False

    def previousS(self):
        return Keyboard.mSPressed == True and Keyboard.mSPressedPreviousFrame == False

    def previousD(self):
        return Keyboard.mDPressed == True and Keyboard.mDPressedPreviousFrame == False

    def previousL(self):
        return Keyboard.mLPressed == True and Keyboard.mLPressedPreviousFrame == False

    def previousJ(self):
        return Keyboard.mJPressed == True and Keyboard.mJPressedPreviousFrame == False

    def previousI(self):
        return Keyboard.mIPressed == True and Keyboard.mIPressedPreviousFrame == False

    def previousK(self):
        return Keyboard.mKPressed == True and Keyboard.mKPressedPreviousFrame == False

    def previousUp(self):
        return Keyboard.mUpPressed == True and Keyboard.mUpPressedPreviousFrame == False

    def previousDown(self):
        return Keyboard.mDownPressed == True and Keyboard.mDownPressedPreviousFrame == False

    def previousH(self):
        return Keyboard.mHPressed == True and Keyboard.mHPressedPreviousFrame == False

    def previousM(self):
        return Keyboard.mMPressed == True and Keyboard.mMPressedPreviousFrame == False

    def previousF(self):
        return Keyboard.mFPressed == True and Keyboard.mFPressedPreviousFrame == False

    def previousT(self):
        return Keyboard.mTPressed == True and Keyboard.mTPressedPreviousFrame == False

    def previousR(self):
        return Keyboard.mRPressed == True and Keyboard.mRPressedPreviousFrame == False

    def previousG(self):
        return Keyboard.mGPressed == True and Keyboard.mGPressedPreviousFrame == False

    def previousC(self):
        return Keyboard.mCPressed == True and Keyboard.mCPressedPreviousFrame == False

    def previousU(self):
        return Keyboard.mUPressed == True and Keyboard.mUPressedPreviousFrame == False

    def previousV(self):
        return Keyboard.mVPressed == True and Keyboard.mVPressedPreviousFrame == False

    def previousEnter(self):
        return Keyboard.mEnterPressed == True and Keyboard.mEnterPressedPreviousFrame == False

    def previousP(self):
        return Keyboard.mPPressed == True and Keyboard.mPPressedPreviousFrame == False

    def destroy(self):
        Keyboard.mInstance = None

    def JoystickPlayer1(self):
        if Keyboard.inst().UpPressedJoy(1) or Keyboard.joysticks[0].get_hat(0)[1] == 1:
            Keyboard.mWPressed = True
        else:
            Keyboard.mWPressed = False

        if Keyboard.inst().DownPressedJoy(1) or Keyboard.joysticks[0].get_hat(0)[1] == -1:
            Keyboard.mSPressed = True
        else:
            Keyboard.mSPressed = False

        if Keyboard.inst().RightPressedJoy(1) or Keyboard.joysticks[0].get_hat(0)[0] == 1:
            Keyboard.mDPressed = True
        else:
            Keyboard.mDPressed = False

        if Keyboard.inst().LeftPressedJoy(1) or Keyboard.joysticks[0].get_hat(0)[0] == -1:
            Keyboard.mAPressed = True
        else:
            Keyboard.mAPressed = False

        if Keyboard.inst().APressedJoy(1):
            Keyboard.mCPressed = True
        else:
            Keyboard.mCPressed = False

        if Keyboard.inst().XPressedJoy(1):
            Keyboard.mVPressed = True
        else:
            Keyboard.mVPressed = False

        if Keyboard.inst().PauseJoy(1):
            Keyboard.mEscapePressed = True
        else:
            Keyboard.mEscapePressed = False

        if Keyboard.inst().LBPressedJoy(1):
            Keyboard.mTPressed = True
        else:
            Keyboard.mTPressed = False

        if Keyboard.inst().RBPressedJoy(1):
            Keyboard.mRPressed = True
        else:
            Keyboard.mRPressed = False

    def JoystickPlayer2(self):
        if Keyboard.inst().UpPressedJoy(2) or Keyboard.joysticks[1].get_hat(0)[1] == 1:
            Keyboard.mUpPressed = True
        else:
            Keyboard.mUpPressed = False

        if Keyboard.inst().DownPressedJoy(2) or Keyboard.joysticks[1].get_hat(0)[1] == -1:
            Keyboard.mDownPressed = True
        else:
            Keyboard.mDownPressed = False

        if Keyboard.inst().RightPressedJoy(2) or Keyboard.joysticks[1].get_hat(0)[0] == 1:
            Keyboard.mRightPressed = True
        else:
            Keyboard.mRightPressed = False

        if Keyboard.inst().LeftPressedJoy(2) or Keyboard.joysticks[1].get_hat(0)[0] == -1:
            Keyboard.mLeftPressed = True
        else:
            Keyboard.mLeftPressed = False

        if Keyboard.inst().APressedJoy(2):
            Keyboard.mKPressed = True
        else:
            Keyboard.mKPressed = False

        if Keyboard.inst().XPressedJoy(2):
            Keyboard.mLPressed = True
        else:
            Keyboard.mLPressed = False

        if Keyboard.inst().PauseJoy(2):
            Keyboard.mEscapePressed = True
        else:
            Keyboard.mEscapePressed = False

        if Keyboard.inst().LBPressedJoy(2):
            Keyboard.mTPressed = True
        else:
            Keyboard.mTPressed = False

        if Keyboard.inst().RBPressedJoy(2):
            Keyboard.mRPressed = True
        else:
            Keyboard.mRPressed = False

    def UpPressedJoy(self, numberPlayer):
        arriba = False
        if Keyboard.joysticks[numberPlayer - 1].get_axis(1) < -Keyboard.zeroZone:
            arriba = True

        return arriba

    def DownPressedJoy(self, numberPlayer):
        abajo = False
        if Keyboard.joysticks[numberPlayer - 1].get_axis(1) > Keyboard.zeroZone:
            abajo = True
        return abajo

    def RightPressedJoy(self, numberPlayer):
        derecha = False
        if Keyboard.joysticks[numberPlayer - 1].get_axis(0) > Keyboard.zeroZone:
            derecha = True
        return derecha

    def LeftPressedJoy(self, numberPlayer):
        left = False
        if Keyboard.joysticks[numberPlayer - 1].get_axis(0) < -Keyboard.zeroZone:
            left = True
        return left

    def APressedJoy(self, numberPlayer):
        return Keyboard.joysticks[numberPlayer - 1].get_button(0)

    def XPressedJoy(self, numberPlayer):
        return Keyboard.joysticks[numberPlayer - 1].get_button(2)

    def YPressedJoy(self, numberPlayer):
        return Keyboard.joysticks[numberPlayer - 1].get_button(3)

    def BPressedJoy(self, numberPlayer):
        return Keyboard.joysticks[numberPlayer - 1].get_button(1)

    def LBPressedJoy(self, numberPlayer):
        #04: LB
        return Keyboard.joysticks[numberPlayer - 1].get_button(4)
        pass

    def RBPressedJoy(self, numberPlayer):
        #05: RB
        return Keyboard.joysticks[numberPlayer - 1].get_button(5)
        pass

    def PauseJoy(self, numberPlayer):
        return Keyboard.joysticks[numberPlayer - 1].get_button(7)

    def BackJoy(self, numberPlayer):
        return Keyboard.joysticks[numberPlayer - 1].get_button(6)