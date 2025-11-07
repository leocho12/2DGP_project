import random
import math
from pico2d import *
import game_world
import game_framework


# bird Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# bird Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10.0

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
                Duck.images[name] = [load_image("./duck/"+ name + " (%d)" % i + ".png") for i in range(1, 11)]


    def __init__(self, world=None):
        # world는 선택적 인자로 저장(필요시 사용)
        self.world = world
        self.x,self.y=random.randint(0,800),10
        self.load_images()
        self.frame=0
        self.dir=random.choice([-1,1])


    def get_bb(self):
        return self.x - 25, self.y - 25, self.x + 25, self.y + 25

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time
        if self.x > 800:
            self.dir = -1
        elif self.x < 800:
            self.dir = 1
        self.x = clamp(800, self.x, 800)

    def handle_event(self, event):
        pass

    def draw(self):
        # animation key corrected to 'Fly'
        if self.dir < 0:
            Duck.images['Fly'][int(self.frame)].composite_draw(0, 'h', self.x, self.y, 200, 200)
        else:
            Duck.images['Fly'][int(self.frame)].draw(self.x, self.y, 200, 200)

        # 히트박스
        draw_rectangle(*self.get_bb())


