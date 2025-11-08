from pico2d import *
from sdl2 import *

import game_world
import game_framework

def _point_in_bb(px, py, bb):
    l, b, r, t = bb
    return l <= px <= r and b <= py <= t

class Gun:
    image = None

    def __init__(self,world):
        self.x, self.y=400,60
        self.frame=0
        self.recoil_timer=0.0
        self.recoil_duration=0.12
        self.world=world
        if Gun.image is None:
            try:
                Gun.image = load_image('gun.png')
            except Exception:
                Gun.image = None

    def update(self):
        if self.recoil_timer > 0.0:
            self.recoil_timer -= game_framework.frame_time
            if self.recoil_timer < 0.0:
                self.recoil_timer = 0.0

    def handle_event(self, event):
        if event.type == SDL_MOUSEMOTION:
            self.x = event.x
            self.y = get_canvas_height() - event.y
        elif event.type == SDL_MOUSEBUTTONDOWN:
            if getattr(event, 'button', None) == 1:
                self.fire()

    def draw(self):
        offset_y=6 if self.recoil_timer > 0.0 else 0
        if Gun.image:
            Gun.image.draw(self.x, self.y)
        else:
            w, h = 40, 20
            draw_rectangle(self.x - w // 2, self.y - h // 2, self.x + w // 2, self.y + h // 2)


def fire(self):
    self.recoil_timer = self.recoil_duration
    # 총알 발사 효과음 재생 (효과음 파일이 있다고 가정)

    # 충돌 검사
    duck_layer = game_world.world[1]  # 오리들이 있는 레이어

    for i in list(duck_layer):
        if hasattr(i,'get_bb'):
            bb=i.get_bb()
            if _point_in_bb(self.x, self.y, bb):
                game_world.remove_object(i)
                break  # 한 번에 하나의 오리만 맞출 수 있도록