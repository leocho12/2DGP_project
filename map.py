from pico2d import load_image, get_canvas_width, get_canvas_height


class Map:
    def __init__(self):
        self.image = load_image('Theme_02_L130_Hill_01.png')
        self.cw=get_canvas_width()
        self.ch=get_canvas_height()
        self.w=self.cw
        self.h=200


    def draw(self):
        self.image.draw(self.cw//2, self.h//2, self.w, self.h)

    def update(self):
        pass
