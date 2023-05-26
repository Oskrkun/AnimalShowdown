# -*- coding: utf-8 -*-

import pygame
from api.Keyboard import *
from api.Game import *
from api.GameState import *
from api.TextSprite import *
from game.states.LvConfiguration import *
from api.AssetAnimatedAction import *
from api.AssetAnimated import *
from api.AudioManager import *


class Settings(GameState):

    mInstance = None
    mInitialized = False

    def __new__(self, *args, **kargs):
        if (Settings.mInstance is None):
            Settings.mInstance = object.__new__(self, *args, **kargs)
            self.init(Settings.mInstance)
        else:
            print (
            "Cuidado: Settings(): No se debería instanciar más de una vez esta clase. Usar Settings.inst().")
        return Settings.mInstance

    @classmethod
    def inst(cls):
        if (not cls.mInstance):
            return cls()
        return cls.mInstance

    def init(self):
        from api.Game import Game

        if (AudioManager.mInitialized):
            return
        GameState.__init__(self)

        self.gc = GameConstants.inst()
        self.game = Game.inst()
        self.audio = AudioManager.inst()

        self.screen = self.game.getScreen()
        self.mouse = self.game.mMousePointer

        ruta = "assets/images/Basics/settings/"

        self.visible = False
        self.res = self.gc.ResSelected
        self.objects = []
        self.buttons = []

        self.frame = Sprite()
        self.frame.setImage(AssetManager.inst().ObjSimple("Basics/settings/", "settingsframe.png"))
        self.frame.setXY(self.gc.SCREEN_WIDTH/2, self.gc.SCREEN_HEIGHT/2)

        frameLeft = self.frame.getX() - self.frame.getWidth() / 2
        frameTop = self.frame.getY() - self.frame.getHeight() / 2

        self.title = TextSprite("Settings", int(100 * self.gc.SCALE), "assets/fonts/m3x6.ttf", (25, 49, 61))
        self.title.setXY(self.frame.getX(), frameTop + self.frame.getHeight() * 0.10)

        self.txtRes = TextSprite("Resolution", int(75 * self.gc.SCALE), "assets/fonts/m3x6.ttf", (25, 49, 61))
        self.txtRes.setXY(frameLeft * 1.05 + self.txtRes.getWidth()/2, frameTop + self.frame.getHeight() * 0.30)

        self.txtFull = TextSprite("Fullscreen", int(75 * self.gc.SCALE), "assets/fonts/m3x6.ttf", (25, 49, 61))
        self.txtFull.setXY(frameLeft * 1.05 + self.txtFull.getWidth() / 2, frameTop + self.frame.getHeight() * 0.45)

        self.txtMute = TextSprite("Mute Sounds", int(75 * self.gc.SCALE), "assets/fonts/m3x6.ttf", (25, 49, 61))
        self.txtMute.setXY(frameLeft * 1.05 + self.txtMute.getWidth() / 2, frameTop + self.frame.getHeight() * 0.60)

        self.resArrowUp = Sprite()
        self.resArrowUp.setImage(AssetManager.inst().ObjSimple("Basics/settings/", "verArrowUp.png"))
        self.resArrowUp.setXY((frameLeft + self.frame.getWidth()) * 0.95, self.txtRes.getY() * 0.96)

        self.resArrowDown = Sprite()
        self.resArrowDown.setImage(AssetManager.inst().ObjSimple("Basics/settings/", "verArrowDown.png"))
        self.resArrowDown.setXY((frameLeft + self.frame.getWidth()) * 0.95, self.txtRes.getY() * 1.06)

        self.fullStates = AssetManager.inst().loadAssets(ruta, "checkbox", self.gc.SCALE)
        self.checkboxFull = Sprite()
        self.checkboxFull.setImage(self.fullStates[0])
        self.checkboxFull.setXY((frameLeft + self.frame.getWidth()) * 0.87, self.txtFull.getY())
        self.FullChecked = False

        self.muteStates = AssetManager.inst().loadAssets(ruta, "checkboxSound", self.gc.SCALE)
        self.checkboxMute = Sprite()
        self.checkboxMute.setImage(self.muteStates[0])
        self.checkboxMute.setXY((frameLeft + self.frame.getWidth()) * 0.87, self.txtMute.getY())
        self.MuteChecked = False

        self.applyButton = AssetManager.inst().loadAssets(ruta, "btn_apply", self.gc.SCALE)
        self.apply = Sprite()
        self.apply.setImage(self.applyButton[0])
        self.apply.setXY(self.frame.getX() * 0.88, frameTop + self.frame.getHeight() * 0.85)

        self.cancelButton = AssetManager.inst().loadAssets(ruta, "btn_cancel", self.gc.SCALE)
        self.cancel = Sprite()
        self.cancel.setImage(self.cancelButton[0])
        self.cancel.setXY(self.frame.getX() * 1.12, frameTop + self.frame.getHeight() * 0.85)

        self.buttonSelected = -1
        self.buttons.append(self.checkboxFull)
        self.buttons.append(self.checkboxMute)
        self.buttons.append(self.apply)
        self.buttons.append(self.cancel)

        self.objects.append(self.frame)
        self.objects.append(self.title)
        self.objects.append(self.txtRes)
        self.objects.append(self.txtFull)
        self.objects.append(self.txtMute)
        # self.objects.append(self.resArrowUp)
        # self.objects.append(self.resArrowDown)
        self.objects.append(self.checkboxFull)
        self.objects.append(self.checkboxMute)
        self.objects.append(self.apply)
        self.objects.append(self.cancel)

    def update(self):
        GameState.update(self)

        i = 0
        while i < len(self.objects):
            self.objects[i].update()
            i += 1

        txt = str(self.gc.ResolutionsWIDTH[self.res]) + "x" + str(self.gc.ResolutionsHEIGHT[self.res])
        self.txtRes.setText("Resolution: " + txt)
        self.txtRes.setX((self.frame.getX() - self.frame.getWidth() / 2) * 1.05 + self.txtRes.getWidth()/2)

        self.updateKeyMov()

        if self.cancel.collides(self.mouse.getPunta()) and (self.mouse.getState() == self.mouse.CLICKED or Keyboard.inst().previousC()):
            self.cancel.setImage(self.cancelButton[1])
            if self.mouse.isEnded() or Keyboard.inst().previousC():
                self.cancel.setImage(self.cancelButton[0])
                AudioManager.inst().playConfirmOption()
                self.close()

        elif self.apply.collides(self.mouse.getPunta()) and (self.mouse.getState() == self.mouse.CLICKED or Keyboard.inst().previousC()):
            self.apply.setImage(self.applyButton[1])
            if self.mouse.isEnded() or Keyboard.inst().previousC():
                self.apply.setImage(self.applyButton[0])
                # self.gc.changeResolution(self.res)
                # self.game.RESOLUTION = (self.gc.ResolutionsWIDTH[self.res], self.gc.ResolutionsHEIGHT[self.res])
                self.game.mIsFullscreen = self.FullChecked
                self.game.fullORnot()
                self.audio.playORmute(self.MuteChecked)
                AudioManager.inst().playConfirmOption()
                self.close()


        # elif self.resArrowUp.collides(self.mouse.getPunta()) and self.mouse.getState() == self.mouse.CLICKED:
        #     if self.mouse.isEnded():
        #         if self.res == 0:
        #             self.res = len(self.gc.ResolutionsWIDTH)-1
        #         else:
        #             self.res -= 1
        #
        # elif self.resArrowDown.collides(self.mouse.getPunta()) and self.mouse.getState() == self.mouse.CLICKED:
        #     if self.mouse.isEnded():
        #         if self.res == len(self.gc.ResolutionsWIDTH)-1:
        #             self.res = 0
        #         else:
        #             self.res += 1

        elif self.checkboxFull.collides(self.mouse.getPunta()) and (self.mouse.getState() == self.mouse.CLICKED or Keyboard.inst().previousC()):
            if self.mouse.isEnded() or Keyboard.inst().previousC():
                if self.FullChecked:
                    self.FullChecked = False
                    self.checkboxFull.setImage(self.fullStates[0])
                else:
                    self.FullChecked = True
                    self.checkboxFull.setImage(self.fullStates[1])
                AudioManager.inst().playConfirmOption()

        elif self.checkboxMute.collides(self.mouse.getPunta()) and (self.mouse.getState() == self.mouse.CLICKED or Keyboard.inst().previousC()):
            if self.mouse.isEnded() or Keyboard.inst().previousC():
                if self.MuteChecked:
                    self.MuteChecked = False
                    self.checkboxMute.setImage(self.muteStates[0])
                else:
                    self.MuteChecked = True
                    self.checkboxMute.setImage(self.muteStates[1])

                AudioManager.inst().playConfirmOption()

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

        i = 0
        while i < len(self.objects):
            self.objects[i].render(self.screen)
            i += 1

    def destroy(self):
        i = 0
        while i < len(self.objects):
            self.objects[i].destroy()
            i += 1
        GameState.destroy(self)

    def open(self):
        self.visible = True
        self.res = self.gc.ResSelected
        self.FullChecked = self.game.mIsFullscreen
        self.MuteChecked = self.audio.muted

        if self.FullChecked:
            self.checkboxFull.setImage(self.fullStates[1])
        else:
            self.checkboxFull.setImage(self.fullStates[0])

        if self.MuteChecked:
            self.checkboxMute.setImage(self.muteStates[1])
        else:
            self.checkboxMute.setImage(self.muteStates[0])

    def close(self):
        self.visible = False

