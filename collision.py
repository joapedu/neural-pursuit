import math
from utils import distance


def check_circle_collision(pos1, radius1, pos2, radius2):
    dist = distance(pos1, pos2)
    return dist < (radius1 + radius2)


def resolve_circle_collision(pos1, radius1, pos2, radius2):
    dist = distance(pos1, pos2)
    if dist == 0:
        return (0, 0)

    overlap = (radius1 + radius2) - dist
    if overlap <= 0:
        return (0, 0)

    dx = (pos2[0] - pos1[0]) / dist
    dy = (pos2[1] - pos1[1]) / dist

    separation_x = dx * overlap * 0.5
    separation_y = dy * overlap * 0.5

    return (separation_x, separation_y)


def check_point_in_obstacle(pos, grid_x, grid_y, cell_size, pathfinding):
    grid_pos_x = pos[0] // cell_size
    grid_pos_y = pos[1] // cell_size
    return not pathfinding.is_walkable(grid_pos_x, grid_pos_y)
