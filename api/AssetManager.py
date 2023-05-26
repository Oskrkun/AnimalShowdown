import pygame
from api.GameConstants import *


class AssetManager(object):
    mInstance = None
    mInitialized = False

    ARRAYS = []

    Basics = []
    Pointer = []
    Menu = []
    Background = []
    Frame = []
    Coin = []

    Stadiums = []
    Disks = []

    MenuButtons = []

    Avatars = []
    Characters = []
    Powers = []
    PowerParticles = []
    Monkey = []
    Toucan = []

    def __new__(self, *args, **kargs):
        if (AssetManager.mInstance is None):
            AssetManager.mInstance = object.__new__(self, *args, **kargs)
            self.init(AssetManager.mInstance)
        return self.mInstance

    @classmethod
    def inst(cls):
        if (not cls.mInstance):
            return cls()
        return cls.mInstance

    def init(self):
        self.ARRAYS.append(self.Basics)
        self.ARRAYS.append(self.Pointer)
        self.ARRAYS.append(self.Menu)
        self.ARRAYS.append(self.Background)
        self.ARRAYS.append(self.Frame)
        self.ARRAYS.append(self.Coin)
        self.ARRAYS.append(self.Stadiums)
        self.ARRAYS.append(self.Disks)
        self.ARRAYS.append(self.Avatars)
        self.ARRAYS.append(self.MenuButtons)
        self.ARRAYS.append(self.Characters)
        self.ARRAYS.append(self.Powers)
        self.ARRAYS.append(self.Monkey)
        self.ARRAYS.append(self.Toucan)

        esc = GameConstants.inst().SCALE
        self.Basics.append(0)  # 0 es el ID del array de los elementos basicos del juego
        ruta = "assets/images/Basics/"

        self.Basics.append(self.Pointer)  # 1 en Basics es el pointer
        self.Pointer.append(self.loadAssets(ruta, "pointer_0_", esc * 1))
        self.Pointer.append(self.loadAssets(ruta, "pointer_1_", esc * 1))

        self.Basics.append(self.Menu)  # 3 en Basics son los menu
        self.Menu = self.loadAssets(ruta, "menu", 1)
        self.Basics.append(self.Background)  # 4 en Basics son los fondos
        self.Background = self.loadAssetsExt(ruta, "background", 1, ".jpg", False)
        self.Coin = self.loadAssets(ruta, "/Coin/coin_", esc * 1)

        self.Characters.append(5)  # 5 es el ID del array de characters
        self.loadCharacter("monkey")  # Load Monkey
        self.loadCharacter("toucan")  # Load Toucan

        self.Powers.append([])
        self.Powers.append([])
        self.Powers.append([])
        # [Player/Side][Power]
        self.Powers[1].append("Player 1 powers")
        self.Powers[1].append(self.loadAssets("assets/images/Characters/monkey/POWER/ObjectPower/", "fireball_", esc * 1))
        self.Powers[1].append(self.loadAssets("assets/images/Characters/toucan/POWER/ObjectPower/", "twister_", esc * 4))
        self.Powers[2].append("Player 2 powers")
        self.Powers[2].append(self.loadAssets("assets/images/Characters/monkey/POWER/ObjectPower/", "fireball_", esc * 1, True))
        self.Powers[2].append(self.loadAssets("assets/images/Characters/toucan/POWER/ObjectPower/", "twister_", esc * 4, True))

        self.PowerParticles.append([])
        self.PowerParticles.append([])
        self.PowerParticles.append([])
        # [Player/Side][Power]
        self.PowerParticles[1].append("Player 1 power particles")
        self.PowerParticles[1].append(self.loadAssets("assets/images/Characters/monkey/POWER/ObjectPower/particles/", "particles_", esc * 1))
        self.PowerParticles[1].append("El tucan no tiene particulas de poder")
        self.PowerParticles[2].append("Player 2 power particles")
        self.PowerParticles[2].append(self.loadAssets("assets/images/Characters/monkey/POWER/ObjectPower/particles/", "particles_", esc * 1, True))
        self.PowerParticles[2].append("El tucan no tiene particulas de poder")

        ruta = "assets/images/Stadium/"
        self.Stadiums.append(self.loadAssets(ruta, "Stadium_0_", 0.3))
        self.Stadiums.append(self.loadAssets(ruta, "Stadium_1_", 5))
        self.Stadiums.append(self.loadAssets(ruta, "Stadium_2_", 5))
        self.Stadiums.append(self.loadAssets(ruta, "Stadium_3_", 0.3))

        ruta = "assets/images/Disk/"
        self.Disks.append(self.loadAssets(ruta, "Disk_00_", esc))

        ruta = "assets/images/HUD/avatars/"
        self.Avatars.append([])
        self.Avatars[0].append(self.loadAssets(ruta, "avatar_00_", esc))
        self.Avatars[0].append(self.loadAssets(ruta, "avatar_01_", esc, True))
        self.Avatars[0].append(self.loadAssets(ruta, "avatar_02_", esc))

        self.Avatars.append([])
        self.Avatars.append([])
        # [Player/Side][ID_Character]
        self.Avatars[1].append("")
        self.Avatars[1].append(self.loadAssets(ruta, "avatar_01_", esc))
        self.Avatars[1].append(self.loadAssets(ruta, "avatar_02_", esc))
        self.Avatars[2].append("")
        self.Avatars[2].append(self.loadAssets(ruta, "avatar_01_", esc, True))
        self.Avatars[2].append(self.loadAssets(ruta, "avatar_02_", esc, True))

        ruta = "assets/images/HUD/EndMenu/"
        self.MenuButtons.append(self.loadAssets(ruta, "resume_", esc))
        self.MenuButtons.append(self.loadAssets(ruta, "rematch_", esc))
        self.MenuButtons.append(self.loadAssets(ruta, "selectscreen_", esc))
        self.MenuButtons.append(self.loadAssets(ruta, "settings_", esc))
        self.MenuButtons.append(self.loadAssets(ruta, "mainmenu_", esc))

    def loadCharacter(self, name):
        ruta = "assets/images/Characters/" + str(name) + "/"
        file = str(name)
        esc = GameConstants.inst().SCALE
        char = []

        # [Player/Side][State][Animation]
        char.append([])  # Posicion [0]: Array relleno
        char.append([])  # Posicion [1]: Array player 1
        char.append([])  # Posicion [2]: Array player 2

        # PLAYER 1
        char[1].append([])  # Posicion [1][0]: Array de animaciones NORMAL
        char[1].append([])  # Posicion [1][1]: Array de animaciones HOLD
        char[1].append([])  # Posicion [1][2]: Array de animaciones THROW
        char[1].append([])  # Posicion [1][3]: Array de animaciones DASH
        char[1].append([])  # Posicion [1][4]: Array de animaciones STUN
        char[1].append([])  # Posicion [1][5]: Array de animaciones CHEER
        char[1].append([])  # Posicion [1][6]: Array de animaciones POWER
        char[1][0].append(self.loadAssets(ruta+"NORMAL/", file + "_00_", esc, False))  # [1][0][0]: Parado
        char[1][0].append(self.loadAssets(ruta+"NORMAL/", file + "_01_", esc, True))   # [1][0][1]: Movimiento LEFT
        char[1][0].append(self.loadAssets(ruta+"NORMAL/", file + "_01_", esc, False))  # [1][0][2]: Movimiento RIGHT
        char[1][0].append(self.loadAssets(ruta+"NORMAL/", file + "_01_", esc, False))  # [1][0][3]: Movimiento UP
        char[1][0].append(self.loadAssets(ruta+"NORMAL/", file + "_01_", esc, False))  # [1][0][4]: Movimiento DOWN
        char[1][1].append(self.loadAssets(ruta+"HOLD/", file + "_10_", esc, False))    # [1][1][0]: HOLD
        char[1][1].append(self.loadAssets(ruta+"HOLD/", file + "_11_", esc, True))     # [1][1][1]: Movimiento LEFT
        char[1][1].append(self.loadAssets(ruta+"HOLD/", file + "_11_", esc, False))    # [1][1][2]: Movimiento RIGHT
        char[1][1].append(self.loadAssets(ruta+"HOLD/", file + "_11_", esc, False))    # [1][1][3]: Movimiento UP
        char[1][1].append(self.loadAssets(ruta+"HOLD/", file + "_11_", esc, False))    # [1][1][4]: Movimiento DOWN
        char[1][2].append(self.loadAssets(ruta+"THROW/", file + "_20_", esc, False))   # [1][2][0]: THROW Parado
        char[1][2].append(self.loadAssets(ruta+"THROW/", file + "_20_", esc, True))    # [1][2][1]: THROW LEFT
        char[1][2].append(self.loadAssets(ruta+"THROW/", file + "_20_", esc, False))   # [1][2][2]: THROW RIGHT
        char[1][2].append(self.loadAssets(ruta+"THROW/", file + "_20_", esc, True))    # [1][2][1]: THROW LEFT
        char[1][3].append(self.loadAssets(ruta +"DASH/", file + "_30_", esc, False))  # [1][3][1]: DASH
        char[1][4].append(self.loadAssets(ruta+"STUN/", file + "_40_", esc, False))     # [1][2][1]: STUN
        char[1][6].append(self.loadAssets(ruta+"POWER/", file + "_60_", esc, False))   # [1][6][0]: POWER

        # PLAYER 2
        char[2].append([])  # Posicion [2][0]: Array de animaciones NORMAL
        char[2].append([])  # Posicion [2][1]: Array de animaciones HOLD
        char[2].append([])  # Posicion [2][2]: Array de animaciones THROW
        char[2].append([])  # Posicion [2][3]: Array de animaciones DASH
        char[2].append([])  # Posicion [2][4]: Array de animaciones STUN
        char[2].append([])  # Posicion [2][5]: Array de animaciones CHEER
        char[2].append([])  # Posicion [2][6]: Array de animaciones POWER
        char[2][0].append(self.loadAssets(ruta+"NORMAL/", file + "_00_", esc, True))   # [2][0][0]: Parado
        char[2][0].append(self.loadAssets(ruta+"NORMAL/", file + "_01_", esc, True))   # [2][0][1]: Movimiento LEFT
        char[2][0].append(self.loadAssets(ruta+"NORMAL/", file + "_01_", esc, False))  # [2][0][2]: Movimiento RIGHT
        char[2][0].append(self.loadAssets(ruta+"NORMAL/", file + "_01_", esc, True))   # [2][0][3]: Movimiento UP
        char[2][0].append(self.loadAssets(ruta+"NORMAL/", file + "_01_", esc, True))   # [2][0][4]: Movimiento DOWN
        char[2][1].append(self.loadAssets(ruta+"HOLD/", file + "_10_", esc, True))     # [2][1][0]: HOLD
        char[2][1].append(self.loadAssets(ruta+"HOLD/", file + "_11_", esc, True))     # [2][1][1]: Movimiento LEFT
        char[2][1].append(self.loadAssets(ruta+"HOLD/", file + "_11_", esc, False))    # [2][1][2]: Movimiento RIGHT
        char[2][1].append(self.loadAssets(ruta+"HOLD/", file + "_11_", esc, True))     # [2][1][3]: Movimiento UP
        char[2][1].append(self.loadAssets(ruta+"HOLD/", file + "_11_", esc, True))     # [2][1][4]: Movimiento DOWN
        char[2][2].append(self.loadAssets(ruta+"THROW/", file + "_20_", esc, True))    # [2][2][0]: THROW Parado
        char[2][2].append(self.loadAssets(ruta+"THROW/", file + "_20_", esc, True))    # [2][2][1]: THROW LEFT
        char[2][2].append(self.loadAssets(ruta+"THROW/", file + "_20_", esc, False))   # [2][2][2]: THROW RIGHT
        char[2][3].append(self.loadAssets(ruta+ "DASH/", file + "_30_", esc, True))  # [2][3][1]: DASH
        char[2][4].append(self.loadAssets(ruta+"STUN/", file + "_40_", esc, True))     # [2][2][4]: STUN
        char[2][6].append(self.loadAssets(ruta+"POWER/", file + "_60_", esc, True))    # [2][6][0]: POWER

        self.Characters.append(char)

    def loadAssets(self, ruta, nomFiles, aEscala=1, flip=False):
        return self.loadAssetsExt(ruta, nomFiles, aEscala, ".png", flip)

    def loadAssetsExt(self, ruta, nomFiles, aEscala, ext, flip=False):
        # cargo el array con la animacion mientras encuentre imagenes
        bandera = True
        array = []

        i = 0
        while (bandera):
            try:
                if i < 10:  # Solo si hay menos de 9 imagenes hay que colocar un 0 delante
                    num = "0" + str(i)
                else:
                    num = str(i)
                tmpImg = pygame.image.load(ruta + nomFiles + num + ext)
                if not flip:
                    tmpImg = pygame.transform.scale(tmpImg, (int(tmpImg.get_width() * aEscala), int(tmpImg.get_height() * aEscala))).convert_alpha()
                else:
                    tmpImg = pygame.transform.scale(tmpImg, (int(tmpImg.get_width() * aEscala), int(tmpImg.get_height() * aEscala)))
                    tmpImg = pygame.transform.flip(tmpImg, True, False).convert_alpha()
                array.append(tmpImg)
                i += 1
            except:
                if i == 0:
                    print("No se han podido cargar los assets: " + nomFiles + " > " + ruta + nomFiles + num + ext)
                bandera = False
        return array

    def loadAssetsSized(self, ruta, nomFiles, sW, sH):
        # cargo el array con la animacion mientras encuentre imagenes
        bandera = True
        array = []

        i = 0
        while (bandera):
            try:
                if i < 10:  # Solo si hay menos de 9 imagenes hay que colocar un 0 delante
                    num = "0" + str(i)
                else:
                    num = str(i)
                tmpImg = pygame.image.load(ruta + nomFiles + num + ".png")
                tmpImg = pygame.transform.scale(tmpImg, (sW, sH)).convert_alpha()
                array.append(tmpImg)
                i += 1
            except:
                if i == 0:
                    print("No se han podido cargar los assets: " + nomFiles + " > " + ruta + nomFiles + num + ext)
                bandera = False
        return array

    def loadAssetsSet(self, ruta, frames):
        esc = GameConstants.inst().SCALE
        array = []
        i = 0
        while i <= len(frames)-1:
            tmpImg = pygame.image.load(ruta + frames[i] + ".png")
            tmpImg = pygame.transform.scale(tmpImg, (int(tmpImg.get_width() * esc), int(tmpImg.get_height() * esc))).convert_alpha()
            array.append(tmpImg)
            i += 1
        return array

    def ObjSimple(self, ruta, archivo, flip=False):
        esc = GameConstants.inst().SCALE
        tmpImg = None
        try:
            tmpImg = pygame.image.load("assets/images/" + ruta + archivo)
            if not flip:
                tmpImg = pygame.transform.scale(tmpImg, (int(tmpImg.get_width() * esc), int(tmpImg.get_height() * esc))).convert_alpha()
            else:
                tmpImg = pygame.transform.scale(tmpImg, (int(tmpImg.get_width() * esc), int(tmpImg.get_height() * esc)))
                tmpImg = pygame.transform.flip(tmpImg, True, False).convert_alpha()
        except:
            print("No se han podido cargar el asset: " + archivo)
        return tmpImg

    def getCharAssets(self, ID):
        return self.Characters[ID]

    def destroy(self):
        i = len(self.ARRAYS)
        while i >= 0:
            self.ARRAYS[i - 1].destroy()
            self.ARRAYS.pop(i - 1)
            i -= 1

