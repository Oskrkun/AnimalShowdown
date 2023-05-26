# -*- coding: utf-8 -*-
import pygame
from api.Keyboard import *
from api.Game import *
from api.GameState import *
from api.TextSprite import *
from api.AssetAnimatedAction import *
from api.AssetManager import *
from api.AssetAnimated import *
from game.Settings import *


class MenuState(GameState):

    mImgSpace = None

    mTextTitle = None
    mTextPressFire = None

    def __init__(self):
        from api.Game import Game
        GameState.__init__(self)

        self.mImgSpace = None
        self.mTextTitle = None
        self.mTextPressFire = None

        self.sc = GameConstants.inst().SCALE
        self.game = Game.inst()
        self.Screen = self.game.getScreen()
        self.screenWidth = GameConstants.inst().SCREEN_WIDTH
        self.screenHeight = GameConstants.inst().SCREEN_HEIGHT

        self.settings = Settings.inst()

        self.ready = True
        self.objects = []
        self.buttons = []
        self.credits = []
        self.showCredits = False

    def init(self):
        GameState.init(self)

        self.mouse = self.game.mMousePointer
        self.mouse.mostrarMouse = True

        ruta = "assets/images/Basics/menu_principal/"
        self.game.setBackground(AssetManager.inst().ObjSimple("Basics/menu_principal/", "background.png"))

        self.bg2 = Sprite()
        self.bg2.setRegistration(self.bg2.TOP_LEFT)
        self.bg2.setImage(AssetManager.inst().ObjSimple("Basics/menu_principal/", "background2.png"))
        self.bg2.setXY(0, 0)

        self.frameLeft = Sprite()
        self.frameLeft.setRegistration(self.frameLeft.TOP_LEFT)
        self.frameLeft.setImage(AssetManager.inst().ObjSimple("Basics/menu_principal/", "frameLeft.png"))
        self.frameLeft.setXY(self.frameLeft.getWidth() * -1.5, 0)

        self.playButton = AssetManager.inst().loadAssets(ruta, "btn_play", self.sc)
        self.btn_play = Sprite()
        self.btn_play.setImage(self.playButton[0])

        self.leaderboardButton = AssetManager.inst().loadAssets(ruta, "btn_leaderboard", self.sc)
        self.btn_leaderboard = Sprite()
        self.btn_leaderboard.setImage(self.leaderboardButton[0])

        self.notAvleaderboard = Sprite()
        self.notAvleaderboard.setImage(AssetManager.inst().ObjSimple("Basics/menu_principal/", "notAvailable.png"))

        self.storeButton = AssetManager.inst().loadAssets(ruta, "btn_credits", self.sc)
        self.btn_store = Sprite()
        self.btn_store.setImage(self.storeButton[0])

        self.optionsButton = AssetManager.inst().loadAssets(ruta, "btn_options", self.sc)
        self.btn_options = Sprite()
        self.btn_options.setImage(self.optionsButton[0])

        self.quitButton = AssetManager.inst().loadAssets(ruta, "btn_quit", self.sc)
        self.btn_quit = Sprite()
        self.btn_quit.setImage(self.quitButton[0])

        self.sun = AssetManager.inst().loadAssets(ruta, "sun", self.sc, False)
        self.sun = AssetAnimated(self.sun, True, 2)
        self.sun.setXY(self.screenWidth * 0.45, self.screenHeight * 0.25)

        self.logo = Sprite()
        self.logo.setImage(AssetManager.inst().ObjSimple("Basics/menu_principal/", "logo.png"))
        self.logo.setXY(self.screenWidth * 0.70, self.screenHeight * 0.15)

        ruta = "assets/images/HUD/"
        self.keysRef = []
        self.keysRef.append(AssetManager.inst().loadAssets(ruta + "keys/", "keysJoyselec_", self.sc))
        self.keysRef.append(AssetManager.inst().loadAssets(ruta + "keys/", "keysP1selec_", self.sc))

        self.keys = AssetAnimated(self.keysRef[1], True, 20)
        if Keyboard.inst().cantJoy >= 1:
            self.keys.initAnimation(self.keysRef[0], 0, -1, 20, True)

        self.createCredits()
        self.objects.append(self.bg2)
        self.objects.append(self.frameLeft)
        self.objects.append(self.btn_play)
        self.objects.append(self.btn_leaderboard)
        self.objects.append(self.btn_store)
        self.objects.append(self.btn_options)
        self.objects.append(self.btn_quit)
        self.objects.append(self.keys)
        self.objects.append(self.sun)
        self.objects.append(self.logo)
        self.objects.append(self.notAvleaderboard)

        self.buttonSelected = -1
        self.buttons.append(self.btn_play)
        self.buttons.append(self.btn_leaderboard)
        self.buttons.append(self.btn_store)
        self.buttons.append(self.btn_options)
        self.buttons.append(self.btn_quit)

    def update(self):
        GameState.update(self)
        self.ready = True

        if Keyboard.inst().escape():
            self.game.mSalir = True

        i = 0
        while i < len(self.objects):
            self.objects[i].update()
            i += 1

        if self.showCredits:
            self.updateCredits()

        # (PosObjetivo - PosActual) / 12
        if self.frameLeft.getX() < 0:
            self.frameLeft.setVelX((0 - self.frameLeft.getX()) / 12 + 1)
            self.placeLeftFrameObjects()
            self.ready = False
        elif self.frameLeft.getX() > 0:
            self.frameLeft.setX(0)
            self.frameLeft.setVelX(0)
            self.placeLeftFrameObjects()

        if self.settings.visible:
            self.settings.update()
        else:
            self.updateKeyMov()
            if self.btn_play.collides(self.mouse.getPunta()) and (self.mouse.getState() == self.mouse.CLICKED or Keyboard.inst().previousC()):
                self.btn_play.setImage(self.playButton[1])
                if self.mouse.isEnded() or Keyboard.inst().previousC():
                    AudioManager.inst().playConfirmOption()
                    from game.states.LvConfiguration import LvConfiguration
                    nextState = LvConfiguration()
                    self.game.setState(nextState)
                    self.btn_play.setImage(self.playButton[0])
            elif self.btn_store.collides(self.mouse.getPunta()) and (self.mouse.getState() == self.mouse.CLICKED or Keyboard.inst().previousC()):
                self.btn_store.setImage(self.storeButton[1])
                if self.mouse.isEnded() or Keyboard.inst().previousC():
                    self.activateCredits()
                    self.btn_store.setImage(self.storeButton[0])
                    AudioManager.inst().playConfirmOption()
            elif self.btn_options.collides(self.mouse.getPunta()) and (self.mouse.getState() == self.mouse.CLICKED or Keyboard.inst().previousC()):
                self.btn_options.setImage(self.optionsButton[1])
                if self.mouse.isEnded() or Keyboard.inst().previousC():
                    self.settings.open()
                    self.btn_options.setImage(self.optionsButton[0])
                    AudioManager.inst().playConfirmOption()
            elif self.btn_quit.collides(self.mouse.getPunta()) and (self.mouse.getState() == self.mouse.CLICKED or Keyboard.inst().previousC()):
                self.btn_quit.setImage(self.quitButton[1])
                if self.mouse.isEnded() or Keyboard.inst().previousC():
                    self.game.mSalir = True
                    self.btn_quit.setImage(self.quitButton[0])

    def placeLeftFrameObjects(self):
        self.btn_play.setXY(self.frameLeft.getX() + self.frameLeft.getWidth() * 0.60, self.frameLeft.getHeight() * 0.15)
        self.btn_leaderboard.setXY(self.btn_play.getX(), self.btn_play.getY() + 170 * self.sc)
        self.btn_store.setXY(self.btn_play.getX(), self.btn_leaderboard.getY() + 170 * self.sc)
        self.btn_options.setXY(self.btn_play.getX(), self.btn_store.getY() + 170 * self.sc)
        self.btn_quit.setXY(self.btn_play.getX(), self.btn_options.getY() + 150 * self.sc)
        self.keys.setXY(self.frameLeft.getX()+self.frameLeft.getWidth()/2, self.btn_quit.getY() + 150 * self.sc)
        self.notAvleaderboard.setXY(self.btn_leaderboard.getX(), self.btn_leaderboard.getY())

    def updateKeyMov(self):
        if Keyboard.inst().previousW() or Keyboard.inst().previousS():
            max = len(self.buttons)-1
            if Keyboard.inst().previousW():
                if self.buttonSelected <= 0:
                    self.buttonSelected = max
                else:
                    self.buttonSelected -= 1
                AudioManager.inst().playMoveOption()
            elif Keyboard.inst().previousS():
                if self.buttonSelected == max:
                    self.buttonSelected = 0
                else:
                    self.buttonSelected += 1
                AudioManager.inst().playMoveOption()

            btn = self.buttons[self.buttonSelected]
            pygame.mouse.set_pos(btn.getX() + self.mouse.getWidth()/2, btn.getY() + self.mouse.getHeight()/2)

    def render(self):
        GameState.render(self)

        if self.showCredits:
            i = 0
            while i < len(self.credits):
                self.credits[i].render(self.Screen)
                i += 1

        i = 0
        while i < len(self.objects):
            self.objects[i].render(self.Screen)
            i += 1

        if self.settings.visible:
            self.settings.render()

    def destroy(self):
        GameState.destroy(self)

    def updateCredits(self):
        i = 0
        while i < len(self.credits):
            self.credits[i].update()
            if self.credits[i].getY() <= 500:
                self.credits[i].setBoundAction(GameObject.WRAP)
            i += 1

    def activateCredits(self):
        self.showCredits = not self.showCredits

        sep = 0.05
        i = 0
        while i < len(self.credits):
            if i < int(len(self.credits)/2):
                self.credits[i].setBoundAction(GameObject.NONE)
                self.credits[i].setXY(self.screenWidth * 0.80 + 3 * self.sc, self.screenHeight * (1 + sep * i) + 3 * self.sc)
            else:
                self.credits[i].setBoundAction(GameObject.NONE)
                self.credits[i].setXY(self.screenWidth * 0.80, self.screenHeight * (1 + sep * (i-int(len(self.credits)/2))))
            i += 1

    def createCredits(self):
        font = "assets/fonts/m3x6.ttf"
        size = 120
        sep = 0.05
        vel = 3

        shadows = []
        shadows.append(TextSprite("SOMBRAS", int(size * self.sc), font, (0, 0, 0)))
        shadows.append(TextSprite("Guzman Arevalo", int(size * self.sc), font, (0, 0, 0)))
        shadows.append(TextSprite("Jose Menendez", int(size * self.sc), font, (0, 0, 0)))
        shadows.append(TextSprite("Oscar Charlo", int(size * self.sc), font, (0, 0, 0)))
        shadows.append(TextSprite("Pablo A. Falero", int(size * self.sc), font, (0, 0, 0)))
        shadows.append(TextSprite("", int(size * self.sc), font, (0, 0, 0)))
        shadows.append(TextSprite("", int(size * self.sc), font, (0, 0, 0)))
        shadows.append(TextSprite("AGRADECIMIENTOS", int(size * self.sc), font, (0, 0, 0)))
        shadows.append(TextSprite("Fernando", int(size * self.sc), font, (0, 0, 0)))
        shadows.append(TextSprite("Ruben", int(size * self.sc), font, (0, 0, 0)))
        shadows.append(TextSprite("Tachuela", int(size * self.sc), font, (0, 0, 0)))

        i = 1
        while i < len(shadows):
            shadows[i].setXY(self.screenWidth * 0.80 + 3 * self.sc, self.screenHeight * (1 + sep * i) + 3 * self.sc)
            shadows[i].setVelY(-vel)
            shadows[i].setBounds(0, -150 * self.sc, self.screenWidth, self.screenHeight + 150 * self.sc)
            self.credits.append(shadows[i])
            i += 1

        lines = []
        lines.append(TextSprite("CREDITOS", int(size * self.sc), font, (255, 255, 255)))
        lines.append(TextSprite("Guzman Arevalo", int(size * self.sc), font, (255, 255, 255)))
        lines.append(TextSprite("Jose Menendez", int(size * self.sc), font, (255, 255, 255)))
        lines.append(TextSprite("Oscar Charlo", int(size * self.sc), font, (255, 255, 255)))
        lines.append(TextSprite("Pablo A. Falero", int(size * self.sc), font, (255, 255, 255)))
        lines.append(TextSprite("", int(size * self.sc), font, (255, 255, 255)))
        lines.append(TextSprite("", int(size * self.sc), font, (255, 255, 255)))
        lines.append(TextSprite("AGRADECIMIENTOS", int(size * self.sc), font, (255, 255, 255)))
        lines.append(TextSprite("Fernando", int(size * self.sc), font, (255, 255, 255)))
        lines.append(TextSprite("Ruben", int(size * self.sc), font, (255, 255, 255)))
        lines.append(TextSprite("Tachuela", int(size * self.sc), font, (255, 255, 255)))

        i = 1
        while i < len(lines):
            lines[i].setXY(self.screenWidth * 0.80, self.screenHeight * (1 + sep * i))
            print self.screenHeight * (1 + sep * i)
            lines[i].setVelY(-vel)
            lines[i].setBounds(0, -150 * self.sc, self.screenWidth, self.screenHeight + 150 * self.sc)
            self.credits.append(lines[i])
            i += 1

