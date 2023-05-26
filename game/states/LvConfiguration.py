# -*- coding: utf-8 -*-

import pygame
from api.Game import *
from api.GameState import *
from game.GameData import *
from api.AssetManager import *
from api.Keyboard import *
from api.TextSprite import *
from game.states.LvConfiguration import *
from api.AssetAnimatedAction import *
from api.AssetAnimated import *
from game.MousePointer import *
from game.CharacterFactory import *
from game.states.MenuState import *
from game.states.MatchManager import *


class LvConfiguration(GameState):
    def __init__(self):
        from api.Game import Game
        GameState.__init__(self)

        self.game = Game.inst()
        self.mouse = self.game.mMousePointer
        self.Screen = self.game.getScreen()
        self.sc = GameConstants.inst().SCALE
        self.screenWidth = GameConstants.inst().SCREEN_WIDTH
        self.screenHeight = GameConstants.inst().SCREEN_HEIGHT

        self.Stadium = 0

        self.frames = 0
        self.ObjVel = 10

        self.cantPersonajes = GameConstants.inst().CANTIDADPERSONAJES
        self.cantEstadios = GameConstants.inst().CANTIDADESTADIOS

        self.background = AssetManager.inst().ObjSimple("HUD/", "background.png")
        self.game.setBackground(self.background)

        self.ready = True
        self.objects = []

        self.charFrames = []
        self.charFrames.append([])
        self.charFrames.append([])
        self.charFrames.append([])

        self.charMatrix = []
        self.charMatrix.append([])
        self.charMatrix.append([])
        self.charMatrix.append([])
        self.loadCharMatrix()

        self.characters = []
        self.characters.append(0)

        self.P1selectionRow = 0
        self.P1selectionCol = 1
        self.P2selectionRow = 0
        self.P2selectionCol = 2

        self.selectedMode = 1
        self.selectedStadium = 0

        self.LOCKED = False
        self.P1locked = False
        self.P2locked = False
        self.startLocked = True

        ruta = "assets/images/HUD/"

        self.charAnimations = []
        self.charAnimations.append([])
        self.charAnimations.append([])
        self.charAnimations.append([])
        self.charAnimations[1].append(AssetManager.inst().loadAssets(ruta + "charAnimations/", "cross_00_", self.sc))
        self.charAnimations[1].append(AssetManager.inst().loadAssets(ruta + "charAnimations/", "monkey_00_", self.sc))
        self.charAnimations[1].append(AssetManager.inst().loadAssets(ruta + "charAnimations/", "toucan_00_", self.sc))
        self.charAnimations[2].append(AssetManager.inst().loadAssets(ruta + "charAnimations/", "cross_00_", self.sc))
        self.charAnimations[2].append(AssetManager.inst().loadAssets(ruta + "charAnimations/", "monkey_00_", self.sc, True))
        self.charAnimations[2].append(AssetManager.inst().loadAssets(ruta + "charAnimations/", "toucan_00_", self.sc, True))

        self.charSheet = []
        self.charSheet.append([])
        self.charSheet.append([])
        self.charSheet.append([])
        self.charSheet[0].append(0)
        self.charSheet[0].append(0)
        self.charSheet[0].append("")
        self.charSheet[1].append(5)
        self.charSheet[1].append(5)
        self.charSheet[1].append("Power: Spirit Ball")
        self.charSheet[2].append(2)
        self.charSheet[2].append(10)
        self.charSheet[2].append("Power: Twist")

        self.stadiumsBG = AssetManager.inst().loadAssets(ruta, "stadiumBG", self.sc)
        self.background = Sprite()
        self.background.setImage(self.stadiumsBG[self.selectedStadium])
        self.background.setXY(self.screenWidth/2, self.screenHeight/2)
        self.objects.append(self.background)

        # CHARACTER GRID
        framesTop = self.screenHeight * 0.30
        framesLeft = self.screenWidth * 0.40
        fila = 0
        while fila < 3:
            columna = 0
            while columna < 3:
                frameCharTmp = Sprite()
                frameCharTmp.setImage(AssetManager.inst().ObjSimple("HUD/", "frameChar.png"))
                frameCharTmp.setXY(framesLeft + frameCharTmp.getWidth() * 1.115 * columna, framesTop + frameCharTmp.getHeight() * 1.115 * fila)
                self.objects.append(frameCharTmp)
                self.charFrames[fila].append(frameCharTmp)
                columna += 1
            fila += 1

        fila = 0
        while fila < 3:
            columna = 0
            while columna < 3:
                avatarTmp = Sprite()
                if self.charMatrix[fila][columna] != 0:
                    avatarTmp = AssetAnimated(AssetManager.inst().Avatars[0][self.charMatrix[fila][columna]], True, 20)
                    self.characters.append(CharacterFactory().inst().createCharacter(self.charMatrix[fila][columna], 1))
                else:
                    avatarTmp = AssetAnimated(AssetManager.inst().Avatars[0][0], True, 20)
                avatarTmp.setXY(self.charFrames[fila][columna].getX(), self.charFrames[fila][columna].getY())
                self.objects.append(avatarTmp)
                columna += 1
            fila += 1

        self.selectP1types = []
        self.selectP1types.append(AssetManager.inst().loadAssets(ruta, "selectBlue_00_", self.sc))
        self.selectP1types.append(AssetManager.inst().loadAssets(ruta, "selectBlue_01_", self.sc))
        self.selectP1 = AssetAnimated(self.selectP1types[0], True, 5)

        self.selectP2types = []
        self.selectP2types.append(AssetManager.inst().loadAssets(ruta, "selectRed_00_", self.sc))
        self.selectP2types.append(AssetManager.inst().loadAssets(ruta, "selectRed_01_", self.sc))
        self.selectP2 = AssetAnimated(self.selectP2types[0], True, 5)

        self.keys = []
        self.keys.append(AssetManager.inst().loadAssets(ruta + "keys/", "keysJoyselec_", self.sc))
        self.keys.append(AssetManager.inst().loadAssets(ruta + "keys/", "keysP1selec_", self.sc))
        self.keys.append(AssetManager.inst().loadAssets(ruta + "keys/", "keysP2selec_", self.sc))

        self.keysP1 = AssetAnimated(self.keys[1], True, 20)
        self.keysP2 = AssetAnimated(self.keys[2], True, 20)

        if Keyboard.inst().cantJoy >= 1:
            self.keysP1.initAnimation(self.keys[0], 0, -1, 20, True)
        if Keyboard.inst().cantJoy >= 2:
            self.keysP2.initAnimation(self.keys[0], 0, -1, 20, True)

        self.keysP1.setXY(self.screenWidth * 0.15, self.screenHeight * 0.715)
        self.keysP2.setXY(self.screenWidth * 0.85, self.keysP1.getY())

        self.veil = AssetAnimated(AssetManager.inst().loadAssetsSized(ruta + "veil/", "veil_", 1920, 1080), False, 5)
        self.veil.setXY(self.screenWidth / 2, self.screenHeight / 2)

        self.objects.append(self.selectP1)
        self.objects.append(self.selectP2)
        self.objects.append(self.keysP1)
        self.objects.append(self.keysP2)
        self.objects.append(self.veil)

        # BARRA SUPERIOR
        self.frameTop = Sprite()
        self.frameTop.setRegistration(self.frameTop.TOP_LEFT)
        self.frameTop.setImage(AssetManager.inst().ObjSimple("HUD/", "frameTop.png"))
        self.frameTop.setXY(0, 0 - self.frameTop.getHeight())

        self.modesArray = AssetManager.inst().loadAssets(ruta, "mode_", self.sc)
        self.mode = Sprite()
        self.mode.setImage(self.modesArray[self.selectedMode])

        self.rightArrows = AssetManager.inst().loadAssets(ruta, "horArrowRight", self.sc)
        self.modeArrowRight = Sprite()
        self.modeArrowRight.setImage(self.rightArrows[0])

        self.leftArrows = AssetManager.inst().loadAssets(ruta, "horArrowLeft", self.sc)
        self.modeArrowLeft = Sprite()
        self.modeArrowLeft.setImage(self.leftArrows[0])

        self.objects.append(self.frameTop)
        self.objects.append(self.mode)
        self.objects.append(self.modeArrowLeft)
        self.objects.append(self.modeArrowRight)

        # BARRA INFERIOR
        self.frameBot = Sprite()
        self.frameBot.setRegistration(self.frameBot.TOP_LEFT)
        self.frameBot.setImage(AssetManager.inst().ObjSimple("HUD/", "frameBot.png"))
        self.frameBot.setXY(0, self.screenHeight)

        self.stadiums = []
        self.stadiums.append(AssetManager.inst().loadAssets(ruta, "stadiumLogo_00_", self.sc))
        self.stadiumLogo = AssetAnimated(self.stadiums[0], True, 2)

        self.stadiumsNameArray = AssetManager.inst().loadAssets(ruta, "stadiumName_", self.sc)
        self.stadiumName = Sprite()
        self.stadiumName.setImage(self.stadiumsNameArray[0])

        self.backButton = AssetManager.inst().loadAssets(ruta, "back_button", self.sc)
        self.back = Sprite()
        self.back.setImage(self.backButton[0])

        self.startStates = []
        self.startStates.append(AssetManager.inst().loadAssets(ruta, "start_button_00_", self.sc))
        self.startStates.append(AssetManager.inst().loadAssets(ruta, "start_button_01_", self.sc))
        self.startStates.append(AssetManager.inst().loadAssets(ruta, "start_button_02_", self.sc))
        self.start = AssetAnimated(self.startStates[2], True, 2)

        self.stadiumArrowUp = Sprite()
        self.stadiumArrowUp.setImage(AssetManager.inst().ObjSimple("HUD/", "verArrowUp.png"))

        self.stadiumArrowDown = Sprite()
        self.stadiumArrowDown.setImage(AssetManager.inst().ObjSimple("HUD/", "verArrowDown.png"))

        self.objects.append(self.frameBot)
        self.objects.append(self.stadiumName)
        self.objects.append(self.stadiumLogo)
        self.objects.append(self.back)
        self.objects.append(self.start)
        # self.objects.append(self.stadiumArrowUp)
        # self.objects.append(self.stadiumArrowDown)

        # CHARACTER SHEETS
        self.charP1 = Sprite()
        self.charP1.setImage(AssetManager.inst().ObjSimple("HUD/", "charSheet.png"))
        self.charP1.setXY(0 - self.charP1.getWidth() / 2, self.screenHeight * 0.49)

        self.charP1_Name = Sprite()
        self.charP1_Name.setImage(AssetManager.inst().ObjSimple("HUD/", "charName.png"))
        self.charP1_animationFrame = Sprite()
        self.charP1_animationFrame.setImage(AssetManager.inst().ObjSimple("HUD/", "charP1_animationFrame.png"))
        self.charP1_animated = AssetAnimated(self.charAnimations[1][self.charMatrix[self.P1selectionRow][self.P1selectionCol]], True, 5)

        self.textMightP1 = TextSprite("Might", int(100 * self.sc), "assets/fonts/m3x6.ttf", (255, 255, 255))
        self.textSpeedP1 = TextSprite("Speed", int(100 * self.sc), "assets/fonts/m3x6.ttf", (255, 255, 255))
        self.textPowerP1 = TextSprite("", int(100 * self.sc), "assets/fonts/m3x6.ttf", (255, 255, 255))
        self.textPowerP1.setRegistration(self.textPowerP1.TOP_LEFT)
        self.textPowerP1.setText(self.charSheet[self.charMatrix[self.P1selectionRow][self.P1selectionCol]][2])
        self.textPowerP1.updateImageTxt()

        self.charP1_MightBar = Sprite()
        self.charP1_MightBar.setImage(AssetManager.inst().ObjSimple("HUD/", "charP1_bar.png"))
        self.charP1_SpeedBar = Sprite()
        self.charP1_SpeedBar.setImage(AssetManager.inst().ObjSimple("HUD/", "charP1_bar.png"))

        self.charP1_MightBarPoints = []
        self.charP1_SpeedBarPoints = []
        i = 1
        while i <= 10:
            mightbar = Sprite()
            mightbar.setImage(AssetManager.inst().ObjSimple("HUD/", "energybar_0_00.png"))
            self.charP1_MightBarPoints.append(mightbar)
            speedbar = Sprite()
            speedbar.setImage(AssetManager.inst().ObjSimple("HUD/", "energybar_0_00.png"))
            self.charP1_SpeedBarPoints.append(speedbar)
            i += 1

        self.objects.append(self.charP1)
        self.objects.append(self.charP1_Name)
        self.objects.append(self.charP1_animationFrame)
        self.objects.append(self.charP1_animated)
        self.objects.append(self.textMightP1)
        self.objects.append(self.textSpeedP1)
        self.objects.append(self.textPowerP1)
        self.objects.append(self.charP1_MightBar)
        self.objects.append(self.charP1_SpeedBar)

        self.charP2 = Sprite()
        self.charP2.setImage(AssetManager.inst().ObjSimple("HUD/", "charSheet.png"))
        self.charP2.setXY(self.screenWidth + self.charP2.getWidth() / 2, self.screenHeight * 0.49)

        self.charP2_Name = Sprite()
        self.charP2_Name.setImage(AssetManager.inst().ObjSimple("HUD/", "charName.png"))
        self.charP2_animationFrame = Sprite()
        self.charP2_animationFrame.setImage(AssetManager.inst().ObjSimple("HUD/", "charP2_animationFrame.png"))
        self.charP2_animated = AssetAnimated(self.charAnimations[2][self.charMatrix[self.P2selectionRow][self.P2selectionCol]], True, 5)

        self.textMightP2 = TextSprite("Might", int(100 * self.sc), "assets/fonts/m3x6.ttf", (255, 255, 255))
        self.textSpeedP2 = TextSprite("Speed", int(100 * self.sc), "assets/fonts/m3x6.ttf", (255, 255, 255))
        self.textPowerP2 = TextSprite("", int(100 * self.sc), "assets/fonts/m3x6.ttf", (255, 255, 255))
        self.textPowerP2.setRegistration(self.textPowerP2.TOP_LEFT)
        self.textPowerP2.setText(self.charSheet[self.charMatrix[self.P2selectionRow][self.P2selectionCol]][2])
        self.textPowerP2.updateImageTxt()

        self.charP2_MightBar = Sprite()
        self.charP2_MightBar.setImage(AssetManager.inst().ObjSimple("HUD/", "charP2_bar.png"))
        self.charP2_SpeedBar = Sprite()
        self.charP2_SpeedBar.setImage(AssetManager.inst().ObjSimple("HUD/", "charP2_bar.png"))

        self.charP2_MightBarPoints = []
        self.charP2_SpeedBarPoints = []
        i = 1
        while i <= 10:
            mightbar = Sprite()
            mightbar.setImage(AssetManager.inst().ObjSimple("HUD/", "energybar_0_00.png"))
            self.charP2_MightBarPoints.append(mightbar)
            speedbar = Sprite()
            speedbar.setImage(AssetManager.inst().ObjSimple("HUD/", "energybar_0_00.png"))
            self.charP2_SpeedBarPoints.append(speedbar)
            i += 1

        self.objects.append(self.charP2)
        self.objects.append(self.charP2_Name)
        self.objects.append(self.charP2_animationFrame)
        self.objects.append(self.charP2_animated)
        self.objects.append(self.textMightP2)
        self.objects.append(self.textSpeedP2)
        self.objects.append(self.textPowerP2)
        self.objects.append(self.charP2_MightBar)
        self.objects.append(self.charP2_SpeedBar)

        self.mouse.mostrarMouse = True

    def update(self):
        GameState.update(self)
        self.ready = True

        if Keyboard.inst().escape():
            self.game.setState(MenuState())

        i = 0
        while i < len(self.objects):
            self.objects[i].update()
            i += 1

        if self.veil.isEnded():
            self.veil.setVisible(False)

        # (PosObjetivo - PosActual) / 12
        if self.frameTop.getY() < 0:
            self.frameTop.setVelY((0 - self.frameTop.getY())/12+1)
            self.placeTopFrameObjects()
            self.ready = False
        elif self.frameTop.getY() > 0:
            self.frameTop.setY(0)
            self.frameTop.setVelY(0)
            self.placeTopFrameObjects()

        if self.frameBot.getY() > self.screenHeight - self.frameBot.getHeight():
            self.frameBot.setVelY((self.screenHeight - self.frameBot.getHeight() - self.frameBot.getY())/12)
            self.placeBotFrameObjects()
            self.ready = False
        elif self.frameBot.getY() < self.screenHeight - self.frameBot.getHeight():
            self.frameBot.setY(self.screenHeight - self.frameBot.getHeight())
            self.frameBot.setVelY(0)
            self.placeBotFrameObjects()

        if self.charP1.getX() < self.screenWidth * 0.18:
            self.charP1.setVelX((self.screenWidth * 0.18 - self.charP1.getX())/12)
            self.placeCharFrameObjects()
            self.ready = False
        elif self.charP1.getX() > self.screenWidth * 0.18:
            self.charP1.setX(self.screenWidth * 0.18)
            self.charP1.setVelX(0)
            self.placeCharFrameObjects()

        if self.charP2.getX() > self.screenWidth * 0.82:
            self.charP2.setVelX((self.screenWidth * 0.82 - self.charP2.getX())/12)
            self.ready = False
        elif self.charP2.getX() < self.screenWidth * 0.82:
            self.charP2.setX(self.screenWidth * 0.82)
            self.charP2.setVelX(0)

        if self.selectedMode == 0:
            self.moveKey(1)
            self.moveKey(2)
        elif self.selectedMode == 1:
            if not self.P1locked:
                self.moveKey(1)
            else:
                self.moveKey(2)

        self.placeSelectors()

        if self.P1locked and self.P2locked:
            if self.start.collides(self.mouse.getPunta()) and self.mouse.getState() == self.mouse.CLICKED:
                self.start.initAnimation(self.startStates[1], 0, len(self.startStates[1]) - 1, 10, True)
                if self.mouse.isEnded():
                    AudioManager.inst().playConfirmOption()
                    self.startMatch()
            elif Keyboard.inst().previousEnter():
                self.startMatch()

        elif self.back.collides(self.mouse.getPunta()) and self.mouse.getState() == self.mouse.CLICKED:
            self.back.setImage(self.backButton[1])
            if self.mouse.isEnded():
                from api.Game import Game
                AudioManager.inst().playConfirmOption()
                self.game.setState(MenuState())

        elif (self.modeArrowRight.collides(self.mouse.getPunta()) and self.mouse.getState() == self.mouse.CLICKED):
            self.modeArrowRight.setImage(self.rightArrows[1])
            AudioManager.inst().playConfirmOption()
            if self.mouse.isEnded():
                self.selectedMode += 1
                if self.selectedMode > len(self.modesArray)-1:
                    self.selectedMode = 0
                self.mode.setImage(self.modesArray[self.selectedMode])
                self.modeArrowRight.setImage(self.rightArrows[0])

        elif (self.modeArrowLeft.collides(self.mouse.getPunta()) and self.mouse.getState() == self.mouse.CLICKED):
            self.modeArrowLeft.setImage(self.leftArrows[1])
            AudioManager.inst().playConfirmOption()
            if self.mouse.isEnded():
                self.selectedMode -= 1
                if self.selectedMode < 0:
                    self.selectedMode = len(self.modesArray)-1
                self.mode.setImage(self.modesArray[self.selectedMode])
                self.modeArrowLeft.setImage(self.leftArrows[0])

        elif Keyboard.inst().cantJoy > 0:
            if Keyboard.inst().previousT():
                self.selectedMode += 1
                AudioManager.inst().playConfirmOption()
                if self.selectedMode > len(self.modesArray) - 1:
                    self.selectedMode = 0
                self.mode.setImage(self.modesArray[self.selectedMode])
                self.modeArrowRight.setImage(self.rightArrows[0])

            if Keyboard.inst().previousR():
                self.selectedMode += 1
                AudioManager.inst().playConfirmOption()
                if self.selectedMode > len(self.modesArray) - 1:
                    self.selectedMode = 0
                self.mode.setImage(self.modesArray[self.selectedMode])
                self.modeArrowRight.setImage(self.rightArrows[0])

            # if Keyboard.inst().previousV() or Keyboard.inst().previousL():
            #     from api.Game import Game
            #     AudioManager.inst().playConfirmOption()
            #     self.game.setState(MenuState())


        if self.selectedMode == 0:
            self.selectP1.setVisible(True)
            self.selectP2.setVisible(True)
            self.keysP2.setVisible(True)
        elif self.selectedMode == 1:
            self.selectP2.setVisible(False)
            self.keysP2.setVisible(False)
            if self.P1locked:
                self.selectP2.setVisible(True)

    def startMatch(self):
        from api.Game import Game
        from game.states.MatchManager import MatchManager
        p1 = self.charMatrix[self.P1selectionRow][self.P1selectionCol]
        p2 = self.charMatrix[self.P2selectionRow][self.P2selectionCol]

        if self.selectedMode == 1:
            p2 *= -1

        self.game.setState(MatchManager.inst())
        MatchManager.inst().startMatch(p1, p2, self.Stadium, True)

    def render(self):
        GameState.render(self)

        i = 0
        while i < len(self.objects):
            self.objects[i].render(self.Screen)
            i += 1

        self.renderStats()
        self.drawScreenText()

    def getCharacter(self, aType): #esto para cambiar de player
        array = AssetManager.Characters[aType][1][0][0]
        asset = AssetAnimated(array, True, 2)
        return asset

    def getStadium(self, aType):
        asset = AssetAnimated(AssetManager.Stadiums[aType], False, 2)
        return asset

    def destroy(self):
        GameState.destroy(self)

    def loadCharMatrix(self):
        self.charMatrix[0].append(0)
        self.charMatrix[0].append(1)
        self.charMatrix[0].append(2)
        self.charMatrix[1].append(0)
        self.charMatrix[1].append(0)
        self.charMatrix[1].append(0)
        self.charMatrix[2].append(0)
        self.charMatrix[2].append(0)
        self.charMatrix[2].append(0)

    def drawText(self, aX, aY, aMsg, aSize, aColor=(0, 0, 0)):
        texto = TextSprite(aMsg, aSize, "assets/fonts/m3x6.ttf", aColor)
        texto.setXY(aX, aY)
        texto.render(self.Screen)
        return texto

    def placeTopFrameObjects(self):
        self.mode.setXY(self.screenWidth / 2, self.frameTop.getY() + self.frameTop.getHeight() * 0.47)
        self.modeArrowRight.setXY(self.mode.getX() + int(self.mode.getWidth() * 0.60), self.mode.getY())
        self.modeArrowLeft.setXY(self.mode.getX() - int(self.mode.getWidth() * 0.598), self.mode.getY())

    def placeBotFrameObjects(self):
        self.stadiumLogo.setXY(self.screenWidth / 2, self.frameBot.getY() + self.frameBot.getHeight() * 0.55)
        self.stadiumName.setXY(self.screenWidth / 2 - self.stadiumLogo.getWidth() / 2 - self.stadiumName.getWidth() / 2, self.stadiumLogo.getY())
        self.back.setXY(self.screenWidth * 0.10, self.stadiumLogo.getY())
        self.start.setXY(self.screenWidth * 0.90, self.stadiumLogo.getY())
        self.stadiumArrowUp.setXY(self.stadiumLogo.getX() * 1.12, self.stadiumLogo.getY() * 0.97)
        self.stadiumArrowDown.setXY(self.stadiumLogo.getX() * 1.12, self.stadiumLogo.getY() * 1.03)

    def placeCharFrameObjects(self):
        self.charP1_Name.setXY(self.charP1.getX() - self.charP1.getWidth()*0.20, self.charP1.getY() - self.charP1.getHeight()/2 - self.charP1_Name.getHeight()/2)
        self.charP1_animationFrame.setXY(self.charP1.getX() + self.charP1.getWidth() * 0.32, self.charP1.getY() - self.charP1.getHeight() * 0.12)
        self.charP1_animated.setXY(self.charP1_animationFrame.getX(), self.charP1_animationFrame.getY())

        posX = self.charP1.getX() - self.charP1.getWidth()/2
        posY = self.charP1.getY() - self.charP1.getHeight()/2
        self.textMightP1.setXY(posX + self.charP1.getWidth() * 0.16, posY + self.charP1.getHeight() * 0.205)
        self.textSpeedP1.setXY(posX + self.charP1.getWidth() * 0.16, posY + self.charP1.getHeight() * 0.495)
        self.textPowerP1.setXY(posX + self.charP1.getWidth() * 0.065, posY + self.charP1.getHeight() * 0.65)

        self.charP1_MightBar.setXY(posX + self.charP1.getWidth() * 0.44, self.textMightP1.getY() * 1.022)
        self.charP1_SpeedBar.setXY(posX + self.charP1.getWidth() * 0.44, self.textSpeedP1.getY() * 1.022)

        self.charP2_Name.setXY(self.charP2.getX() + self.charP2.getWidth()*0.20, self.charP2.getY() - self.charP2.getHeight()/2 - self.charP2_Name.getHeight()/2)
        self.charP2_animationFrame.setXY(self.charP2.getX() - self.charP2.getWidth() * 0.32, self.charP2.getY() - self.charP2.getHeight() * 0.12)
        self.charP2_animated.setXY(self.charP2_animationFrame.getX(), self.charP2_animationFrame.getY())

        posX = self.charP2.getX() - self.charP2.getWidth() / 2
        posY = self.charP2.getY() - self.charP2.getHeight() / 2
        self.textMightP2.setXY(posX + self.charP2.getWidth() * 0.46, posY + self.charP2.getHeight() * 0.205)
        self.textSpeedP2.setXY(posX + self.charP2.getWidth() * 0.46, posY + self.charP2.getHeight() * 0.495)
        self.textPowerP2.setXY(posX + self.charP2.getWidth() * 0.065, posY + self.charP2.getHeight() * 0.65)

        self.charP2_MightBar.setXY(posX + self.charP2.getWidth() * 0.74, self.textMightP2.getY() * 1.022)
        self.charP2_SpeedBar.setXY(posX + self.charP2.getWidth() * 0.74, self.textSpeedP2.getY() * 1.022)

        self.placeBarPoints()

    def placeBarPoints(self):
        mightPosXp1 = self.charP1_MightBar.getX() - self.charP1_MightBar.getWidth() / 2 + self.charP1_MightBar.getWidth() * 0.085 + self.charP1_MightBarPoints[0].getWidth()/2+1
        i = 0
        while i < 10:
            self.charP1_MightBarPoints[i].setXY(mightPosXp1 + (self.charP1_MightBarPoints[i].getWidth() + 4 * self.sc) * i, self.charP1_MightBar.getY())
            self.charP1_SpeedBarPoints[i].setXY(mightPosXp1 + (self.charP1_SpeedBarPoints[i].getWidth() + 4 * self.sc) * i, self.charP1_SpeedBar.getY())
            i += 1

        mightPosXp2 = self.charP2_MightBar.getX() - self.charP2_MightBar.getWidth() / 2 + self.charP2_MightBar.getWidth() * 0.085 + self.charP2_MightBarPoints[0].getWidth() / 2 + 1
        i = 0
        while i < 10:
            self.charP2_MightBarPoints[i].setXY(mightPosXp2 + (self.charP2_MightBarPoints[i].getWidth() + 4 * self.sc) * i, self.charP2_MightBar.getY())
            self.charP2_SpeedBarPoints[i].setXY(mightPosXp2 + (self.charP2_SpeedBarPoints[i].getWidth() + 4 * self.sc) * i, self.charP2_SpeedBar.getY())
            i += 1

    def placeSelectors(self):
        charFrameP1 = self.charFrames[self.P1selectionRow][self.P1selectionCol]
        charFrameP2 = self.charFrames[self.P2selectionRow][self.P2selectionCol]
        self.selectP1.setXY(charFrameP1.getX(), charFrameP1.getY())
        self.selectP2.setXY(charFrameP2.getX(), charFrameP2.getY())

    def drawScreenText(self):
        if self.charMatrix[self.P1selectionRow][self.P1selectionCol] != 0:
            name = self.characters[self.charMatrix[self.P1selectionRow][self.P1selectionCol]].Name
            self.drawText(self.charP1_Name.getX(), self.charP1_Name.getY()*1.00, name, int(120 * self.sc), (255, 255, 255))

        if self.charMatrix[self.P2selectionRow][self.P2selectionCol] != 0:
            name = self.characters[self.charMatrix[self.P2selectionRow][self.P2selectionCol]].Name
            self.drawText(self.charP2_Name.getX(), self.charP2_Name.getY()*1.00, name, int(120 * self.sc), (255, 255, 255))

        self.textPowerP1.setText(self.charSheet[self.charMatrix[self.P1selectionRow][self.P1selectionCol]][2])
        self.textPowerP1.updateImageTxt()
        self.textPowerP2.setText(self.charSheet[self.charMatrix[self.P2selectionRow][self.P2selectionCol]][2])
        self.textPowerP2.updateImageTxt()

    def renderStats(self):
        i = 0
        while i < self.charSheet[self.charMatrix[self.P1selectionRow][self.P1selectionCol]][0]:
            self.charP1_MightBarPoints[i].render(self.Screen)
            i += 1
        i = 0
        while i < self.charSheet[self.charMatrix[self.P1selectionRow][self.P1selectionCol]][1]:
            self.charP1_SpeedBarPoints[i].render(self.Screen)
            i += 1
        i = 0
        while i < self.charSheet[self.charMatrix[self.P2selectionRow][self.P2selectionCol]][0]:
            self.charP2_MightBarPoints[i].render(self.Screen)
            i += 1
        i = 0
        while i < self.charSheet[self.charMatrix[self.P2selectionRow][self.P2selectionCol]][1]:
            self.charP2_SpeedBarPoints[i].render(self.Screen)
            i += 1

    def moveKey(self, playerNumber):
        self.defineKeys(playerNumber)

        if not self.LOCKED:
            if playerNumber == 1:
                row = self.P1selectionRow
                col = self.P1selectionCol
            elif playerNumber == 2:
                row = self.P2selectionRow
                col = self.P2selectionCol

            if self.Move_UP:
                AudioManager.inst().playMoveOption()
                if row == 0:
                    row = 2
                else:
                    row -= 1
            elif self.Move_DOWN:
                AudioManager.inst().playMoveOption()
                if row == 2:
                    row = 0
                else:
                    row += 1
            elif self.Move_LEFT:
                AudioManager.inst().playMoveOption()
                if col == 0:
                    col = 2
                else:
                    col -= 1
            elif self.Move_RIGHT:
                AudioManager.inst().playMoveOption()
                if col == 2:
                    col = 0
                else:
                    col += 1

            if playerNumber == 1:
                self.P1selectionRow = row
                self.P1selectionCol = col
            elif playerNumber == 2:
                self.P2selectionRow = row
                self.P2selectionCol = col

            if self.Move_UP or self.Move_DOWN or self.Move_LEFT or self.Move_RIGHT:
                if playerNumber == 1:
                    anim = self.charAnimations[1][self.charMatrix[self.P1selectionRow][self.P1selectionCol]]
                    self.charP1_animated.initAnimation(anim, 0, len(anim) - 1, 5, True)
                elif playerNumber == 2:
                    anim = self.charAnimations[2][self.charMatrix[self.P2selectionRow][self.P2selectionCol]]
                    self.charP2_animated.initAnimation(anim, 0, len(anim) - 1, 5, True)

        if self.P1locked and self.P2locked:
            if self.A:
                self.startMatch()

        if self.A:
            if playerNumber == 1 and self.charMatrix[self.P1selectionRow][self.P1selectionCol] != 0:
                self.P1locked = True
                AudioManager.inst().playConfirmCharacter()
                self.selectP1.initAnimation(self.selectP1types[1], 0, len(self.selectP1types[1]) - 1, 10, True)
            elif playerNumber == 2 and self.charMatrix[self.P2selectionRow][self.P2selectionCol] != 0:
                self.P2locked = True
                AudioManager.inst().playConfirmCharacter()
                self.selectP2.initAnimation(self.selectP2types[1], 0, len(self.selectP2types[1]) - 1, 10, True)
            if self.P1locked and self.P2locked:
                self.start.initAnimation(self.startStates[0], 0, len(self.startStates[0]) - 1, 10, True)
        if self.B:
            if playerNumber == 1:
                if not self.P1locked:
                    self.game.setState(MenuState())
                else:
                    self.P1locked = False
                    self.selectP1.initAnimation(self.selectP1types[0], 0, len(self.selectP1types[0]) - 1, 10, True)
            elif playerNumber == 2:
                if self.selectedMode == 0:
                    self.P2locked = False
                    self.selectP2.initAnimation(self.selectP2types[0], 0, len(self.selectP2types[0]) - 1, 10, True)
                if self.selectedMode == 1:
                    if self.P2locked:
                        self.P2locked = False
                        self.selectP2.initAnimation(self.selectP2types[0], 0, len(self.selectP2types[0]) - 1, 10, True)
                    elif not self.P2locked:
                        self.P1locked = False
                        self.selectP1.initAnimation(self.selectP1types[0], 0, len(self.selectP1types[0]) - 1, 10, True)
            if not self.P1locked or not self.P2locked:
                self.start.initAnimation(self.startStates[2], 0, len(self.startStates[2]) - 1, 10, True)

    def defineKeys(self, playerNumber):
        if playerNumber == 1:
            self.Move_UP = Keyboard.inst().previousW()
            self.Move_DOWN = Keyboard.inst().previousS()
            self.Move_LEFT = Keyboard.inst().previousA()
            self.Move_RIGHT = Keyboard.inst().previousD()
            self.A = Keyboard.inst().previousC()
            self.B = Keyboard.inst().previousV()
            self.LOCKED = self.P1locked
        elif playerNumber == 2:
            if self.selectedMode == 0:
                self.Move_UP = Keyboard.inst().previousUp()
                self.Move_DOWN = Keyboard.inst().previousDown()
                self.Move_LEFT = Keyboard.inst().previousLeft()
                self.Move_RIGHT = Keyboard.inst().previousRight()
                self.A = Keyboard.inst().previousK()
                self.B = Keyboard.inst().previousL()
                self.LOCKED = self.P2locked
            elif self.selectedMode == 1:
                self.Move_UP = Keyboard.inst().previousW()
                self.Move_DOWN = Keyboard.inst().previousS()
                self.Move_LEFT = Keyboard.inst().previousA()
                self.Move_RIGHT = Keyboard.inst().previousD()
                self.A = Keyboard.inst().previousC()
                self.B = Keyboard.inst().previousV()
                self.LOCKED = self.P2locked
