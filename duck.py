from pico2d import *
import game_world
from state_machine import StateMachine

class Duck:

    image=None

    def __init__(self, world):
        self.x,self.y=400,60
        self.frame=0
        self.face_dir=1
        self.dir=0
        self.image=load_image('duck.png')

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

