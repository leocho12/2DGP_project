from pico2d import *
from sdl2 import *

import game_world
import game_framework

class Gun:
    image = None

    def __init__(self,world):
        self.x, self.y=400,60
        self.frame=0
        if Gun.image is None:
            try:
                self.image=load_image('gun.png')

    def update(self):
        pass

    def handle_event(self, event):
        if event.type == SDL_MOUSEMOTION:
            self.x = event.x
            self.y = get_canvas_height() - event.y
        elif event.type == SDL_MOUSEBUTTONDOWN:
            if getattr(event, 'button', None) == 1:
                self.fire()

    def draw(self):
    if Gun.image:
        Gun.image.draw(self.x, self.y)
    else:
        w, h = 40, 20
        draw_rectangle(self.x - w // 2, self.y - h // 2, self.x + w // 2, self.y + h // 2)


def fire(self):
    from gun import Bullet as _Bullet  # 같은 파일 안에 있을 경우 안전 호출(혹은 위에서 직접 사용)
    bullet = _Bullet(self.x, self.y + 20)
    game_world.add_object(bullet, 2)