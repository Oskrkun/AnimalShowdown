# -*- coding: utf-8 -*-

import pygame
from api.Keyboard import *
from api.Game import *
from api.GameState import *
from api.TextSprite import *
from game.states.LvConfiguration import *
from api.AssetAnimatedAction import *
from api.AssetAnimated import *


class Configuration(GameState):
    def __init__(self):
        GameState.__init__(self)

    def init(self):
        GameState.init(self)

        self.screenWidth = GameConstants.inst().SCREEN_WIDTH
        self.screenHeight = GameConstants.inst().SCREEN_HEIGHT

        self.x = 0
        self.contador = 0

        # Cargar la imagen del fondo. La imagen es de 800x600 al igual que la pantalla.
        self.mImg = AssetManager.inst().Background[0]

        # Dibujar la imagen cargada en la imagen de fondo del juego.
        Game.inst().setBackground(self.mImg)


    def update(self):
        GameState.update(self)

    def render(self):
        GameState.render(self)
        screen = Game.inst().getScreen()

    def destroy(self):
        GameState.destroy(self)