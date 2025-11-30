from pico2d import *
from damage_overlay import DamageOverlay
from gun import Gun
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
    damage=None

    def load_images(self):
        if Kamikaze.images is None:
            Kamikaze.images = []
            for i in range(1, 5):
                path = f"./duck/Boom ({i}).png"
                try:
                    Kamikaze.images.append(load_image(path))
                except Exception:
                    pass

        # 폭발 애니메이션
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

        # x=400 기준으로 대칭 위치에서 생성
        if x is None:
            if random.random() < 0.5:
                self.x = random.randint(100, 300)  # 왼쪽
            else:
                self.x = random.randint(500, 700)  # 오른쪽
        else:
            self.x = x

        self.y = y
        self.frame = 0.0
        self.state = 'Charge'
        # 기본 속도를 더 빠르게 설정 (기존 180 -> 320)
        self.base_speed = 320.0
        # 중앙 근처에서 소폭 가속을 적용하기 위한 파라미터
        self.speed_boost_near = 1.25
        self.boost_range = 150.0
        self.activation_range = 300.0
        self.blast_radius = 80.0
        self.explosion_damage = 1
        self.target = target
        self.explode_duration = 0.45
        self.explode_timer = 0.0
        self.explode_frame = 0.0
        self.base_scale = 1.0
        self.max_scale = 2.0
        self.current_scale = self.base_scale

        # 화면 중앙 하단을 향하는 방향 설정
        target_x = get_canvas_width() / 2  # 400
        target_y = 60

        dx = target_x - self.x
        dy = target_y - self.y
        angle_rad = math.atan2(dy, dx)

        self.vx = math.cos(angle_rad)
        self.vy = math.sin(angle_rad)

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
        # 우선 타겟이 지정되어 있으면 그것을 사용
        if self.target:
            return self.target

        # UI 레이어에서 Gun 인스턴스를 직접 찾아 반환하도록 변경
        try:
            for o in game_world.world[game_world.LAYER_UI]:
                if isinstance(o, Gun):
                    return o
        except Exception:
            pass
        return None

    def deal_damage_to_player(self):
        # 중앙 도달 시에만 호출되며, 여기서 데미지 오버레이를 생성함
        overlay = DamageOverlay()
        game_world.add_object(overlay, game_world.LAYER_UI)

        player = self.find_player()
        if player is None:
            return

        # 플레이어에게 실제 데미지 전달(가능하면)
        if hasattr(player, 'take_damage'):
            try:
                player.take_damage(self.explosion_damage)
            except Exception as e:
                pass
        elif hasattr(player, 'hp'):
            try:
                player.hp -= self.explosion_damage
            except Exception:
                pass

    def take_damage(self, damage):
        # 피격 처리는 그대로: 폭발 상태가 아니면 제거되도록 유지
        if self.state == 'Explode':
            return
        try:
            game_world.score += 30
        except Exception:
            pass
        # 통계: 처치한 오리 수 증가
        try:
            game_world.ducks_killed += 1
        except Exception:
            pass
        try:
            game_world.remove_object(self)
        except Exception:
            pass


    def update(self):
        dt = game_framework.frame_time

        if self.state == 'Charge':
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * dt) % FRAMES_PER_ACTION

            # 속도 계산: 중앙 근처에서는 약간 가속
            if abs(self.x - 400) <= self.boost_range:
                current_speed = self.base_speed * self.speed_boost_near * game_world.speed_multiplier
            else:
                current_speed = self.base_speed * game_world.speed_multiplier

            # 초기 방향을 유지하며 직진 (현재 속도 사용)
            self.x += self.vx * current_speed * dt
            self.y += self.vy * current_speed * dt

            # x=400까지의 거리로 스케일 조절
            start_x = 100 if self.x < 400 else 700  # 시작 위치 (왼쪽 또는 오른쪽)
            total_distance = abs(400 - start_x)  # 400까지의 총 거리 (300)
            current_distance = abs(self.x - start_x)  # 현재까지 이동한 거리

            # 진행도 계산
            progress = min(1.0, current_distance / total_distance)

            # 크기 조절
            self.current_scale = self.base_scale + progress * (self.max_scale - self.base_scale)

            # x=400 근처에 도달하면 폭발
            if abs(self.x - 400) <= 10:
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
            if Kamikaze.explode_images:
                total_frames = len(Kamikaze.explode_images)
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
            if Kamikaze.images:
                idx = int(self.frame) % max(1, len(Kamikaze.images))
                img = Kamikaze.images[idx]
                w = getattr(img, 'w', 48) * self.current_scale
                h = getattr(img, 'h', 48) * self.current_scale
                img.draw(self.x, self.y, w, h)
            else:
                draw_rectangle(*self.get_bb())
