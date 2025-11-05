import random
import math
from pico2d import *
import game_world
from state_machine import StateMachine

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

    image=None

    def load_images(self):
        if Duck.images == None:
            Duck.images = {}
            for name in animation_names:
                Duck.images[name] = [load_image("./duck/"+ name + " (%d)" % i + ".png") for i in range(1, 11)]


    def __init__(self, world):
        self.x,self.y=random.randint(0,800),10
        self.frame=0
        self.face_dir=1
        self.dir=0

        self.IDLE=Idle(self)
        self.FLY=Fly(self)
        self.HIT=Hit(self)
        self.DIE=Die(self)
        self.state_machine=StateMachine(
            self.IDLE,
            {
                self.FLY:{},
                self.HIT:{},
                self.DIE:{}
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT',event))
        pass

    def draw(self):
        self.state_machine.draw()

