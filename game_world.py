# layer 0: Background Objects
# layer 1: Foreground Objects

world = [[], [], []]  # 게임 내 객체들을 담는 리스트

def add_object(o, depth=0):
    world[depth].append(o)

def add_objects(ol, depth=0):
    world[depth] += ol

def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            return
    raise ValueError('Cannot delete non existing object')

def update():
    for layer in world:
        for o in list(layer):
            o.update()

def render():
    for layer in world:
        for o in list(layer):
            o.draw()

def clear():
    global world

    for layer in world:
        layer.clear()