from pico2d import *
import math
import random

import game_world
import game_framework


TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 3.0

class Kamikaze:
    images = None

    def load_images(self):
        if Kamikaze.images is None:
            Kamikaze.images = []
            for i in range(1, 5):
                path = f"./duck/Boom ({i}).png"
                try:
                    Kamikaze.images.append(load_image(path))
                except Exception:
                    pass

    def __init__(self, x=None, y=60, target=None):
        self.load_images()
        self.x = random.randint(50, 750) if x is None else x
        self.y = y
        self.frame = 0.0
        self.state = 'Idle'
        self.speed = 180.0     # 돌진 속도
        self.activation_range = 420.0
        self.blast_radius = 80.0
        self.explosion_damage = 2
        self.target = target
        self.explode_duration = 0.6  # 폭발 애니메이션 총 시간
        self.explode_timer = 0.0
        self.base_scale=0.6
        self.max_scale=2.0
        self.current_scale=self.base_scale


    def get_image_size(self):
        if Kamikaze.images and len(Kamikaze.images) > 0:
            img = Kamikaze.images[0]
            return getattr(img, 'w', 48), getattr(img, 'h', 48)
        return 48, 48

    def get_bb(self):
        w, h = self.get_image_size()
        half_w = (w * self.current_scale) / 2.0
        half_h = (h * self.current_scale) / 2.0
        return (self.x - half_w, self.y - half_h, self.x + half_w, self.y + half_h)


    def distance_to(self, tx, ty):
        return math.hypot(self.x - tx, self.y - ty)

    def find_player(self):
        if self.target:
            return self.target
        try:
            for o in game_world.world[game_world.LAYER_UI]:
                if hasattr(o, 'x') and hasattr(o, 'y'):
                    return o
        except Exception:
            pass
        return None

    def deal_damage_to_player(self):
        player = self.find_player()
        if player is None:
            return
        if hasattr(player, 'take_damage'):
            try:
                player.take_damage(self.explosion_damage)
            except Exception:
                pass
        elif hasattr(player, 'hp'):
            try:
                player.hp -= self.explosion_damage
            except Exception:
                pass

    def update(self):
        dt = game_framework.frame_time
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * dt) % FRAMES_PER_ACTION

        player = self.find_player()
        tx, ty = get_canvas_width() / 2, 60

        if self.state == 'Idle':
            dist = self.distance_to(tx, ty)
            if dist <= self.activation_range:
                self.state = 'Charge'
        elif self.state == 'Charge':
            # 화면(플레이어) 쪽으로 이동
            dx = tx - self.x
            dy = ty - self.y
            dist = math.hypot(dx, dy)
            if dist > 1e-5:
                nx = dx / dist
                ny = dy / dist
                self.x += nx * self.speed * dt
                self.y += ny * self.speed * dt

            # 거리 기반 스케일: 가까워질수록 커짐
            if dist < self.activation_range:
                progress = max(0.0, min(1.0, 1.0 - (dist / max(1.0, self.activation_range))))
            else:
                progress = 0.0
            self.current_scale = self.base_scale + progress * (self.max_scale - self.base_scale)

            # 폭발 범위 도달
            if dist <= self.blast_radius:
                self.state = 'Explode'
                self.explode_timer = self.explode_duration
                self.deal_damage_to_player()
        elif self.state == 'Explode':
            # 폭발 중에는 더 크게 보여줌 (애니메이션 진행률로 추가 증폭)
            self.explode_timer -= dt
            if self.explode_timer <= 0.0:
                try:
                    game_world.remove_object(self)
                except Exception:
                    pass
            else:
                prog = 1.0 - (self.explode_timer / max(self.explode_duration, 1e-6))
                # 폭발시 스케일을 좀 더 키움
                self.current_scale = self.base_scale + (self.max_scale - self.base_scale) * (0.8 + 0.2 * prog)

    def draw(self):
        if self.state == 'Explode' and Kamikaze.images:
            total_frames = len(Kamikaze.images)
            if total_frames == 0:
                return
            progress = max(0.0, min(1.0, 1.0 - (self.explode_timer / max(self.explode_duration, 1e-6))))
            idx = int(progress * (total_frames - 1))
            img = Kamikaze.images[idx]
            w = getattr(img, 'w', 64) * self.current_scale
            h = getattr(img, 'h', 64) * self.current_scale
            img.draw(self.x, self.y, w, h)
        else:
            if Kamikaze.images:
                img = Kamikaze.images[0]
                w = getattr(img, 'w', 48) * self.current_scale
                h = getattr(img, 'h', 48) * self.current_scale
                img.draw(self.x, self.y, w, h)
            else:
                draw_rectangle(*self.get_bb())
