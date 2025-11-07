from pico2d import load_image

class Map:
    def __init__(self):
        self.image = load_image('Theme_02_L130_Hill_01.png')

    def draw(self):
        self.image.draw(400, 300)

    def update(self):
        pass
