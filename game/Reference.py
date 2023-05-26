from api.Sprite import *
from api.GameConstants import *


class Reference(Sprite):

    def __init__(self, color=1):
        Sprite.__init__(self)

        if color == 1:
            self.mImg = pygame.image.load("assets/images/References/limit.png")
        elif color == 2:
            self.mImg = pygame.image.load("assets/images/References/post.png")
        elif color == 3:
            self.mImg = pygame.image.load("assets/images/References/body.png")
        self.show = False

    def update(self):
        Sprite.update(self)

    def destroy(self):
        Sprite.destroy(self)

    def render(self, aScreen):
        if GameConstants.inst().SHOW_REF or self.show:
            Sprite.render(self, aScreen)
