from pico2d import*


from map import Map
from duck import Duck


def handle_events():
    global running

    event_list=get_events()
    for event in event_list:
        if event.type==SDL_QUIT:
            running=False
        elif event.type==SDL_KEYDOWN and event.key==SDLK_ESCAPE:
            running=False
        else:
            duck.handle_event(event)
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