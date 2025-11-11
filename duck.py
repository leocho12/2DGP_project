import random
import math
from pico2d import *
import game_world
import game_framework


# bird Fly Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
Fly_SPEED_KMPH = 10.0  # Km / Hour
Fly_SPEED_MPM = (Fly_SPEED_KMPH * 1000.0 / 60.0)
Fly_SPEED_MPS = (Fly_SPEED_MPM / 60.0)
Fly_SPEED_PPS = (Fly_SPEED_MPS * PIXEL_PER_METER)

# bird Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 3.0

class Idle:
    pass


class Fly:
    pass


class Hit:
    pass


class Die:
    pass

animation_names = ['Fly']

class Duck:

    images=None

    def load_images(self):
        if Duck.images == None:
            Duck.images = {}
            for name in animation_names:
                Duck.images[name] = [load_image("./duck/"+ name + " (%d)" % i + ".png") for i in range(1, 4)]


    def __init__(self, world=None):
        # world는 선택적 인자로 저장(필요시 사용)
        self.world = world
        self.x=random.randint(0,800)
        self.y=100#시작 높이
        self.load_images()
        self.frame=0
        self.dir=random.choice([-1,1])
        self.angle = random.randint(30, 60)  # 30~60도 사이의 각도
        self.speed = Fly_SPEED_PPS
        # 상승 속도 비율 (0.0 ~ 1.0, 작을수록 상승이 느려짐)
        self.upward_scale = 1.0
        # 체력
        self.max_hp=3
        self.hp=self.max_hp

    def get_bb(self):
        half_width = 40  # 이미지 너비의 절반 (80/2)
        half_height = 40  # 이미지 높이의 절반 (80/2)
        return (
            self.x - half_width,  # 왼쪽
            self.y - half_height,  # 아래
            self.x + half_width,  # 오른쪽
            self.y # 위
        )

    def take_damage(self, damage):
        self.hp-=damage
        if self.hp <=0:
            return True
        return False

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

        # 방향 전환 (0.1% 확률)
        if random.random() < 0.005:
            self.dir *= -1
            self.angle = random.randint(30, 60)

        # 대각선 이동 계산 (들여쓰기 수정)
        angle_rad = math.radians(self.angle)
        # 가로 이동
        self.x += self.speed * self.dir * math.cos(angle_rad) * game_framework.frame_time
        # 세로 이동: 상승일 때만 scale 적용
        vertical = self.speed * math.sin(angle_rad) * game_framework.frame_time
        if vertical > 0:
            vertical *= self.upward_scale
        self.y += vertical

        # 화면 경계 처리
        if self.x < 0:
            self.dir = 1
        elif self.x > 800:
            self.dir = -1

        #Y축이 620 이상이면 삭제
        if self.y > 620:
            game_world.remove_object(self)

        self.x = clamp(0, self.x, 800)

    def handle_event(self, event):
        pass

    def draw(self):
        # animation key corrected to 'Fly'
        if self.dir < 0:
            Duck.images['Fly'][int(self.frame)].composite_draw(0, 'h', self.x, self.y, 80, 80)
        else:
            Duck.images['Fly'][int(self.frame)].draw(self.x, self.y, 80, 80)

        # 히트박스
        draw_rectangle(*self.get_bb())
