from pico2d import*
from map import Map

def handle_events():
    pass

def reset_world():
    pass

def update_world():
    pass

def render_world():
    pass

running=True

open_canvas()
reset_world()
#game main loop
while running:
    handle_events()
    update_world()
    clear_canvas()
    render_world()
    delay(0.01)
#finalization code
close_canvas()