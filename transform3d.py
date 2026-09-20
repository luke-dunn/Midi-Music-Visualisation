import math

from settings import (
    TILT,
    CAMERA_DISTANCE,
    WIDTH,
    HEIGHT,
    WORLD_SCALE,
)


def rotate_point(x, y, z, angle):

    # Rotate around vertical Y axis
    ca = math.cos(angle)
    sa = math.sin(angle)

    x2 = x * ca + z * sa
    z2 = -x * sa + z * ca

    # Permanent tilt
    ct = math.cos(TILT)
    st = math.sin(TILT)

    y2 = y * ct - z2 * st
    z3 = y * st + z2 * ct

    return x2, y2, z3


def project_point(x, y, z):

    depth = CAMERA_DISTANCE + z
    perspective = CAMERA_DISTANCE / depth

    screen_x = WIDTH / 2 + x * WORLD_SCALE * perspective
    screen_y = HEIGHT / 2 - y * WORLD_SCALE * perspective

    return screen_x, screen_y
