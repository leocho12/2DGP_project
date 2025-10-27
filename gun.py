from pico2d import *
from sdl2 import *

import game_world
from state_machine import StateMachine

class Gun:
    image = None

    def __init__(self,world):
        self.x, self.y=400,60
        self.frame=0
        self.image=load_image('duck.png')

        self.IDLE=Idle(self)
        self.SHOOT=Shoot(self)

        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE:{},
                self.SHOOT:{}
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()

    def fire(self):
        bullet=Bullet(self.x,self.y)
        game_world.add_objects(bullet,1)
