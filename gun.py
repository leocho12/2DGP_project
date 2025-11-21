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

        # 플레이어 체력
        self.max_hp = 5
        self.hp = self.max_hp

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

        # 플레이어 HP 표시 (오른쪽에 작은 박스들)
        hp_box_w = 12
        hp_box_h = 12
        hp_base_x = base_x + (box_w + gap) * self.max_ammo + 20
        hp_base_y = base_y
        for i in range(self.max_hp):
            hx = hp_base_x + i * (hp_box_w + 4)
            hy = hp_base_y
            # 체력이 남아있으면 테두리로 표시 (이미지 없음)
            draw_rectangle(hx - hp_box_w//2, hy - hp_box_h//2, hx + hp_box_w//2, hy + hp_box_h//2)
            # 체력이 남은 슬롯은 내부를 채운 것처럼 보이게 작은 추가 사각형을 그림
            if i < self.hp:
                inner = 3
                draw_rectangle(hx - hp_box_w//2 + inner, hy - hp_box_h//2 + inner,
                               hx + hp_box_w//2 - inner, hy + hp_box_h//2 - inner)

    # 발사 함수
    def fire(self):
        # 장전중 발사 금지
        if self.reloading:
            return
        # 잔탄 없으면 자동 재장전
        if self.ammo <= 0:
            self.start_reload()
            return
        # 잔탄 감소
        self.recoil_timer = self.recoil_duration
        self.ammo -= 1

        # 충돌 검사 - LAYER_FOREGROUND와 LAYER_UI 모두 검사
        layers_to_check = [game_world.LAYER_FOREGROUND, game_world.LAYER_UI]

        for layer_index in layers_to_check:
            try:
                layer = game_world.world[layer_index]
            except Exception:
                continue

            for i in list(layer):
                if hasattr(i, 'get_bb'):
                    bb = i.get_bb()
                    if _point_in_bb(self.x, self.y, bb):
                        # 오브젝트에게 데미지 위임
                        if hasattr(i, 'take_damage'):
                            i.take_damage(self.damage)
                        else:
                            # take_damage가 없으면 즉시 제거
                            try:
                                game_world.remove_object(i)
                            except Exception:
                                pass
                        return  # 한 번에 하나의 오브젝트만 맞출 수 있도록

    # 재장전 함수
    def start_reload(self):
        if not self.reloading and self.ammo < self.max_ammo:
            self.reloading = True
            self.reload_timer = self.reloading_duration

    # 플레이어(총)에게 데미지를 입히는 함수 (자폭 오리에서 호출됨)
    def take_damage(self, damage):
        try:
            self.hp -= damage
        except Exception:
            return
        if self.hp <= 0:
            self.hp = 0
            # 체력 0 처리: 현재는 게임 종료 또는 추가 처리 없이 0으로 고정
            # 필요하면 여기서 게임 오버 상태 전환을 구현할 수 있음
