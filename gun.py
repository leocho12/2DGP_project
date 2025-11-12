from pico2d import *
from sdl2 import *

import game_world
import game_framework

def _point_in_bb(px, py, bb):
    l, b, r, t = bb
    return l <= px <= r and b <= py <= t

class Gun:
    bullet_image = None
    image = None

    def __init__(self,world=None):
        self.recoil_scale =0.9  # 반동 시 축소 비율
        self.world = world
        self.x, self.y=400,60
        self.frame=0
        self.recoil_timer=0.0
        self.recoil_duration=0.12
        self.world=world
        #재장전 변수
        self.max_ammo=3
        self.ammo=self.max_ammo
        self.reloading=False
        self.reloading_duration=1.5
        self.reload_timer=0.0
        # 데미지
        self.damage=1

        if Gun.image is None:
            try:
                Gun.image = load_image('gun.png')
            except Exception:
                Gun.image = None

        if Gun.bullet_image is None:
            try:
                Gun.bullet_image = load_image('bullet.png')
            except Exception:
                Gun.bullet_image = None

    def update(self):
        # 반동 타이머
        if self.recoil_timer > 0.0:
            self.recoil_timer -= game_framework.frame_time
            if self.recoil_timer < 0.0:
                self.recoil_timer = 0.0

        # 재장전 타이머
        if self.reloading:
            self.reload_timer -= game_framework.frame_time
            if self.reload_timer <= 0.0:
                self.reloading = False
                self.reload_timer = 0.0
                self.ammo = self.max_ammo


    def handle_event(self, event):
        # 마우스 이돌
        if event.type == SDL_MOUSEMOTION:
            self.x = event.x
            self.y = get_canvas_height() - event.y
        # 발사
        elif event.type == SDL_MOUSEBUTTONDOWN:
            # left button usually == 1
            if getattr(event, 'button', None) == 1:
                self.fire()
        # 수동 재장전
        elif event.type == SDL_KEYDOWN:
            if getattr(event, 'key', None) == SDLK_r:
                self.start_reload()

    def draw(self):
        # 반동
        if self.recoil_timer > 0.0 and self.recoil_duration > 0.0:
            t = self.recoil_timer / self.recoil_duration  # 0..1
            scale = self.recoil_scale + (1.0 - self.recoil_scale) * (1.0 - t)
        else:
            scale = 1.0
        # 총
        if Gun.image:
            iw = getattr(Gun.image, 'w', 40)
            ih = getattr(Gun.image, 'h', 20)
            Gun.image.draw(self.x, self.y, iw * scale, ih * scale)
        else:
            base_w, base_h = 40, 20
            w = base_w * scale
            h = base_h * scale
            draw_rectangle(self.x - w // 2, self.y - h // 2, self.x + w // 2, self.y + h // 2)

        # 잔탄
        base_x = 40
        base_y = get_canvas_height() - 30
        box_w = 18
        box_h = 12
        gap = 6

        if self.reloading:
            # 경과 시간 계산
            elapsed = self.reloading_duration - self.reload_timer
            # 각 총알이 채워지는 시간 간격
            time_per_bullet = self.reloading_duration / self.max_ammo
            # 현재까지 채워진 총알 수
            bullets_loaded = int(elapsed / time_per_bullet)
            bullets_loaded = min(bullets_loaded, self.max_ammo)
        else:
            bullets_loaded=self.ammo

        for i in range(self.max_ammo):
            bx = base_x + i * (box_w + gap)
            by = base_y

            # 채워진 슬롯이면 총알 이미지 표시
            if i < bullets_loaded:
                if Gun.bullet_image:
                    Gun.bullet_image.draw(bx, by, box_w - 4, box_h - 4)
                else:
                    # 이미지 없을 경우 채워진 사각형으로 대체
                    draw_rectangle(bx - (box_w // 2 - 2), by - (box_h // 2 - 2),
                                   bx + (box_w // 2 - 2), by + (box_h // 2 - 2))
            else:
                # 빈 슬롯은 테두리만 보여줌 (기존 동작 유지)
                pass
        if self.reloading:
            # draw a larger outline around boxes to indicate reloading
            draw_rectangle(base_x - 12, base_y - 16, base_x + (box_w + gap) * self.max_ammo - gap + 12, base_y + 16)

    # 발사 함수
    def fire(self):

        # 장전중 발사 금지
        if self.reloading:
            return
        # 잔탄 없으면 자동 재장전
        if self.ammo<=0:
            self.start_reload()
            return
        # 잔탄 감소
        self.recoil_timer = self.recoil_duration
        self.ammo-=1

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
                    # 오리 피격 처리
                    if hasattr(i,'take_damage'):
                        dead=i.take_damage(self.damage)
                        if dead:
                            game_world.remove_object(i)
                    else:
                        game_world.remove_object(i)
                    break  # 한 번에 하나의 오리만 맞출 수 있도록

    # 재장전 함수
    def start_reload(self):
        if not self.reloading and self.ammo < self.max_ammo:
            self.reloading = True
            self.reload_timer = self.reloading_duration