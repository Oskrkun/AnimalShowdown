# -*- coding: utf-8 -*-

import pygame
from api.Game import *

class AudioManager(object):

    mInstance = None
    mInitialized = False

    mChannels = 8

    def __new__(self, *args, **kargs):
        if (AudioManager.mInstance is None):
            AudioManager.mInstance = object.__new__(self, *args, **kargs)
            self.init(AudioManager.mInstance)
        else:
            print ("Cuidado: AudioManager(): No se debería instanciar más de una vez esta clase. Usar AudioManager.inst().")
        return AudioManager.mInstance

    @classmethod
    def inst(cls):
        if (not cls.mInstance):
            return cls()
        return cls.mInstance
    
    def init(self):
        if (AudioManager.mInitialized):
            return
        AudioManager.mInitialized = True

        self.audios = []
        self.inGameSounds = []
        self.inMenuSounds = []
        self.inSelectionSounds = []

        self.audios.append(self.inGameSounds)
        self.audios.append(self.inMenuSounds)
        self.audios.append(self.inSelectionSounds)

        self.muted = False

        try:
            AudioManager.mChannels = pygame.mixer.get_num_channels()
            """------------SOUNDS MATCH--------------------------------------"""
            self.goalSound = pygame.mixer.Sound("assets/sounds/goal.wav")
            self.goalSoundInit = False
            self.startMatchSound = pygame.mixer.Sound("assets/sounds/start.wav")
            self.startMatchSound.set_volume(0.7)
            self.startMatchSoundInit = False
            self.inGameSounds.append(self.goalSound)
            self.inGameSounds.append(self.startMatchSound)
            """--------------------------------------------------------------"""

            """------------SOUNDS MENU---------------------------------------"""
            self.menuMoveOptions = pygame.mixer.Sound("assets/sounds/moveMenus.wav")
            self.menuMoveOptionsInit = False
            self.menuMusic = pygame.mixer.Sound("assets/sounds/menuMusic.wav")
            self.menuMusic.set_volume(0.7)
            self.menuMusicInit = False
            self.menuConfirmations = pygame.mixer.Sound("assets/sounds/confirmOption.wav")
            self.menuConfirmationsInit = False
            self.inMenuSounds.append(self.menuMoveOptions)
            self.inMenuSounds.append(self.menuMusic)
            self.inMenuSounds.append(self.menuConfirmations)
            """--------------------------------------------------------------"""

            """------------SOUNDS SELECTION----------------------------------"""
            self.selectionConfirm = pygame.mixer.Sound("assets/sounds/confirmCharacter.wav")
            self.selectionConfirmInit = False
            self.selectionStage = pygame.mixer.Sound("assets/sounds/selectionStage.wav")
            self.selectionStageInit = False
            self.inSelectionSounds.append(self.selectionConfirm)
            self.inSelectionSounds.append(self.selectionStage)

            """--------------------------------------------------------------"""
        except:
            pass

    def update(self):
        from api.Game import Game

        if (Game.inst().getState().__class__.__name__ == "MatchManager") and not self.muted:
            if not self.startMatchSoundInit:
                self.startMatchSoundInit = True
                AudioManager.inst().playStart()
                AudioManager.inst().muteInMenuSounds()
                AudioManager.inst().muteInSelectionSounds()
        elif (Game.inst().getState().__class__.__name__ == "MenuState") and not self.muted:
            if not self.menuMusicInit:
                self.menuMusicInit = True
                AudioManager.inst().playMenu()
                AudioManager.inst().muteInGameSounds()
                AudioManager.inst().muteInSelectionSounds()
        elif (Game.inst().getState().__class__.__name__ == "LvConfiguration") and not self.muted:
            if not self.selectionStageInit:
                self.selectionStageInit = True
                AudioManager.inst().playSelectionStage()
                AudioManager.inst().muteInGameSounds()
                AudioManager.inst().muteInMenuSounds()
        
    def play(self, aSound, loop = 0):
        AudioManager.inst().get_channel().play(aSound, loop)

    def mute(self):
        for e in self.audios:
            for i in e:
                i.stop()

        self.startMatchSoundInit = False
        self.menuMusicInit = False
        self.selectionStageInit = False

    def playORmute(self, var):
        self.muted = var
        if self.muted:
            AudioManager.inst().mute()

    def muteInGameSounds(self):
        for e in self.inGameSounds:
            e.stop()

    def muteInMenuSounds(self):
        for e in self.inMenuSounds:
            e.stop()
        self.menuMusicInit = self.muted

    def playGoal(self):
        if not self.muted:
            self.play(self.goalSound)

    def playMoveOption(self):
        if not self.muted:
            self.play(self.menuMoveOptions)

    def playConfirmOption(self):
        if not self.muted:
            self.play(self.menuConfirmations)

    def playConfirmCharacter(self):
        if not self.muted:
            self.play(self.selectionConfirm)

    def playStart(self):
        if not self.muted:
            self.play(self.startMatchSound)

    def playMenu(self):
        if not self.muted:
            self.play(self.menuMusic, -1)

    def playSelectionStage(self):
        if not self.muted:
            self.play(self.selectionStage, -1)

    def muteInSelectionSounds(self):
        for e in self.inSelectionSounds:
            e.stop()
        self.selectionStageInit = self.muted

    def get_channel(self):
        c = pygame.mixer.find_channel(True)
        while c is None:
            AudioManager.mChannels += 1
            pygame.mixer.set_num_channels(AudioManager.mChannels)
            c = pygame.mixer.find_channel()
        return c
    
    def destroy(self):
        AudioManager.mInstance = None
