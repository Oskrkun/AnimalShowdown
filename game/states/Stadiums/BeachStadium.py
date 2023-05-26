# -*- coding: utf-8 -*-

import pygame
from api.Keyboard import *
from api.Game import *
from api.GameState import *
from api.TextSprite import *
from game.states.LvConfiguration import *
from api.AssetAnimatedAction import *
from api.AssetAnimated import *
from game.Characters.Character import *
from game.Characters.Monkey import *
from game.Characters.Toucan import *
from game.CharacterFactory import *
from api.AssetManager import *
from game.Disk.Disk import *
from game.states.Stadiums.Stadium import *
from game.Reference import *
from api.ParticleManager import *


class BeachStadium(Stadium):

    specialBarP1 = []
    specialBarP2 = []

    def __init__(self , aClima):
        from api.Game import Game
        Stadium.__init__(self)
        self.sc = GameConstants.inst().SCALE

        self.ID = 0

        self.Clima = aClima

        #igual q siempre
        self.upperObjects = []
        #middle es el viejo lower
        self.centerObjects = []
        #lower es para hud y efectos por encima de toda la cancha
        self.lowerObjects = []

        self.Ulimit = GameConstants.inst().Ulimit
        self.Dlimit = GameConstants.inst().Dlimit
        self.Llimit = GameConstants.inst().Llimit
        self.Rlimit = GameConstants.inst().Rlimit

        AssMan = AssetManager.inst()

        # print("Limites: Up " , self.Ulimit , " / Down " , self.Dlimit , " / Left " , self.Llimit , " / Right " , self.Rlimit)



        #------------CANCHA------------------------------------------------------------
        #----Carga de assets------

        ruta = "assets/images/Stadium/Beach/"
        self.fxNight = AssMan.loadAssets(ruta, "fxNigth_", self.sc, False)

        if self.Clima == 1:
            self.mImg = pygame.image.load("assets/images/Stadium/Beach/beachBG.png").convert()
            self.mImg = pygame.transform.scale(self.mImg, (int(self.mImg.get_width() * self.sc), int(self.mImg.get_height() * self.sc)))
            self.sun = AssMan.loadAssets(ruta, "sun_", self.sc, False)
            self.borderup = AssMan.loadAssets(ruta, "borderup_0_", self.sc, False)
        elif self.Clima == 2:
            self.mImg = pygame.image.load("assets/images/Stadium/Beach/beachBGNight.png").convert()
            self.mImg = pygame.transform.scale(self.mImg, (int(self.mImg.get_width() * self.sc), int(self.mImg.get_height() * self.sc)))
            self.sun = AssMan.loadAssets(ruta, "moon_", self.sc, False)
            self.borderup = AssMan.loadAssets(ruta, "borderup_1_", self.sc, False)

        self.borderdown = AssMan.loadAssets(ruta, "borderdown_0_", self.sc, False)
        self.middle = AssMan.loadAssets(ruta, "middle_0_", self.sc, False)

        self.arcoAP1 = self.loadObjSimple("Stadium/Beach/arcos/", "arcoA.png", True)
        self.arcoBP1 = self.loadObjSimple("Stadium/Beach/arcos/", "arcoB.png", True)
        self.arcoAP2 = self.loadObjSimple("Stadium/Beach/arcos/", "arcoA.png")
        self.arcoBP2 = self.loadObjSimple("Stadium/Beach/arcos/", "arcoB.png")
        self.seatingP1 = self.loadObjSimple("Stadium/Beach/", "seating.png", True)
        self.seatingP2 = self.loadObjSimple("Stadium/Beach/", "seating.png")

        self.peopleLeft = AssMan.loadAssets(ruta + "people/", "people_0_", self.sc, True)
        self.peopleRight = AssMan.loadAssets(ruta + "people/", "people_0_", self.sc, False)
        self.sea = AssMan.loadAssets(ruta + "sea/", "sea_", self.sc, False)
        self.animatedSeaLeft = AssMan.loadAssets(ruta + "sea/", "animated_sea_", self.sc, False)
        self.animatedSeaRight = AssMan.loadAssets(ruta + "sea/", "animated_sea_", self.sc, True)
        self.palmsBG = AssMan.loadAssets(ruta + "palmsBG/", "palmsBG_", self.sc, False)
        self.palms = AssMan.loadAssets(ruta + "palmsFront/", "palms_", self.sc, False)
        self.cloudLeft = AssMan.loadAssets(ruta + "clouds/", "cloudLeft", self.sc, False)
        self.cloudRight = AssMan.loadAssets(ruta + "clouds/", "cloudRight", self.sc, False)
        self.cloud01 = AssMan.loadAssets(ruta + "clouds/", "cloud01_", self.sc, False)
        self.cloud02 = AssMan.loadAssets(ruta + "clouds/", "cloud02_", self.sc, False)
        self.cloud03 = AssMan.loadAssets(ruta + "clouds/", "cloud03_", self.sc, False)
        self.flag01 = AssMan.loadAssets(ruta + "flags/", "flag01_", self.sc, False)
        self.flag02 = AssMan.loadAssets(ruta + "flags/", "flag01_", self.sc, False)

        ruta = "assets/images/HUD/"
        self.specialmeterP1 = AssMan.loadAssets(ruta, "special_meter_0_", self.sc, False)
        self.specialmeterP2 = AssMan.loadAssets(ruta, "special_meter_0_", self.sc, False)
        self.timerbox = AssMan.loadAssets(ruta, "timer_", self.sc, False)
        self.scoreleft = AssMan.loadAssets(ruta, "scoreLeft_", self.sc, False)
        self.scoreright = AssMan.loadAssets(ruta, "scoreRight_", self.sc, False)
        self.avatarframeP1 = AssMan.loadAssets(ruta, "avatar1_", self.sc, False)
        self.avatarframeP2 = AssMan.loadAssets(ruta, "avatar2_", self.sc, False)

        i = 1
        while i <= 10:
            bar = self.loadObjSimple("HUD/", "energybar_0_00.png")
            self.specialBarP1.append(bar)
            i += 1
        i = 1
        while i <= 10:
            bar = self.loadObjSimple("HUD/", "energybar_0_00.png")
            self.specialBarP2.append(bar)
            i += 1

        self.fxNight = AssetAnimated(self.fxNight, True, 2)
        self.sun = AssetAnimated(self.sun, True, 2)
        self.borderup = AssetAnimated(self.borderup, True, 2)
        self.borderdown = AssetAnimated(self.borderdown, True, 2)
        self.middle = AssetAnimated(self.middle, True, 2)
        self.peopleLeft = AssetAnimated(self.peopleLeft, True, 6)
        self.peopleRight = AssetAnimated(self.peopleRight, True, 6)
        self.specialmeterP1 = AssetAnimated(self.specialmeterP1, True, 2)
        self.specialmeterP2 = AssetAnimated(self.specialmeterP2, True, 2)
        self.timerbox = AssetAnimated(self.timerbox, True, 2)
        self.scoreleft = AssetAnimated(self.scoreleft, True, 2)
        self.scoreright = AssetAnimated(self.scoreright, True, 2)
        self.avatarframeP1 = AssetAnimated(self.avatarframeP1, True, 2)
        self.avatarframeP2 = AssetAnimated(self.avatarframeP2, True, 2)
        self.sea = AssetAnimated(self.sea, True, 2)
        self.animatedSeaLeft = AssetAnimated(self.animatedSeaLeft, True, 10)
        self.animatedSeaRight = AssetAnimated(self.animatedSeaRight, True, 10)
        self.palmsBG = AssetAnimated(self.palmsBG, True, 5)
        self.palms = AssetAnimated(self.palms, True, 5)

        self.cloudLeft = AssetAnimated(self.cloudLeft, True, 2)
        self.cloudRight = AssetAnimated(self.cloudRight, True, 2)
        self.cloud01 = AssetAnimated(self.cloud01, True, 2)
        self.cloud02 = AssetAnimated(self.cloud02, True, 2)
        self.cloud03 = AssetAnimated(self.cloud03, True, 2)

        self.flag01 = AssetAnimated(self.flag01, True, 10)
        self.flag02 = AssetAnimated(self.flag02, True, 10)

        #---posiciones de assets-----
        self.fxNight.setXY(self.screenWidth / 2, self.screenHeight / 2)
        self.sun.setXY(self.screenWidth * 0.25, self.screenHeight * 0.10)
        self.sea.setRegistration(self.sea.TOP_LEFT)
        self.sea.setXY(0, self.screenHeight * 0.245)
        self.animatedSeaLeft.setRegistration(self.sea.TOP_LEFT)
        self.animatedSeaRight.setRegistration(self.sea.TOP_LEFT)
        self.animatedSeaLeft.setXY(0, self.sea.getY())
        self.animatedSeaRight.setXY(self.screenWidth - self.animatedSeaRight.getWidth(), self.sea.getY())
        self.borderup.setXY(self.screenWidth / 2, self.Ulimit)
        self.flag01.setXY(self.borderup.getX() * 0.85, self.borderup.getY() - self.borderup.getHeight()/2)
        self.flag02.setXY(self.borderup.getX() * 1.20, self.borderup.getY() - self.borderup.getHeight()/2)
        self.borderdown.setXY(self.screenWidth / 2, self.Dlimit - self.borderdown.getHeight()/2)
        self.palms.setXY(self.screenWidth / 2, self.screenHeight - self.palms.getHeight()/2)
        self.palmsBG.setXY(self.screenWidth / 2, 0 + self.palmsBG.getHeight() / 2)
        self.middle.setXY(self.screenWidth / 2, (self.Ulimit + self.Dlimit)/2)

        self.arcoAP1.setXY(0 + self.arcoAP1.getWidth()/2, self.screenHeight - self.arcoAP1.getHeight()/2)
        self.arcoBP1.setXY(self.arcoAP1.getX() + self.arcoAP1.getWidth()/2 - self.arcoBP1.getWidth()/2, self.arcoAP1.getY())
        self.arcoAP2.setXY(self.screenWidth - self.arcoAP1.getWidth()/2, self.screenHeight - self.arcoAP1.getHeight()/2)
        self.arcoBP2.setXY(self.arcoAP2.getX() - self.arcoAP2.getWidth()/2 + self.arcoBP2.getWidth()/2, self.arcoAP2.getY())

        self.seatingP1.setXY(0 + self.seatingP1.getWidth()/2, self.screenHeight - self.seatingP1.getHeight() * 0.45)
        self.seatingP2.setXY(self.screenWidth - self.seatingP2.getWidth()/2, self.screenHeight - self.seatingP2.getHeight() * 0.45)

        self.peopleLeft.setXY(0 + self.peopleLeft.getWidth()/2, self.screenHeight * 0.52)
        self.peopleRight.setXY(self.screenWidth - self.peopleLeft.getWidth()/2, self.screenHeight * 0.52)
        self.timerbox.setXY(self.screenWidth / 2, self.screenHeight * 0.075)
        self.scoreleft.setXY(self.screenWidth / 2 - self.timerbox.getWidth()/2 - self.scoreleft.getWidth()/2, self.timerbox.getY())
        self.scoreright.setXY(self.screenWidth / 2 + self.timerbox.getWidth()/2 + self.scoreleft.getWidth()/2, self.timerbox.getY())
        self.avatarframeP1.setXY(self.screenWidth * 0.10, self.screenHeight * 0.09)
        self.avatarframeP2.setXY(self.screenWidth - self.screenWidth * 0.10, self.screenHeight * 0.09)
        self.specialmeterP1.setXY(self.avatarframeP1.getX() + self.avatarframeP1.getWidth() + 30 * self.sc, self.avatarframeP1.getY() * 0.85)
        self.specialmeterP2.setXY(self.avatarframeP2.getX() - self.avatarframeP2.getWidth() - 30 * self.sc, self.avatarframeP2.getY() * 0.85)

        self.cloudLeft.setXY(0 + self.cloudLeft.getWidth()/2, 0 + self.cloudLeft.getHeight()/2)
        self.cloudRight.setXY(self.screenWidth - self.cloudRight.getWidth()/2, 0 + self.cloudRight.getHeight()/2)
        self.cloud01.setXY(self.screenWidth * 0.10, self.screenHeight * 0.03 + self.cloud01.getHeight()/2)
        self.cloud02.setXY(self.screenWidth * 0.65, self.screenHeight * 0.08 + self.cloud02.getHeight()/2)
        self.cloud03.setXY(self.screenWidth * 0.35, self.screenHeight * 0.14 + self.cloud03.getHeight()/2)
        self.cloud01.setVelX(2)
        self.cloud02.setVelX(1.5)
        self.cloud03.setVelX(1)
        self.cloud01.setBoundAction(self.WRAP)
        self.cloud02.setBoundAction(self.WRAP)
        self.cloud03.setBoundAction(self.WRAP)
        self.cloud01.setBounds(0, 0, self.screenWidth, self.screenHeight)
        self.cloud02.setBounds(0, 0, self.screenWidth, self.screenHeight)
        self.cloud03.setBounds(0, 0, self.screenWidth, self.screenHeight)

        posX = self.specialmeterP1.getX() - self.specialmeterP1.getWidth()/2 + 22 * self.sc
        i = 0
        while i < 10:
            self.specialBarP1[i].setXY(posX + (self.specialBarP1[i].getWidth()+4*self.sc) * i, self.specialmeterP1.getY())
            i += 1
        posX = self.specialmeterP2.getX() + self.specialmeterP2.getWidth() / 2 - 22 * self.sc
        i = 0
        while i < 10:
            self.specialBarP2[i].setXY(posX - (self.specialBarP2[i].getWidth()+4*self.sc) * i, self.specialmeterP2.getY())
            i += 1

        #------------FIN-CANCHA--------------------------------------------------------

        self.loadFieldLimits()
        self.loadObjectsArray()

        # Dibujar la imagen cargada en la imagen de fondo del juego.
        Game.inst().setBackground(self.mImg)

    def update(self):
        Stadium.update(self)


        i = 0
        while i < len(self.upperObjects):
            self.upperObjects[i].update()
            i += 1

        i = 0
        while i < len(self.centerObjects):
            self.centerObjects[i].update()
            i += 1

        ParticleManager.inst().update()

    def render(self, p1, p2, disk, aP1, aP2, aScreen):



        i = 0
        while i < len(self.upperObjects):
            self.upperObjects[i].render(aScreen)
            i += 1

        ParticleManager.inst().render(aScreen)
        aP1.render(aScreen)
        aP2.render(aScreen)



        renderOrder = self.depth(disk, p1, p2)
        i = 0
        while i < len(renderOrder):
            renderOrder[i].render(aScreen)
            i += 1

        i = 0
        while i < len(self.centerObjects):
            self.centerObjects[i].render(aScreen)
            i += 1

        i = 0
        while i < len(self.lowerObjects):
            self.lowerObjects[i].render(aScreen)
            i += 1



    def destroy(self):
        Stadium.destroy(self)

    def loadFieldLimits(self):
        self.UpperLimit = Reference()
        self.UpperLimit.setImage(pygame.transform.scale(self.UpperLimit.mImg, (self.borderup.getWidth(), int(self.borderup.getHeight()*0.4))).convert_alpha())
        self.UpperLimit.setXY(self.borderup.getX(), self.borderup.getY() - 20 * self.sc)

        self.LowerLimit = Reference()
        self.LowerLimit.setImage(pygame.transform.scale(self.LowerLimit.mImg, (self.borderdown.getWidth(), int(self.borderdown.getHeight()*0.35))).convert_alpha())
        self.LowerLimit.setXY(self.borderdown.getX(), self.borderdown.getY())

        self.LeftLimit1 = Reference()
        self.LeftLimit1.setRegistration(self.LeftLimit1.TOP_LEFT)
        self.LeftLimit1.setImage(pygame.transform.scale(self.LeftLimit1.mImg, (int(self.arcoBP1.getWidth()*0.35), int(self.arcoBP1.getHeight() * 0.27))).convert_alpha())
        self.LeftLimit1.setXY(self.arcoBP1.getX(), int(self.UpperLimit.getY() - self.UpperLimit.getHeight()/2))

        self.LeftLimit2 = Reference()
        self.LeftLimit2.setRegistration(self.LeftLimit2.TOP_LEFT)
        self.LeftLimit2.setImage(pygame.transform.scale(self.LeftLimit2.mImg, (self.LeftLimit1.getWidth(), int(self.LeftLimit1.getHeight() * 0.94))).convert_alpha())
        self.LeftLimit2.setXY(self.arcoBP1.getX() - 48 * self.sc, int(self.LowerLimit.getY() + self.LowerLimit.getHeight()/2 - self.LeftLimit2.getHeight()))

        self.RightLimit1 = Reference()
        self.RightLimit1.setRegistration(self.RightLimit1.TOP_LEFT)
        self.RightLimit1.setImage(pygame.transform.scale(self.RightLimit1.mImg, (int(self.arcoBP2.getWidth()*0.35), int(self.arcoBP2.getHeight() * 0.27))).convert_alpha())
        self.RightLimit1.setXY(self.arcoBP2.getX() - self.RightLimit1.getWidth(), self.LeftLimit1.getY())

        self.RightLimit2 = Reference()
        self.RightLimit2.setRegistration(self.RightLimit2.TOP_LEFT)
        self.RightLimit2.setImage(pygame.transform.scale(self.RightLimit1.mImg, (self.RightLimit1.getWidth(), self.RightLimit1.getHeight())).convert_alpha())
        self.RightLimit2.setXY(self.arcoBP2.getX() - self.RightLimit1.getWidth() + 48 * self.sc, self.LeftLimit2.getY())

        postW = int(25 * self.sc)
        postH = int(20 * self.sc)
        self.postL1 = Reference(2)
        self.postL1.setRegistration(self.postL1.TOP_LEFT)
        self.postL1.setImage(pygame.transform.scale(self.postL1.mImg, (postW, postH)).convert_alpha())
        self.postL1.setXY(self.LeftLimit1.getX()+self.LeftLimit1.getWidth()/2, self.LeftLimit1.getY()+self.LeftLimit1.getHeight())

        self.postL2 = Reference(2)
        self.postL2.setRegistration(self.postL2.TOP_LEFT)
        self.postL2.setImage(pygame.transform.scale(self.postL2.mImg, (postW, postH)).convert_alpha())
        self.postL2.setXY(self.LeftLimit2.getX()+self.LeftLimit2.getWidth()/2, self.LeftLimit2.getY()-self.postL2.getHeight())

        self.postR1 = Reference(2)
        self.postR1.setRegistration(self.postR1.TOP_LEFT)
        self.postR1.setImage(pygame.transform.scale(self.postR1.mImg, (postW, postH)).convert_alpha())
        self.postR1.setXY(self.RightLimit1.getX(), self.RightLimit1.getY()+self.RightLimit1.getHeight())

        self.postR2 = Reference(2)
        self.postR2.setRegistration(self.postR2.TOP_LEFT)
        self.postR2.setImage(pygame.transform.scale(self.postR2.mImg, (postW, postH)).convert_alpha())
        self.postR2.setXY(self.RightLimit2.getX(), self.RightLimit2.getY() - self.postR2.getHeight())

    def loadObjectsArray(self):

        self.upperObjects.append(self.sun)
        self.upperObjects.append(self.cloud02)
        self.upperObjects.append(self.cloud03)
        self.upperObjects.append(self.cloud01)
        self.upperObjects.append(self.cloudLeft)
        self.upperObjects.append(self.cloudRight)
        self.upperObjects.append(self.sea)
        self.upperObjects.append(self.animatedSeaLeft)
        self.upperObjects.append(self.animatedSeaRight)
        self.upperObjects.append(self.palmsBG)
        self.upperObjects.append(self.arcoAP1)
        self.upperObjects.append(self.arcoAP2)
        self.upperObjects.append(self.flag01)
        self.upperObjects.append(self.flag02)
        self.upperObjects.append(self.borderup)
        self.upperObjects.append(self.middle)


        self.centerObjects.append(self.seatingP1)
        self.centerObjects.append(self.seatingP2)
        self.centerObjects.append(self.peopleLeft)
        self.centerObjects.append(self.peopleRight)
        self.centerObjects.append(self.arcoBP1)
        self.centerObjects.append(self.arcoBP2)


        self.centerObjects.append(self.borderdown)
        self.centerObjects.append(self.palms)


        self.centerObjects.append(self.UpperLimit)
        self.centerObjects.append(self.LowerLimit)
        self.centerObjects.append(self.LeftLimit1)
        self.centerObjects.append(self.LeftLimit2)
        self.centerObjects.append(self.RightLimit1)
        self.centerObjects.append(self.RightLimit2)
        self.centerObjects.append(self.postL1)
        self.centerObjects.append(self.postL2)
        self.centerObjects.append(self.postR1)
        self.centerObjects.append(self.postR2)

        if self.Clima == 2:
            self.lowerObjects.append(self.fxNight)
        self.lowerObjects.append(self.timerbox)
        self.lowerObjects.append(self.scoreleft)
        self.lowerObjects.append(self.scoreright)
        self.lowerObjects.append(self.avatarframeP1)
        self.lowerObjects.append(self.avatarframeP2)
        self.lowerObjects.append(self.specialmeterP1)
        self.lowerObjects.append(self.specialmeterP2)


    def loadObjSimple(self, ruta, archivo, flip=False):
        aux = Sprite()
        aux.setImage(AssetManager.inst().ObjSimple(ruta, archivo, flip))
        return aux
