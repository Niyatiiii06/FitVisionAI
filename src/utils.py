import math


def calculate_angle(a, b, c):
    """
    Calculate the angle ABC in degrees.
    B is the middle joint.
    """

    ax, ay = a.x, a.y
    bx, by = b.x, b.y
    cx, cy = c.x, c.y

    radians = math.atan2(cy - by, cx - bx) - math.atan2(ay - by, ax - bx)

    angle = abs(math.degrees(radians))

    if angle > 180:
        angle = 360 - angle

    return angle