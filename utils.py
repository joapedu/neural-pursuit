import math


def distance(pos1: tuple, pos2: tuple) -> float:
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)


def normalize_vector(x: float, y: float) -> tuple:
    length = math.sqrt(x * x + y * y)
    if length == 0:
        return (0, 0)
    return (x / length, y / length)


def clamp(value: float, min_val: float, max_val: float) -> float:
    return max(min_val, min(value, max_val))


def lerp(start: float, end: float, t: float) -> float:
    return start + (end - start) * t
