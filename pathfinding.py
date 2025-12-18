import heapq
from typing import List, Tuple, Optional, Set
from dataclasses import dataclass


@dataclass
class Node:
    x: int
    y: int
    g: float = 0
    h: float = 0
    parent: Optional["Node"] = None

    @property
    def f(self) -> float:
        return self.g + self.h

    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))


class Pathfinding:
    def __init__(self, grid_width: int, grid_height: int, cell_size: int):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.cell_size = cell_size
        self.obstacles: Set[Tuple[int, int]] = set()

    def add_obstacle(self, x: int, y: int):
        grid_x = x // self.cell_size
        grid_y = y // self.cell_size
        self.obstacles.add((grid_x, grid_y))

    def remove_obstacle(self, x: int, y: int):
        grid_x = x // self.cell_size
        grid_y = y // self.cell_size
        self.obstacles.discard((grid_x, grid_y))

    def is_walkable(self, grid_x: int, grid_y: int) -> bool:
        if grid_x < 0 or grid_x >= self.grid_width:
            return False
        if grid_y < 0 or grid_y >= self.grid_height:
            return False
        return (grid_x, grid_y) not in self.obstacles

    def heuristic(self, node: Node, goal: Node) -> float:
        dx = abs(node.x - goal.x)
        dy = abs(node.y - goal.y)
        return (dx + dy) * 10

    def get_neighbors(self, node: Node) -> List[Node]:
        neighbors = []
        directions = [
            (0, 1),
            (1, 0),
            (0, -1),
            (-1, 0),
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1),
        ]

        for dx, dy in directions:
            new_x = node.x + dx
            new_y = node.y + dy

            if self.is_walkable(new_x, new_y):
                cost = 14 if abs(dx) + abs(dy) == 2 else 10
                neighbors.append(Node(new_x, new_y))

        return neighbors

    def find_path(
        self, start_pos: Tuple[int, int], goal_pos: Tuple[int, int]
    ) -> List[Tuple[int, int]]:
        start_grid_x = start_pos[0] // self.cell_size
        start_grid_y = start_pos[1] // self.cell_size
        goal_grid_x = goal_pos[0] // self.cell_size
        goal_grid_y = goal_pos[1] // self.cell_size

        start = Node(start_grid_x, start_grid_y)
        goal = Node(goal_grid_x, goal_grid_y)

        if not self.is_walkable(goal.x, goal.y):
            return []

        if start == goal:
            return [goal_pos]

        open_set = []
        heapq.heappush(open_set, start)
        closed_set: Set[Tuple[int, int]] = set()
        all_nodes = {start: start}

        while open_set:
            current = heapq.heappop(open_set)

            if (current.x, current.y) in closed_set:
                continue

            closed_set.add((current.x, current.y))

            if current == goal:
                path = []
                node = current
                while node:
                    world_x = node.x * self.cell_size + self.cell_size // 2
                    world_y = node.y * self.cell_size + self.cell_size // 2
                    path.append((world_x, world_y))
                    node = node.parent
                return path[::-1]

            neighbors = self.get_neighbors(current)
            for neighbor in neighbors:
                if (neighbor.x, neighbor.y) in closed_set:
                    continue

                if neighbor not in all_nodes:
                    all_nodes[neighbor] = neighbor

                neighbor_node = all_nodes[neighbor]
                tentative_g = current.g + (
                    14
                    if abs(neighbor.x - current.x) + abs(neighbor.y - current.y) == 2
                    else 10
                )

                if neighbor_node.g == 0 or tentative_g < neighbor_node.g:
                    neighbor_node.g = tentative_g
                    neighbor_node.h = self.heuristic(neighbor_node, goal)
                    neighbor_node.parent = current
                    heapq.heappush(open_set, neighbor_node)

        return []

    def get_next_step(
        self, start_pos: Tuple[int, int], goal_pos: Tuple[int, int]
    ) -> Optional[Tuple[int, int]]:
        path = self.find_path(start_pos, goal_pos)
        if len(path) > 1:
            return path[1]
        elif len(path) == 1:
            return path[0]
        return None
