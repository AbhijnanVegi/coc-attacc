import math

from game.game_object import GameObject


def get_distance(position1: tuple, position2: tuple) -> float:
    return math.sqrt(
        (position1[0] - position2[0]) ** 2 + (position1[1] - position2[1]) ** 2
    )


def get_nearest_object(objects: list, position: tuple):
    nearest = None
    min_distance = 1000
    for obj in objects:
        if not obj:
            continue
        distance = get_distance(position, obj.position)
        if distance < min_distance:
            min_distance = distance
            nearest = obj

    return nearest


def get_nearest_pos(object: GameObject, position: tuple):
    if not object:
        return None
    row = None
    col = None
    if position[0] <= object.position[0]:
        col = 0
    elif position[0] >= object.position[0] + object.size[0]:
        col = object.size[0] - 1
    elif (
        position[0] > object.position[0]
        and position[0] < object.position[0] + object.size[0]
    ):
        col = position[0] - object.position[0]

    if position[1] <= object.position[1]:
        row = 0
    elif position[1] >= object.position[1] + object.size[1]:
        row = object.size[1] - 1
    elif (
        position[1] > object.position[1]
        and position[1] < object.position[1] + object.size[1]
    ):
        row = position[1] - object.position[1]

    return (object.position[0] + col, object.position[1] + row)


def check_collision(object1: GameObject, object2: GameObject) -> bool:
    if not object1 or not object2:
        return False
    collisionX = (
        object1.position[0] + object1.size[0] >= object2.position[0]
        and object1.position[0] <= object2.position[0] + object2.size[0]
    )
    collisionY = (
        object1.position[1] + object1.size[1] >= object2.position[1]
        and object1.position[1] <= object2.position[1] + object2.size[1]
    )

    return collisionX and collisionY


def check_inside(object1: GameObject, object2: GameObject) -> bool:
    if not object1 or not object2:
        return False
    x = (
        object1.position[0] + object1.size[0] > object2.position[0]
        and object1.position[0] < object2.position[0] + object2.size[0]
    )
    y = (
        object1.position[1] + object1.size[1] > object2.position[1]
        and object1.position[1] < object2.position[1] + object2.size[1]
    )

    return x and y
