from pico2d import *
import game_framework

image=None

def init():
    global image
    try:
        image=load_image('title.png')
    except Exception:
        image=None

def finish():
    global image
    del image

def hande_event(event):
    event_list=get_events()
    for event in event_list:
        if event.type == SDL_KEYDOWN and event.key.keysym.sym == SDLK_SPACE:
            game_framework.change_state('play_mode')
        elif event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key.keysym.sym == SDLK_ESCAPE:
            game_framework.quit()