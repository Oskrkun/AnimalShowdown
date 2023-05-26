# -*- coding: utf-8 -*-

import pygame
from game.CharacterFactory import *
from game.Disk.Disk import *
from game.states.Stadiums.BeachStadium import *
from api.GameState import *
from api.Game import *
from game.states.Stadiums.BeachStadium import *
from game.Settings import *
import math


class MatchManager(GameState):
    mInstance = None
    mInitialized = False

    Player1 = None
    Player2 = None
    Disk = None
    Stadium = None

    Scores = []
    Goal = False
    GoalFrames = []
    GoalPlayer = 0

    TimerMin = 1
    TimerSec = 30
    TimeFrames = 0

    Intro = False
    IntroFrames = 180
    matchIntroVeil = None

    Started = False
    StartFrames = 60

    Finished = False

    Objects = []
    Players = []

    Paused = False
    mIsMuted = False

    mTextPause = None

    def __new__(self, *args, **kargs):
        if (MatchManager.mInstance is None):
            MatchManager.mInstance = object.__new__(self, *args, **kargs)
            self.init(MatchManager.mInstance)
        return self.mInstance

    @classmethod
    def inst(cls):
        if (not cls.mInstance):
            return cls()
        return cls.mInstance

    def __init__(self):
        GameState.__init__(self)
        init()

    def init(self):
        from api.Game import Game
        self.screenWidth = GameConstants.inst().SCREEN_WIDTH
        self.screenHeight = GameConstants.inst().SCREEN_HEIGHT
        self.sc = GameConstants.inst().SCALE

        self.Screen = Game.inst().getScreen()
        self.FPS = Game.inst().FPS

        self.settings = Settings.inst()

        self.Players.append(self.Player1)
        self.Players.append(self.Player2)

        self.Scores.append(0)
        self.Scores.append(0)
        self.Scores.append(0)

        self.StartPlayer = Math.randNumberBetween(1, 2)

        self.mIsMuted = True
        self.mIsPaused = False

        self.mTextPause = TextSprite("PAUSA", 180, "assets/fonts/m3x6.ttf", (0, 0, 0))
        self.mTextPause.setXY(GameConstants.inst().SCREEN_WIDTH/2, GameConstants.inst().SCREEN_HEIGHT/2)

        self.BG_Veil = Sprite()
        self.BG_Veil.setImage(AssetManager.inst().ObjSimple("HUD/", "BG_Veil.png"))
        self.BG_Veil.setXY(self.screenWidth/2, self.screenHeight/2)

        self.pauseScreen = Sprite()
        self.pauseScreen.setImage(AssetManager.inst().ObjSimple("HUD/keys/", "pauseScreen_00.png"))
        self.pauseScreen.setXY(self.screenWidth / 2, self.screenHeight / 2)

        self.keys = []
        self.keys.append(AssetManager.inst().loadAssets("assets/images/HUD/keys/", "keysJoy_", self.sc))
        self.keys.append(AssetManager.inst().loadAssets("assets/images/HUD/keys/", "keysP1_", self.sc))
        self.keys.append(AssetManager.inst().loadAssets("assets/images/HUD/keys/", "keysP2_", self.sc))

        self.keysP1 = AssetAnimated(self.keys[1], True, 5)
        self.keysP2 = AssetAnimated(self.keys[2], True, 5)

        if Keyboard.inst().cantJoy >= 1:
            self.keysP1.initAnimation(self.keys[0], 0, -1, 20, True)
        if Keyboard.inst().cantJoy == 2:
            self.keysP2.initAnimation(self.keys[0], 0, -1, 20, True)

        self.keysP1.setXY(self.screenWidth * 0.25, self.screenHeight * 0.75)
        self.keysP2.setXY(self.screenWidth * 0.75, self.keysP1.getY())

        self.goalConf()

        self.mouse = Game.inst().mMousePointer

    def togglePause(self):
        self.Paused = not self.Paused
        self.mouse.mostrarMouse = self.Paused

    def toggleMuteSounds(self):
        self.mIsMuted = not self.mIsMuted

        if self.mIsMuted:
            AudioManager.inst().mute()
        else:
            AudioManager.inst().playStart()

    def update(self):
        if not self.Finished:
            if Keyboard.inst().escape():
                self.togglePause()
                self.settings.visible = False
        elif self.Finished:
            self.mouse.mostrarMouse = True

        self.mTextPause.update()

        # Cuando el juego esta en pausa no se corre update().
        if not self.Paused:
            if self.Started:
                if not self.Finished:
                    self.Disk.setVisible(True)
                    self.timePass()
                    for e in self.Objects:
                        e.update()
                    self.Disk.update()
                    self.Player1.update()
                    self.Player2.update()
                    self.Stadium.update()
                    self.checkGoal()
                else:
                    self.updateMatchMenu()
            else:
                self.Disk.setVisible(False)
                if self.Intro:
                    self.runIntro()
                else:
                    self.Player1.update()
                    self.Player2.update()
                    self.Stadium.update()
                    self.Coin.update()
                    if self.Coin.isEnded():
                        if self.StartPlayer == 1:
                            self.Coin.gotoAndStop(0)
                        elif self.StartPlayer == 2:
                            self.Coin.gotoAndStop(6)
                        self.StartFrames -= 1
                        if self.StartFrames == 0:
                            self.Started = True
                            if self.StartPlayer == 1:
                                self.Disk.setHold(self.Player1)
                            elif self.StartPlayer == 2:
                                self.Disk.setHold(self.Player2)
        else:
            self.updateMatchMenu()

        self.keysP1.update()
        self.keysP2.update()

    def render(self):
        GameState.render(self)

        self.Stadium.render(self.Player1, self.Player2, self.Disk, self.avatarPlayer1, self.avatarPlayer2, self.Screen)

        for e in self.Objects:
            e.render(self.Screen)

        i = 0
        while i < self.Player1.Energy:
            self.Stadium.specialBarP1[i].render(self.Screen)
            i += 1
        i = 0
        while i < self.Player2.Energy:
            self.Stadium.specialBarP2[i].render(self.Screen)
            i += 1

        self.screenTexts()

        if self.Paused:
            self.renderMatchMenu()
        elif not self.Started and not self.Intro:
            self.Coin.render(self.Screen)
        elif self.Intro:
            self.renderIntro()
        elif self.Finished:
            self.renderMatchMenu()

    def startMatch(self, p1, p2, stadium, intro):
        self.setStadium(stadium)
        self.setPlayer1(p1)
        self.setPlayer2(p2)
        self.Disk = Disk()

        self.Paused = False
        self.Finished = False
        self.Started = not intro
        self.Intro = intro
        self.IntroFrames = 180
        self.StartFrames = 60

        self.TimerMin = 1
        self.TimerSec = 30

        self.Scores[1] = 0
        self.Scores[2] = 0

        self.dia = Math.randNumberBetween(0, 1)

        #--------------------Player1Bounds------------------
        aMinX1 = self.Stadium.Llimit + self.Stadium.LeftLimit1.getWidth() / 2 + (self.Player1.collidesZoneBody.getWidth()) + 1 * self.sc
        aMinY1 = self.Stadium.Ulimit + self.Stadium.borderup.getHeight()/2 + (self.Player1.collidesZone.getHeight()/2)
        aMaxX1 = self.Stadium.middle.getX() - int(self.Player1.collidesZoneBody.getWidth() * 0.60)
        aMaxY1 = self.Stadium.Dlimit - self.Stadium.borderdown.getHeight()/2
        self.Player1.setBounds(aMinX1, aMinY1, aMaxX1, aMaxY1)

        # --------------------Player2Bounds-----------------
        aMinX2 = self.Stadium.middle.getX() + int(self.Player2.collidesZoneBody.getWidth() * 0.60)
        aMinY2 = self.Stadium.Ulimit + self.Stadium.borderup.getHeight()/2 + (self.Player2.collidesZone.getHeight() /2)
        aMaxX2 = self.Stadium.Rlimit - self.Stadium.RightLimit1.getWidth()/2 - (self.Player2.collidesZoneBody.getWidth()) - 1 * self.sc
        aMaxY2 = self.Stadium.Dlimit - self.Stadium.borderdown.getHeight()/2
        self.Player2.setBounds(aMinX2, aMinY2, aMaxX2, aMaxY2)
        #---------------------------------------------------

        self.Player1.setXY(self.Stadium.Llimit + self.screenWidth * 0.20, int((self.Stadium.Ulimit + self.Stadium.Dlimit)/2) + self.Player1.collidesZone.getHeight()/2)
        self.Player2.setXY(self.Stadium.Rlimit - self.screenWidth * 0.20, int((self.Stadium.Ulimit + self.Stadium.Dlimit)/2) + self.Player2.collidesZone.getHeight()/2)

        self.Coin = AssetAnimated(AssetManager.inst().Coin, False, 1)
        self.Coin.setXY(self.screenWidth/2, self.screenHeight/2)
        self.Coin.initAnimation(self.Coin.mFrame, 0, -1, 0.25, False)

        self.buttonSelect = Sprite()
        self.buttonSelect.setImage(AssetManager.inst().ObjSimple("HUD/EndMenu/", "buttonselect.png"))
        self.buttonSelected = 1

        self.pauseMenuCreation()
        self.endMenuCreation()

        self.mouse.mostrarMouse = False

    def drawText(self, aX, aY, aMsg, aSize, aColor=(0, 0, 0)):
        sc = GameConstants.inst().SCALE
        texto = TextSprite(aMsg, int(aSize * sc), "assets/fonts/days.otf", aColor)
        texto.setXY(aX, aY)
        texto.render(self.Screen)
        return texto

    def add(self, aElement):
        self.Objects.append(aElement)

    def setPlayer1(self, PJ):
        self.Player1 = CharacterFactory().inst().createCharacter(PJ, 1)
        self.avatarPlayer1 = AssetAnimated(AssetManager.Avatars[1][self.Player1.charID], True, 20)
        self.avatarPlayer1.setXY(self.Stadium.avatarframeP1.getX(), self.Stadium.avatarframeP1.getY())
        self.Objects.append(self.avatarPlayer1)

    def setPlayer2(self, PJ):
        self.Player2 = CharacterFactory().inst().createCharacter(PJ, 2)
        self.avatarPlayer2 = AssetAnimated(AssetManager.Avatars[2][self.Player2.charID], True, 20)
        self.avatarPlayer2.setXY(self.Stadium.avatarframeP2.getX(), self.Stadium.avatarframeP2.getY())
        self.Objects.append(self.avatarPlayer2)

    def setStadium(self, stadium):
        if stadium == 0:
            horaRandom = Math.randNumberBetween(1, 4)

            #esto para que sea mas probable jugar de dia
            # 100 / 4 = 75% de chance jugar dia 25% noche
            if horaRandom >= 3:
                horaRandom = 1
            self.Stadium = BeachStadium(horaRandom)

    def checkGoal(self):
        if not self.Goal:
            if self.Disk.getX() > self.screenWidth + self.screenWidth * 0.1:
                self.scoreGoal(self.Player1.playerNumber)
                self.Player2.addEnergy()
                try:
                    AudioManager.inst().playGoal()
                except:
                    return
            elif self.Disk.getX() < 0 - self.screenWidth * 0.1:
                self.scoreGoal(self.Player2.playerNumber)
                try:
                    AudioManager.inst().playGoal()
                except:
                    return

        if self.Disk.getX() > self.screenWidth * 2:
            self.endGoal(self.Player2)
        elif self.Disk.getX() < (self.screenWidth * 1)*-1:
            self.endGoal(self.Player1)

    def endMatch(self):
        self.Started = False
        self.destroy()

    def pauseMenu(self):
        self.BG_Veil.render(self.Screen)
        self.mTextPause.render(self.Screen)
        self.keysP1.render(self.Screen)
        self.keysP2.render(self.Screen)

    def timePass(self):
        if self.TimerMin == 0 and self.TimerSec == 0:
            self.Finished = True
            return
        self.TimeFrames += 1
        if self.TimeFrames >= self.FPS:
            self.TimeFrames = 0
            self.TimerSec -= 1
            if self.TimerSec < 0:
                self.TimerMin -= 1
                self.TimerSec = 59

        self.verifyEnergy()

    def textTime(self):
        textSec = ""
        if self.TimerSec < 10:
            textSec = ":0" + str(self.TimerSec)
        else:
            textSec = ":" + str(self.TimerSec)
        return str(self.TimerMin) + textSec

    def screenTexts(self):
        self.drawText(self.Stadium.timerbox.getX(), self.Stadium.timerbox.getY(), self.textTime(), 60, (255, 255, 255))
        self.drawText(self.Stadium.scoreleft.getX() + self.Stadium.scoreleft.getWidth()*0.10, self.Stadium.scoreleft.getY(), str(self.Scores[1]), 40, (255, 255, 255))
        self.drawText(self.Stadium.scoreright.getX() - self.Stadium.scoreright.getWidth()*0.10, self.Stadium.scoreright.getY(), str(self.Scores[2]), 40, (255, 255, 255))

        if self.Goal:
            if self.TimeFrames%2 == 0:
                self.GoalFrames[0].render(self.Screen)
            elif self.TimeFrames%2 != 0:
                self.GoalFrames[self.GoalPlayer].render(self.Screen)

    def goalConf(self):
        self.GoalFrames.append(TextSprite("GOAL", int(320 * GameConstants.inst().SCALE), "assets/fonts/m3x6.ttf", (255, 255, 255)))
        self.GoalFrames.append(TextSprite("GOAL", int(320 * GameConstants.inst().SCALE), "assets/fonts/m3x6.ttf", (0, 0, 128)))
        self.GoalFrames.append(TextSprite("GOAL", int(320 * GameConstants.inst().SCALE), "assets/fonts/m3x6.ttf", (128, 0, 0)))
        self.GoalFrames[0].setXY(GameConstants.inst().SCREEN_WIDTH / 2, GameConstants.inst().SCREEN_HEIGHT / 2)
        self.GoalFrames[1].setXY(GameConstants.inst().SCREEN_WIDTH / 2, GameConstants.inst().SCREEN_HEIGHT / 2)
        self.GoalFrames[2].setXY(GameConstants.inst().SCREEN_WIDTH / 2, GameConstants.inst().SCREEN_HEIGHT / 2)

    def scoreGoal(self, playerNumber):
        self.Goal = True
        if playerNumber == 1:
            self.Scores[1] += 1
            self.GoalPlayer = 1
        elif playerNumber == 2:
            self.Scores[2] += 1
            self.GoalPlayer = 2

    def endGoal(self, player):
        self.Disk.char = player
        player.setDisk(self.Disk)
        self.Goal = False

    def verifyEnergy(self):
        self.Player1.EnergyFrames += 1
        self.Player2.EnergyFrames += 1

        if self.Player1.EnergyFrames >= self.Player1.PowerChargeFrames:
            self.Player1.addEnergy()
            self.Player1.EnergyFrames = 0

        if self.Player2.EnergyFrames >= self.Player2.PowerChargeFrames:
            self.Player2.addEnergy()
            self.Player2.EnergyFrames = 0

    def runIntro(self):
        self.IntroFrames -= 1

        if self.IntroFrames == 0:
            self.Intro = False

    def renderIntro(self):
        self.BG_Veil.render(self.Screen)
        self.keysP1.render(self.Screen)
        self.keysP2.render(self.Screen)
        self.drawText(self.screenWidth / 2+5, self.screenHeight * 0.25+5, str(int(self.IntroFrames / 60)+1), 150, (0, 0, 0))
        self.drawText(self.screenWidth / 2, self.screenHeight * 0.25, str(int(self.IntroFrames / 60)+1), 150, (255, 255, 255))

    def pauseMenuCreation(self):
        self.PauseMenu = []

        self.bgscreen = Sprite()
        self.bgscreen.setImage(AssetManager.inst().ObjSimple("HUD/EndMenu/", "pauseMenu" + str(self.Stadium.ID) + ".png"))
        self.bgscreen.setXY(self.screenWidth / 2, self.screenHeight / 2)
        self.PauseMenu.append(self.bgscreen)

        self.framePauseMenu = Sprite()
        self.framePauseMenu.setImage(AssetManager.inst().ObjSimple("HUD/EndMenu/", "framePausedMenu.png"))
        self.framePauseMenu.setXY(self.screenWidth / 2, self.screenHeight / 2)
        self.PauseMenu.append(self.framePauseMenu)

        self.resumeButton = Sprite()
        self.resumeButton.setImage(AssetManager.inst().MenuButtons[0][0])
        self.resumeButton.setXY(self.framePauseMenu.getX(), (self.framePauseMenu.getY() - self.framePauseMenu.getHeight()/2) * 1.39)
        self.PauseMenu.append(self.resumeButton)

        self.screenButton = Sprite()
        self.screenButton.setImage(AssetManager.inst().MenuButtons[2][0])
        self.screenButton.setXY(self.framePauseMenu.getX(), self.PauseMenu[2].getY() + 87 * self.sc)
        self.PauseMenu.append(self.screenButton)

        self.settingsButton = Sprite()
        self.settingsButton.setImage(AssetManager.inst().MenuButtons[3][0])
        self.settingsButton.setXY(self.framePauseMenu.getX(), self.PauseMenu[3].getY() + 87 * self.sc)
        self.PauseMenu.append(self.settingsButton)

        self.mainmenuButton = Sprite()
        self.mainmenuButton.setImage(AssetManager.inst().MenuButtons[4][0])
        self.mainmenuButton.setXY(self.framePauseMenu.getX(), self.PauseMenu[4].getY() + 87 * self.sc)
        self.PauseMenu.append(self.mainmenuButton)

    def endMenuCreation(self):
        self.EndMenu = []

        self.bgscreen = Sprite()
        self.bgscreen.setImage(AssetManager.inst().ObjSimple("HUD/EndMenu/", "pauseMenu" + str(self.Stadium.ID) + ".png"))
        self.bgscreen.setXY(self.screenWidth / 2, self.screenHeight / 2)
        self.EndMenu.append(self.bgscreen)

        self.frameEndMenu = Sprite()
        self.frameEndMenu.setImage(AssetManager.inst().ObjSimple("HUD/EndMenu/", "frameEndMenu.png"))
        self.frameEndMenu.setXY(self.screenWidth / 2, self.screenHeight / 2)
        self.EndMenu.append(self.frameEndMenu)

        self.rematchButton = Sprite()
        self.rematchButton.setImage(AssetManager.inst().MenuButtons[1][0])
        self.rematchButton.setXY(self.screenWidth / 2, (self.frameEndMenu.getY() - self.frameEndMenu.getHeight()/2) * 1.19)
        self.EndMenu.append(self.rematchButton)

        self.screenButton = Sprite()
        self.screenButton.setImage(AssetManager.inst().MenuButtons[2][0])
        self.screenButton.setXY(self.framePauseMenu.getX(), self.EndMenu[2].getY() + 87 * self.sc)
        self.EndMenu.append(self.screenButton)

        self.settingsButton = Sprite()
        self.settingsButton.setImage(AssetManager.inst().MenuButtons[3][0])
        self.settingsButton.setXY(self.framePauseMenu.getX(), self.EndMenu[3].getY() + 87 * self.sc)
        self.EndMenu.append(self.settingsButton)

        self.mainmenuButton = Sprite()
        self.mainmenuButton.setImage(AssetManager.inst().MenuButtons[4][0])
        self.mainmenuButton.setXY(self.framePauseMenu.getX(), self.EndMenu[4].getY() + 87 * self.sc)
        self.EndMenu.append(self.mainmenuButton)

    def updateMatchMenu(self):
        from api.Game import Game
        menu = []
        if self.settings.visible:
            self.settings.update()
        else:
            if self.Paused:
                menu = self.PauseMenu
            elif self.Finished:
                menu = self.EndMenu

            self.updateKeyMov(menu)

            if menu[2].collides(self.mouse.getPunta()) and (self.mouse.getState() == self.mouse.CLICKED or Keyboard.inst().previousC()):
                if self.mouse.isEnded() or Keyboard.inst().previousC():
                    if self.Paused:
                        self.togglePause()
                    elif self.Finished:
                        self.rematch()
            elif menu[3].collides(self.mouse.getPunta()) and (self.mouse.getState() == self.mouse.CLICKED or Keyboard.inst().previousC()):
                menu[3].setImage(AssetManager.inst().MenuButtons[2][1])
                if self.mouse.isEnded() or Keyboard.inst().previousC():
                    menu[3].setImage(AssetManager.inst().MenuButtons[2][0])
                    Game.inst().setState(LvConfiguration())
            elif menu[4].collides(self.mouse.getPunta()) and (self.mouse.getState() == self.mouse.CLICKED or Keyboard.inst().previousC()):
                menu[4].setImage(AssetManager.inst().MenuButtons[3][1])
                if self.mouse.isEnded() or Keyboard.inst().previousC():
                    menu[4].setImage(AssetManager.inst().MenuButtons[3][0])
                    self.settings.open()
            elif menu[5].collides(self.mouse.getPunta()) and (self.mouse.getState() == self.mouse.CLICKED or Keyboard.inst().previousC()):
                menu[5].setImage(AssetManager.inst().MenuButtons[4][1])
                if self.mouse.isEnded() or Keyboard.inst().previousC():
                    menu[5].setImage(AssetManager.inst().MenuButtons[4][0])
                    Game.inst().setState(MenuState())

    def updateKeyMov(self, menu):
        if Keyboard.inst().previousW() or Keyboard.inst().previousS():
            if Keyboard.inst().previousW():
                if self.buttonSelected <= 2:
                    self.buttonSelected = 5
                else:
                    self.buttonSelected -= 1
            elif Keyboard.inst().previousS():
                if self.buttonSelected == 5:
                    self.buttonSelected = 2
                else:
                    self.buttonSelected += 1

            btn = menu[self.buttonSelected]
            pygame.mouse.set_pos(btn.getX() + self.mouse.getWidth()/2, btn.getY() + self.mouse.getHeight()/2)

    def renderMatchMenu(self):
        menu = []
        if self.Paused:
            menu = self.PauseMenu
        elif self.Finished:
            menu = self.EndMenu

        i = 0
        while i < len(menu):
            menu[i].render(self.Screen)
            i += 1
        # self.buttonSelect.render(self.Screen)

        self.keysP1.render(self.Screen)
        self.keysP2.render(self.Screen)

        if self.settings.visible:
            self.settings.render()

    def destroy(self):
        # i = len(self.Objects)
        # while i > 0:
        #     self.Objects[i - 1].destroy()
        #     self.Objects.pop(i - 1)
        #     i = i - 1

        # self.Player1.destroy()
        # self.Player2.destroy()
        # self.Stadium.destroy()
        # self.Disk.destroy()

        self.mTextPause.destroy()
        self.mTextPause = None

    def rematch(self):
        self.StartPlayer = Math.randNumberBetween(1, 2)

        self.Scores[1] = 0
        self.Scores[2] = 0

        self.Finished = False
        self.Started = False
        self.StartFrames = 60
        self.Intro = True
        self.IntroFrames = 180

        self.Player1.setXY(self.Stadium.Llimit + self.screenWidth * 0.20, int((self.Stadium.Ulimit + self.Stadium.Dlimit) / 2) + self.Player1.collidesZone.getHeight() / 2)
        self.Player2.setXY(self.Stadium.Rlimit - self.screenWidth * 0.20, int((self.Stadium.Ulimit + self.Stadium.Dlimit) / 2) + self.Player2.collidesZone.getHeight() / 2)
        self.Player1.setState(self.Player1.NORMAL)
        self.Player1.disk = None
        self.Player2.setState(self.Player1.NORMAL)
        self.Player2.disk = None
        self.Disk.char = None
        self.Disk.setState(self.Disk.NORMAL)
        self.Disk.setVisible(False)

        self.Coin.setXY(self.Stadium.screenWidth / 2, self.Stadium.screenHeight / 2)
        self.Coin.initAnimation(self.Coin.mFrame, 0, 18, 0.25, False)

        self.TimerMin = 1
        self.TimerSec = 30

        self.mouse.mostrarMouse = False
