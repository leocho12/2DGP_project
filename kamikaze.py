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
    explode_images = None

    def load_images(self):
        if Kamikaze.images is None:
            Kamikaze.images = []
            for i in range(1, 5):
                path = f"./duck/Boom ({i}).png"
                try:
                    Kamikaze.images.append(load_image(path))
                except Exception:
                    pass

        # 폭발 애니메이션 프레임 로드 (Explode 1~9)
        if Kamikaze.explode_images is None:
            Kamikaze.explode_images = []
            for i in range(1, 10):
                path = f"./duck/Explode ({i}).png"
                try:
                    Kamikaze.explode_images.append(load_image(path))
                except Exception:
                    pass

    def __init__(self, x=None, y=100, angle_deg=None, target=None):
        self.load_images()
        self.x = random.randint(50, 750) if x is None else x
        self.y = y
        self.frame = 0.0
        self.state = 'Idle'
        self.speed = 180.0
        self.activation_range = 420.0
        self.blast_radius = 80.0
        self.explosion_damage = 2
        self.target = target
        self.explode_duration = 0.45  # 9프레임 * 0.05초 = 0.45초
        self.explode_timer = 0.0
        self.explode_frame = 0.0
        self.base_scale = 0.6
        self.max_scale = 2.0
        self.current_scale = self.base_scale

        # 초기 진행 방향 (생성 위치에서 앞으로 직진)
        if angle_deg is None:
            angle_deg = -90 + random.uniform(-12.0, 12.0)
        rad = math.radians(angle_deg)
        self.vx = math.cos(rad)
        self.vy = math.sin(rad)

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

        player = self.find_player()
        tx, ty = (player.x, player.y) if player else (get_canvas_width() / 2, 60)

        if self.state == 'Idle':
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * dt) % FRAMES_PER_ACTION
            dist = self.distance_to(tx, ty)
            if dist <= self.activation_range:
                self.state = 'Charge'
        elif self.state == 'Charge':
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * dt) % FRAMES_PER_ACTION

            # 자신의 초기 전진 방향으로 직진
            self.x += self.vx * self.speed * dt
            self.y += self.vy * self.speed * dt

            # 플레이어와의 거리로 스케일 조절
            dist = self.distance_to(tx, ty)
            if dist < self.activation_range:
                progress = max(0.0, min(1.0, 1.0 - (dist / max(1.0, self.activation_range))))
            else:
                progress = 0.0
            self.current_scale = self.base_scale + progress * (self.max_scale - self.base_scale)

            # 폭발 범위 도달
            if dist <= self.blast_radius:
                self.state = 'Explode'
                self.explode_timer = self.explode_duration
                self.explode_frame = 0.0
                self.deal_damage_to_player()

            # 화면 밖으로 나가면 제거
            if self.x < -200 or self.x > get_canvas_width() + 200 or self.y < -200 or self.y > get_canvas_height() + 200:
                try:
                    game_world.remove_object(self)
                except Exception:
                    pass

        elif self.state == 'Explode':
            # 폭발 애니메이션: Duck과 동일한 방식으로 프레임 진행
            if Kamikaze.explode_images:
                total_frames = len(Kamikaze.explode_images)
                frame_duration = self.explode_duration / total_frames

                self.explode_timer -= dt
                self.explode_frame += (total_frames / self.explode_duration) * dt

                if self.explode_frame >= total_frames:
                    try:
                        game_world.remove_object(self)
                    except Exception:
                        pass
            else:
                self.explode_timer -= dt
                if self.explode_timer <= 0.0:
                    try:
                        game_world.remove_object(self)
                    except Exception:
                        pass

    def draw(self):
        if self.state == 'Explode' and Kamikaze.explode_images:
            # 폭발 애니메이션 그리기
            total_frames = len(Kamikaze.explode_images)
            if total_frames == 0:
                return
            idx = int(self.explode_frame) % total_frames
            img = Kamikaze.explode_images[idx]
            w = getattr(img, 'w', 100) * self.current_scale
            h = getattr(img, 'h', 100) * self.current_scale
            img.draw(self.x, self.y, w, h)
        else:
            # Idle/Charge 상태: Boom 이미지 그리기
            if Kamikaze.images:
                idx = int(self.frame) % max(1, len(Kamikaze.images))
                img = Kamikaze.images[idx]
                w = getattr(img, 'w', 48) * self.current_scale
                h = getattr(img, 'h', 48) * self.current_scale
                img.draw(self.x, self.y, w, h)
            else:
                draw_rectangle(*self.get_bb())
