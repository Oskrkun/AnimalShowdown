# -*- coding: utf-8 -*-


from api.AnimatedSprite import *
from pygame import *
from api.Keyboard import *
from api.GameConstants import *
from api.AudioManager import *
from game.GameData import *


class AssetAnimatedAction(AnimatedSprite):
    # Máquina de estados.
    NORMAL = 0
    PRESSED = 1

    #aRuta1 es la ruta de los frames de la animacion normal aRuta2 son cuando le hacen click se le pasa un ancho y alto a los botones para escalarlos
    def __init__(self, aRuta1,aRuta2,aAncho,aAlto,aName,aDir):

        Sprite.__init__(self)

        # Crear el sonido de Click.
        # self.soundShoot = pygame.mixer.Sound("assets/sounds/placeHolderButtonSounds.wav")

        self.dir = aDir

        self.alto = aAlto
        self.ancho = aAncho
        self.Name = aName

        #cargo el array con la animacion mientras encuentre fotos
        bandera = True
        self.mFramesNormal = []
        i = 0
        while (bandera):
            try:
                tmpImg = pygame.image.load(aRuta1 + str(i) + ".png")
                if self.dir:
                    tmpImg = pygame.transform.flip(tmpImg,True,False)
                # aca controlar el tamaño de las imagenes
                tmpImg = pygame.transform.scale(tmpImg, (self.ancho, self.alto)).convert_alpha()
                self.mFramesNormal.append(tmpImg)
                i = i + 1
            except:
                #si da error es porque no bhay mas fotos para cargar :D
                bandera = False

        # Cargar la secuencia de imágenes del Click
        bandera = True
        self.mFramesPressed = []
        i = 0
        while (bandera):
            try:
                tmpImg = pygame.image.load(aRuta2 + str(i) + ".png")
                if self.dir:
                    tmpImg = pygame.transform.flip(tmpImg,True,False)
                # aca controlar el tamaño de las imagenes
                tmpImg = pygame.transform.scale(tmpImg, (self.ancho, self.alto)).convert_alpha()
                self.mFramesPressed.append(tmpImg)
                i = i + 1
            except:
                #si da error es porque no bhay mas fotos para cargar :D
                bandera = False

        #tamaño de los botones
        self.mWidth = self.mFramesNormal[0].get_width()
        self.mHeight = self.mFramesNormal[0].get_height()

        # Estado inicial.
        self.mState = AssetAnimatedAction.NORMAL
        self.setState(AssetAnimatedAction.NORMAL)

    def update(self):

        if self.getState() == AssetAnimatedAction.NORMAL:
            pass
            #aca si le hacen click paso a estado PRESSED
            #y pongo el sonido del click
        elif self.getState() == AssetAnimatedAction.PRESSED:
            if self.isEnded():
                self.setState(AssetAnimatedAction.NORMAL)
            #aca si se levanto el click paso a estado NORMAL

        AnimatedSprite.update(self)


    def render(self, aScreen):
        AnimatedSprite.render(self, aScreen)

    # Establece el estado actual e inicializa las variables correspondientes
    # al estado.
    def setState(self, aState):
        AnimatedSprite.setState(self, aState)
        self.setVisible(True)

        #Cuando le hacen click
        if self.getState() == AssetAnimatedAction.PRESSED:
            self.initAnimation(self.mFramesPressed, 0,len(self.mFramesNormal) -1, 2, False)
        elif (self.getState() == AssetAnimatedAction.NORMAL):
            self.initAnimation(self.mFramesNormal, 0,len(self.mFramesPressed) -1, 2, True)
            #el array de frames que se va a reproducir donde empieza el delay si es ciclico o no alto y ancho

    # def click(self):
    #     if self.getState()

    def destroy(self):
        AnimatedSprite.destroy(self)

        i = len(self.mFramesNormal)
        while i > 0:
            self.mFramesNormal[i - 1] = None
            self.mFramesNormal.pop(i - 1)
            i = i - 1

        i = len(self.mFramesPressed)
        while i > 0:
            self.mFramesPressed[i - 1] = None
        self.mFramesPressed.pop(i - 1)
        i = i - 1