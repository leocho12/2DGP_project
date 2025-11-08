from pico2d import *
from sdl2 import *

import game_world
import game_framework

def _point_in_bb(px, py, bb):
    l, b, r, t = bb
    return l <= px <= r and b <= py <= t

class Gun:
    image = None

    def __init__(self,world=None):
        self.recoil_scale =0.9  # 반동 시 축소 비율
        self.world = world
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
        # 반동이 남아있으면 스케일을 작게 적용하고 시간이 지나며 원래 크기로 복원
        if self.recoil_timer > 0.0 and self.recoil_duration > 0.0:
            t = self.recoil_timer / self.recoil_duration  # 0..1
            # 남은 시간 비율에 따라 스케일을 보간 (발사직후 작고 천천히 1.0으로)
            scale = self.recoil_scale + (1.0 - self.recoil_scale) * (1.0 - t)
        else:
            scale = 1.0

        if Gun.image:
            iw = getattr(Gun.image, 'w', 40)
            ih = getattr(Gun.image, 'h', 20)
            Gun.image.draw(self.x, self.y, iw * scale, ih * scale)
        else:
            base_w, base_h = 40, 20
            w = base_w * scale
            h = base_h * scale
            draw_rectangle(self.x - w // 2, self.y - h // 2, self.x + w // 2, self.y + h // 2)

    def fire(self):
        self.recoil_timer = self.recoil_duration
        # 총알 발사 효과음 재생 (효과음 파일이 있다고 가정)

        # 충돌 검사
        try:
            duck_layer = game_world.world[1]
        except Exception:
            duck_layer = []

        for i in list(duck_layer):
            if hasattr(i,'get_bb'):
                bb=i.get_bb()
                if _point_in_bb(self.x, self.y, bb):
                    game_world.remove_object(i)
                    break  # 한 번에 하나의 오리만 맞출 수 있도록