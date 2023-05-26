from api.GameConstants import *

class Console(object):
    mInstance = None
    mInitialized = False

    def __new__(self, *args, **kargs):
        if (Console.mInstance is None):
            Console.mInstance = object.__new__(self, *args, **kargs)
            self.init(Console.mInstance)
        return self.mInstance

    @classmethod
    def inst(cls):
        if (not cls.mInstance):
            return cls()
        return cls.mInstance

    def init(self):
        print("ANIMAL JAMMERS")
        print("Resolution: " + str(GameConstants.inst().SCREEN_WIDTH) + " x " + str(GameConstants.inst().SCREEN_HEIGHT))
        print ("")
        print ("////////////////////////////////")
        print ("")

    def printLine(self, array):
        print(str(array[0]) + ": " + str(array[1]))

    def printVars(self, array):
        print ("")
        print ("----------------------------")
        i = 0
        while i < len(array):
            print(str(array[i]) + ": " + str(array[i+1]))
            i += 2

    def printHighlight(self, array):
        print ("")
        print ("////////////////////////////////")
        print ("")
        i = 0
        while i < len(array):
            print(str(array[i]).upper() + ": " + str(array[i+1]))
            i += 2
