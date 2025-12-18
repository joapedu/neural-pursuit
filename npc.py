import pygame
import math
from pathfinding import Pathfinding
from fsm import FSM, State
from utils import distance, normalize_vector
from graphics import Graphics
from collision import check_circle_collision, resolve_circle_collision


class NPC:
    def __init__(
        self,
        x: int,
        y: int,
        pathfinding: Pathfinding,
        color: tuple = (255, 0, 0),
        sprite=None,
        sprite_name=None,
    ):
        self.x = float(x)
        self.y = float(y)
        self.start_x = float(x)
        self.start_y = float(y)
        self.radius = 20
        self.speed = 4.5
        self.color = color
        self.pathfinding = pathfinding
        self.fsm = FSM(State.PATROL)
        self.path = []
        self.path_index = 0
        self.patrol_targets = []
        self.patrol_index = 0
        self.chase_target = None
        self.detection_range = 150
        self.attack_range = 40
        self.attack_cooldown = 0
        self.health = 100
        self.max_health = 100
        self.last_known_player_pos = None
        self.return_threshold = 200

        self.sprite = sprite
        self.sprite_name = sprite_name
        if self.sprite:
            original_width, original_height = self.sprite.get_size()
            scale_factor = 0.3
            new_width = int(original_width * scale_factor)
            new_height = int(original_height * scale_factor)
            self.sprite = pygame.transform.scale(self.sprite, (new_width, new_height))
            self.sprite_width, self.sprite_height = self.sprite.get_size()
            self.radius = max(self.sprite_width, self.sprite_height) // 2 + 5
        else:
            self.sprite_width, self.sprite_height = 40, 40

        self.setup_fsm()
        self.setup_patrol_points()

    def setup_patrol_points(self):
        base_x = int(self.start_x)
        base_y = int(self.start_y)
        self.patrol_targets = [
            (base_x - 100, base_y - 100),
            (base_x + 100, base_y - 100),
            (base_x + 100, base_y + 100),
            (base_x - 100, base_y + 100),
        ]

    def setup_fsm(self):
        self.fsm.add_state_handler(State.PATROL, lambda p, o=None: self.handle_patrol(p, o))
        self.fsm.add_state_handler(State.CHASE, lambda p, o=None: self.handle_chase(p, o))
        self.fsm.add_state_handler(State.ATTACK, self.handle_attack)
        self.fsm.add_state_handler(State.RETURN, lambda p, o=None: self.handle_return(p, o))

        self.fsm.add_transition(State.PATROL, State.CHASE, self.should_chase)
        self.fsm.add_transition(State.CHASE, State.ATTACK, self.should_attack)
        self.fsm.add_transition(State.CHASE, State.RETURN, self.should_return)
        self.fsm.add_transition(
            State.ATTACK, State.CHASE, self.should_chase_after_attack
        )
        self.fsm.add_transition(State.ATTACK, State.RETURN, self.should_return)
        self.fsm.add_transition(State.RETURN, State.PATROL, self.should_resume_patrol)

    def should_chase(self, player_pos: tuple) -> bool:
        if player_pos is None:
            return False
        dist = distance((self.x, self.y), player_pos)
        return dist <= self.detection_range

    def should_attack(self, player_pos: tuple) -> bool:
        if player_pos is None:
            return False
        dist = distance((self.x, self.y), player_pos)
        return dist <= self.attack_range

    def should_chase_after_attack(self, player_pos: tuple) -> bool:
        if player_pos is None:
            return False
        dist = distance((self.x, self.y), player_pos)
        return dist > self.attack_range and dist <= self.detection_range

    def should_return(self, player_pos: tuple) -> bool:
        dist_from_start = distance((self.x, self.y), (self.start_x, self.start_y))
        if player_pos is None:
            return dist_from_start > self.return_threshold
        dist_from_player = distance((self.x, self.y), player_pos)
        return (
            dist_from_player > self.detection_range
            and dist_from_start > self.return_threshold
        )

    def should_resume_patrol(self, player_pos: tuple) -> bool:
        dist_from_start = distance((self.x, self.y), (self.start_x, self.start_y))
        return dist_from_start <= 50

    def handle_patrol(self, player_pos: tuple, other_npcs=None):
        if not self.patrol_targets:
            return

        target = self.patrol_targets[self.patrol_index]
        dist = distance((self.x, self.y), target)

        if dist < 20:
            self.patrol_index = (self.patrol_index + 1) % len(self.patrol_targets)
            target = self.patrol_targets[self.patrol_index]
            self.path = []

        if not self.path or len(self.path) == 0:
            next_step = self.pathfinding.get_next_step(
                (int(self.x), int(self.y)), target
            )
            if next_step:
                self.path = [next_step]
                self.path_index = 0

        self.follow_path(other_npcs, player_pos, self.pathfinding)

    def handle_chase(self, player_pos: tuple, other_npcs=None):
        if player_pos is None:
            return

        self.last_known_player_pos = player_pos
        dist = distance((self.x, self.y), player_pos)

        if dist > self.attack_range:
            next_step = self.pathfinding.get_next_step(
                (int(self.x), int(self.y)), player_pos
            )
            if next_step:
                self.path = [next_step]
                self.path_index = 0
            self.follow_path(other_npcs, player_pos, self.pathfinding)

    def handle_attack(self, player_pos: tuple):
        if self.attack_cooldown <= 0:
            self.attack_cooldown = 60
            return True
        return False

    def handle_return(self, player_pos: tuple, other_npcs=None):
        dist_from_start = distance((self.x, self.y), (self.start_x, self.start_y))

        if dist_from_start > 30:
            next_step = self.pathfinding.get_next_step(
                (int(self.x), int(self.y)), (int(self.start_x), int(self.start_y))
            )
            if next_step:
                self.path = [next_step]
                self.path_index = 0
            self.follow_path(other_npcs, player_pos, self.pathfinding)
        else:
            self.path = []
            self.patrol_index = 0

    def follow_path(self, other_npcs=None, player_pos=None, pathfinding=None):
        if not self.path or self.path_index >= len(self.path):
            return

        target = self.path[self.path_index]
        target_x, target_y = target

        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.sqrt(dx * dx + dy * dy)

        if dist < 5:
            self.path_index += 1
        else:
            dx_norm, dy_norm = normalize_vector(dx, dy)
            new_x = self.x + dx_norm * self.speed
            new_y = self.y + dy_norm * self.speed
            
            collision_occurred = False
            
            if pathfinding:
                grid_x = int(new_x) // pathfinding.cell_size
                grid_y = int(new_y) // pathfinding.cell_size
                if not pathfinding.is_walkable(grid_x, grid_y):
                    collision_occurred = True
            
            if not collision_occurred and other_npcs:
                for other_npc in other_npcs:
                    if other_npc != self and other_npc.is_alive():
                        if check_circle_collision(
                            (new_x, new_y), self.radius,
                            (other_npc.x, other_npc.y), other_npc.radius
                        ):
                            sep_x, sep_y = resolve_circle_collision(
                                (new_x, new_y), self.radius,
                                (other_npc.x, other_npc.y), other_npc.radius
                            )
                            new_x -= sep_x
                            new_y -= sep_y
                            collision_occurred = True
            
            if not collision_occurred:
                self.x = new_x
                self.y = new_y

    def update(self, player_pos: tuple, other_npcs=None):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        current_state = self.fsm.get_state()
        if current_state == State.PATROL:
            self.handle_patrol(player_pos, other_npcs)
        elif current_state == State.CHASE:
            self.handle_chase(player_pos, other_npcs)
        elif current_state == State.ATTACK:
            self.handle_attack(player_pos)
        elif current_state == State.RETURN:
            self.handle_return(player_pos, other_npcs)
        
        self.fsm.update(player_pos)

    def draw(self, screen: pygame.Surface):
        npc_pos = (int(self.x), int(self.y))
        current_state = self.fsm.get_state()

        if current_state == State.CHASE:
            detection_surface = pygame.Surface(
                (self.detection_range * 2, self.detection_range * 2), pygame.SRCALPHA
            )
            pygame.draw.circle(
                detection_surface,
                (255, 255, 100, 30),
                (self.detection_range, self.detection_range),
                self.detection_range,
            )
            screen.blit(
                detection_surface,
                (npc_pos[0] - self.detection_range, npc_pos[1] - self.detection_range),
                special_flags=pygame.BLEND_ALPHA_SDL2,
            )
            border_surface = pygame.Surface(
                (self.detection_range * 2, self.detection_range * 2), pygame.SRCALPHA
            )
            pygame.draw.circle(
                border_surface,
                (255, 255, 100, 100),
                (self.detection_range, self.detection_range),
                self.detection_range,
                2,
            )
            screen.blit(
                border_surface,
                (npc_pos[0] - self.detection_range, npc_pos[1] - self.detection_range),
            )

        if self.sprite:
            sprite_rect = self.sprite.get_rect(center=npc_pos)
            
            state_colors = {
                State.PATROL: (100, 255, 100),
                State.CHASE: (255, 255, 100),
                State.ATTACK: (255, 100, 100),
                State.RETURN: (100, 150, 255)
            }
            state_color = state_colors.get(current_state, (255, 255, 255))
            
            outline_width = 3
            outline_surface = pygame.Surface(
                (sprite_rect.width + outline_width * 2, sprite_rect.height + outline_width * 2),
                pygame.SRCALPHA
            )
            
            try:
                mask = pygame.mask.from_surface(self.sprite)
                outline_points = mask.outline()
                
                for point in outline_points:
                    for dx in range(-outline_width, outline_width + 1):
                        for dy in range(-outline_width, outline_width + 1):
                            if dx * dx + dy * dy <= outline_width * outline_width:
                                x, y = point[0] + dx + outline_width, point[1] + dy + outline_width
                                if 0 <= x < outline_surface.get_width() and 0 <= y < outline_surface.get_height():
                                    outline_surface.set_at((x, y), (*state_color, 220))
            except Exception:
                pygame.draw.rect(
                    outline_surface,
                    (*state_color, 220),
                    pygame.Rect(0, 0, outline_surface.get_width(), outline_surface.get_height()),
                    outline_width
                )
            
            screen.blit(outline_surface, (sprite_rect.x - outline_width, sprite_rect.y - outline_width))
            screen.blit(self.sprite, sprite_rect)
        else:
            state_colors = {
                State.PATROL: (100, 255, 100),
                State.CHASE: (255, 255, 100),
                State.ATTACK: (255, 100, 100),
                State.RETURN: (100, 150, 255),
            }
            state_color = state_colors.get(current_state, (255, 255, 255))
            glow_intensity = 6 if current_state == State.CHASE else 4
            Graphics.draw_glow_circle(
                screen, self.color, npc_pos, self.radius, glow_intensity
            )

            hex_points = []
            for i in range(6):
                angle = i * math.pi / 3
                x = npc_pos[0] + self.radius * math.cos(angle)
                y = npc_pos[1] + self.radius * math.sin(angle)
                hex_points.append((x, y))
            pygame.draw.polygon(screen, self.color, hex_points)

        health_bar_width = 35
        health_bar_height = 5
        health_percent = self.health / self.max_health
        sprite_height = self.sprite_height if self.sprite else self.radius * 2
        health_bar_x = int(self.x - health_bar_width // 2)
        health_bar_y = int(self.y - sprite_height // 2 - 15)

        health_bar_rect = pygame.Rect(
            health_bar_x, health_bar_y, health_bar_width, health_bar_height
        )
        pygame.draw.rect(screen, (40, 20, 20), health_bar_rect)
        health_fill = pygame.Rect(
            health_bar_x,
            health_bar_y,
            int(health_bar_width * health_percent),
            health_bar_height,
        )
        Graphics.draw_gradient_rect(
            screen, health_fill, (255, 100, 100), (200, 0, 0), False
        )
        border_surface = pygame.Surface(
            (health_bar_rect.width, health_bar_rect.height), pygame.SRCALPHA
        )
        pygame.draw.rect(
            border_surface,
            (255, 255, 255, 80),
            pygame.Rect(0, 0, health_bar_rect.width, health_bar_rect.height),
            1,
        )
        screen.blit(border_surface, health_bar_rect)

        if self.path and len(self.path) > 0 and current_state != State.PATROL:
            for i, point in enumerate(self.path):
                if i >= self.path_index:
                    Graphics.draw_particle(screen, point, (150, 150, 255), 2, 150)

    def take_damage(self, amount: int):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def is_alive(self) -> bool:
        return self.health > 0
