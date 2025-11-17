from pico2d import *
import math
import random

import game_world
import game_framework

# 필요하면 Gun 타입 비교를 위해 import 가능 (선택)
# from gun import Gun

# 애니메이션 상수 (duck.py와 동일한 방식 사용 가능)
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 3.0

class Kamikaze:
    images = None

    def load_images(self):
        if Kamikaze.images is None:
            Kamikaze.images = []
            # duck 폴더의 Boom (1).png ... Boom (4).png 사용
            for i in range(1, 5):
                path = f"./duck/Boom ({i}).png"
                try:
                    Kamikaze.images.append(load_image(path))
                except Exception:
                    pass
            # fallback 빈 이미지 리스트 허용

    def __init__(self, x=None, y=60, target=None):
        # 기본적으로 풀 뒤에 숨기려면 y는 낮게(풀 높이와 비슷) 둠
        self.load_images()
        self.x = random.randint(50, 750) if x is None else x
        self.y = y
        self.frame = 0.0
        self.state = 'Idle'    # 'Idle' | 'Charge' | 'Explode'
        self.speed = 180.0     # 돌진 속도 (pixel/s)
        self.activation_range = 220.0
        self.blast_radius = 80.0
        self.explosion_damage = 2
        self.target = target  # target이 없으면 UI 레이어에서 Gun을 찾음
        self.explode_duration = 0.6  # 폭발 애니메이션 총 시간
        self.explode_timer = 0.0

    def get_bb(self):
        # 히트박스는 돌진 중 플레이어와의 충돌 판정용(디버그 용)
        half = 20
        return (self.x - half, self.y - half, self.x + half, self.y + half)

    def distance_to(self, tx, ty):
        return math.hypot(self.x - tx, self.y - ty)

    def find_player(self):
        if self.target:
            return self.target
        # UI 레이어에서 Gun 인스턴스를 찾아 반환
        try:
            for o in game_world.world[game_world.LAYER_UI]:
                # 간단 타입 체크: Gun 클래스가 없으면 duck/gun 모듈의 속성으로 판단
                # 대신, 플레이어 역할을 하는 객체를 반환
                if hasattr(o, 'x') and hasattr(o, 'y'):
                    return o
        except Exception:
            pass
        return None

    def deal_damage_to_player(self):
        player = self.find_player()
        if player is None:
            return
        # 우선 take_damage 메서드 호출
        if hasattr(player, 'take_damage'):
            try:
                player.take_damage(self.explosion_damage)
            except Exception:
                pass
        # 아니면 hp 속성이 있으면 직접 감소
        elif hasattr(player, 'hp'):
            try:
                player.hp -= self.explosion_damage
            except Exception:
                pass

    def update(self):
        dt = game_framework.frame_time
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * dt) % FRAMES_PER_ACTION

        player = self.find_player()
        if self.state == 'Idle':
            if player:
                dist = self.distance_to(player.x, player.y)
                if dist <= self.activation_range:
                    self.state = 'Charge'
        elif self.state == 'Charge':
            if player:
                # 플레이어 쪽으로 직선 이동
                dx = player.x - self.x
                dy = player.y - self.y
                dist = math.hypot(dx, dy)
                if dist > 1e-5:
                    nx = dx / dist
                    ny = dy / dist
                    self.x += nx * self.speed * dt
                    self.y += ny * self.speed * dt
                # 폭발 범위 도달 시 폭발 상태로 전환
                if dist <= self.blast_radius:
                    self.state = 'Explode'
                    self.explode_timer = self.explode_duration
                    # 즉시 한 번 데미지 적용 (근거리이므로)
                    self.deal_damage_to_player()
            else:
                # 플레이어 없으면 대기 상태로 복귀
                self.state = 'Idle'
        elif self.state == 'Explode':
            # 폭발 애니메이션 시간 감소
            self.explode_timer -= dt
            if self.explode_timer <= 0.0:
                # 애니메이션 종료 후 오브젝트 제거
                try:
                    game_world.remove_object(self)
                except Exception:
                    pass

    def draw(self):
        # 상태에 따라 다른 프레임을 그림
        if self.state == 'Explode' and Kamikaze.images:
            # 폭발 애니메이션: frame 인덱스를 explode 진행률로 매핑
            total_frames = len(Kamikaze.images)
            if total_frames == 0:
                return
            progress = max(0.0, min(1.0, 1.0 - (self.explode_timer / max(self.explode_duration, 1e-6))))
            idx = int(progress * (total_frames - 1))
            img = Kamikaze.images[idx]
            w = getattr(img, 'w', 64)
            h = getattr(img, 'h', 64)
            img.draw(self.x, self.y, w, h)
        else:
            # Idle / Charge 시에는 첫 프레임(숨은 상태도 그리되 풀에 의해 가려짐)
            if Kamikaze.images:
                img = Kamikaze.images[0]
                w = getattr(img, 'w', 48)
                h = getattr(img, 'h', 48)
                img.draw(self.x, self.y, w, h)
            else:
                # 이미지가 없으면 간단한 디버그 사각형
                draw_rectangle(*self.get_bb())
