import pygame
import random
from pathfinding import Pathfinding
from npc import NPC
from fsm import State
from graphics import Graphics
from sprites_manager import SpritesManager

GAME_NAME = "Neural Pursuit"


class Game:
    def __init__(self, width: int = 1200, height: int = 800):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(GAME_NAME)
        self.clock = pygame.time.Clock()
        self.running = True

        self.game_state = "menu"
        self.death_timer = 0
        self.death_fade_alpha = 0
        self.menu_fade_alpha = 255

        self.cell_size = 40
        self.grid_width = width // self.cell_size
        self.grid_height = height // self.cell_size

        self.player_x = width // 2
        self.player_y = height // 2
        self.player_radius = 25
        self.player_speed = 4
        self.player_health = 100
        self.max_player_health = 100

        self.pathfinding = Pathfinding(
            self.grid_width, self.grid_height, self.cell_size
        )
        self.setup_obstacles()

        self.font = pygame.font.Font(None, 48)
        self.title_font = pygame.font.Font(None, 72)
        self.small_font = pygame.font.Font(None, 24)
        self.medium_font = pygame.font.Font(None, 32)

        self.show_debug = False
        self.score = 0
        self.time_alive = 0
        self.player_angle = 0
        self.background_gradient = [(15, 15, 35), (25, 20, 45)]

        self.sprites_manager = SpritesManager()
        hero_sprite = self.sprites_manager.get_sprite("hero")
        if hero_sprite:
            hero_width, hero_height = hero_sprite.get_size()
            scale_factor = 0.3
            scaled_width = int(hero_width * scale_factor)
            scaled_height = int(hero_height * scale_factor)
            self.player_sprite = pygame.transform.scale(
                hero_sprite, (scaled_width, scaled_height)
            )
            self.player_sprite_width, self.player_sprite_height = (
                self.player_sprite.get_size()
            )
            self.player_radius = (
                max(self.player_sprite_width, self.player_sprite_height) // 2 + 5
            )
        else:
            self.player_sprite = None
            self.player_sprite_width, self.player_sprite_height = 40, 40

        self.decorations = []
        self.setup_decorations()

        self.npcs = []
        self.setup_npcs()

        menu_sprite = self.sprites_manager.get_sprite("menu")
        if menu_sprite:
            original_width, original_height = menu_sprite.get_size()
            if original_width != self.width or original_height != self.height:
                self.menu_sprite = pygame.transform.scale(
                    menu_sprite, (self.width, self.height)
                )
                scale_x = self.width / original_width
                scale_y = self.height / original_height
            else:
                self.menu_sprite = menu_sprite
                scale_x = 1.0
                scale_y = 1.0

            button_left = int(original_width * 0.05 * scale_x)
            button_right = int(original_width * 0.50 * scale_x)
            button_width = button_right - button_left

            start_button_top = int(original_height * 0.38 * scale_y)
            start_button_bottom = int(original_height * 0.50 * scale_y)
            start_button_height = start_button_bottom - start_button_top

            credits_button_top = int(original_height * 0.54 * scale_y)
            credits_button_bottom = int(original_height * 0.66 * scale_y)
            credits_button_height = credits_button_bottom - credits_button_top

            exit_button_top = int(original_height * 0.70 * scale_y)
            exit_button_bottom = int(original_height * 0.82 * scale_y)
            exit_button_height = exit_button_bottom - exit_button_top

            self.start_button_rect = pygame.Rect(
                button_left, start_button_top, button_width, start_button_height
            )
            self.credits_button_rect = pygame.Rect(
                button_left, credits_button_top, button_width, credits_button_height
            )
            self.exit_button_rect = pygame.Rect(
                button_left, exit_button_top, button_width, exit_button_height
            )
        else:
            self.menu_sprite = None
            self.start_button_rect = pygame.Rect(
                self.width // 2 - 100, self.height // 2 + 30, 200, 40
            )
            self.exit_button_rect = pygame.Rect(
                self.width // 2 - 100, self.height // 2 + 100, 200, 40
            )

        morreu_sprite = self.sprites_manager.get_sprite("morreu")
        if morreu_sprite:
            morreu_width, morreu_height = morreu_sprite.get_size()
            if morreu_width != self.width or morreu_height != self.height:
                self.morreu_sprite = pygame.transform.scale(
                    morreu_sprite, (self.width, self.height)
                )
            else:
                self.morreu_sprite = morreu_sprite
        else:
            self.morreu_sprite = None

        creditos_sprite = self.sprites_manager.get_sprite("creditos")
        if creditos_sprite:
            creditos_width, creditos_height = creditos_sprite.get_size()
            if creditos_width != self.width or creditos_height != self.height:
                self.creditos_sprite = pygame.transform.scale(
                    creditos_sprite, (self.width, self.height)
                )
                scale_x = self.width / creditos_width
                scale_y = self.height / creditos_height
            else:
                self.creditos_sprite = creditos_sprite
                scale_x = 1.0
                scale_y = 1.0

            back_button_top = int(creditos_height * 0.88 * scale_y)
            back_button_bottom = int(creditos_height * 0.95 * scale_y)
            back_button_height = back_button_bottom - back_button_top
            back_button_left = int(creditos_width * 0.40 * scale_x)
            back_button_right = int(creditos_width * 0.60 * scale_x)
            back_button_width = back_button_right - back_button_left

            self.back_button_rect = pygame.Rect(
                back_button_left, back_button_top, back_button_width, back_button_height
            )
        else:
            self.creditos_sprite = None
            self.back_button_rect = pygame.Rect(
                self.width // 2 - 100, self.height - 80, 200, 40
            )

    def setup_obstacles(self):
        num_obstacles = 18
        attempts = 0
        placed = 0
        while placed < num_obstacles and attempts < 100:
            x = random.randint(2, self.grid_width - 3) * self.cell_size
            y = random.randint(2, self.grid_height - 3) * self.cell_size
            grid_x = x // self.cell_size
            grid_y = y // self.cell_size

            player_grid_x = self.player_x // self.cell_size
            player_grid_y = self.player_y // self.cell_size

            if abs(grid_x - player_grid_x) > 3 or abs(grid_y - player_grid_y) > 3:
                self.pathfinding.add_obstacle(x, y)
                placed += 1
            attempts += 1

    def setup_npcs(self):
        positions = [
            (200, 200),
            (1000, 200),
            (200, 600),
            (1000, 600),
        ]

        enemy_sprites = ["inimigo1", "inimigo2", "inimigo3", "inimigo4"]

        for i, (x, y) in enumerate(positions):
            sprite_name = enemy_sprites[i % len(enemy_sprites)]
            enemy_sprite = self.sprites_manager.get_sprite(sprite_name)
            npc = NPC(
                x, y, self.pathfinding, sprite=enemy_sprite, sprite_name=sprite_name
            )
            self.npcs.append(npc)

    def setup_decorations(self):
        deco_sprites = ["deco1", "deco2", "deco3"]
        margin = 80
        num_decorations = 12

        for i, deco_name in enumerate(deco_sprites):
            deco_sprite = self.sprites_manager.get_sprite(deco_name)
            if deco_sprite:
                deco_width, deco_height = deco_sprite.get_size()
                scaled_width = int(deco_width * 0.6)
                scaled_height = int(deco_height * 0.6)
                scaled_sprite = pygame.transform.scale(
                    deco_sprite, (scaled_width, scaled_height)
                )

                decorations_per_type = num_decorations // len(deco_sprites)
                for j in range(decorations_per_type):
                    x = random.randint(margin, self.width - margin)
                    y = random.randint(margin, self.height - margin)

                    grid_x = x // self.cell_size
                    grid_y = y // self.cell_size

                    player_grid_x = self.player_x // self.cell_size
                    player_grid_y = self.player_y // self.cell_size

                    if (
                        abs(grid_x - player_grid_x) > 2
                        or abs(grid_y - player_grid_y) > 2
                    ):
                        if self.pathfinding.is_walkable(grid_x, grid_y):
                            self.decorations.append(
                                {
                                    "sprite": scaled_sprite,
                                    "x": x,
                                    "y": y,
                                    "width": scaled_width,
                                    "height": scaled_height,
                                }
                            )

    def handle_input(self):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= self.player_speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += self.player_speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= self.player_speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += self.player_speed

        new_x = self.player_x + dx
        new_y = self.player_y + dy

        player_collision_radius = (
            max(self.player_sprite_width, self.player_sprite_height) // 2
            if self.player_sprite
            else self.player_radius
        )

        grid_x = new_x // self.cell_size
        grid_y = new_y // self.cell_size

        if self.pathfinding.is_walkable(grid_x, grid_y):
            if player_collision_radius <= new_x < self.width - player_collision_radius:
                self.player_x = new_x
            if player_collision_radius <= new_y < self.height - player_collision_radius:
                self.player_y = new_y

    def reset_game(self):
        self.player_x = self.width // 2
        self.player_y = self.height // 2
        self.player_health = self.max_player_health
        self.time_alive = 0
        self.score = 0

        for npc in self.npcs:
            npc.x = npc.start_x
            npc.y = npc.start_y
            npc.health = npc.max_health
            npc.fsm.change_state(State.PATROL)
            npc.path = []
            npc.path_index = 0

    def update(self):
        if self.game_state == "menu" or self.game_state == "credits":
            return

        if self.game_state == "death":
            self.death_timer += 1 / 60

            if self.death_timer < 1.0:
                self.death_fade_alpha = min(255, int(self.death_timer * 255))
            elif self.death_timer < 2.0:
                self.death_fade_alpha = 255
            elif self.death_timer < 3.0:
                fade_out = (self.death_timer - 2.0) / 1.0
                self.death_fade_alpha = int(255 * (1 - fade_out))
            else:
                self.game_state = "menu"
                self.death_timer = 0
                self.death_fade_alpha = 0
                self.menu_fade_alpha = 0
                self.reset_game()
            return

        player_pos = (self.player_x, self.player_y)

        keys = pygame.key.get_pressed()
        if (
            keys[pygame.K_w]
            or keys[pygame.K_UP]
            or keys[pygame.K_s]
            or keys[pygame.K_DOWN]
            or keys[pygame.K_a]
            or keys[pygame.K_LEFT]
            or keys[pygame.K_d]
            or keys[pygame.K_RIGHT]
        ):
            self.player_angle += 0.15

        self.time_alive += 1 / 60

        for npc in self.npcs:
            if npc.is_alive():
                npc.update(player_pos, self.npcs)

                if npc.fsm.get_state() == State.ATTACK:
                    if npc.handle_attack(player_pos):
                        self.player_health -= 5
                        if self.player_health <= 0:
                            self.player_health = 0

        if self.player_health <= 0 and self.game_state == "playing":
            self.game_state = "death"
            self.death_timer = 0
            self.death_fade_alpha = 0

    def draw_obstacles(self):
        for grid_x in range(self.grid_width):
            for grid_y in range(self.grid_height):
                if not self.pathfinding.is_walkable(grid_x, grid_y):
                    x = grid_x * self.cell_size
                    y = grid_y * self.cell_size
                    rect = pygame.Rect(x, y, self.cell_size, self.cell_size)

                    Graphics.draw_gradient_rect(
                        self.screen, rect, (60, 50, 70), (40, 35, 55), True
                    )

                    inner_rect = pygame.Rect(
                        x + 2, y + 2, self.cell_size - 4, self.cell_size - 4
                    )
                    Graphics.draw_gradient_rect(
                        self.screen, inner_rect, (80, 70, 90), (60, 50, 70), True
                    )

                    pygame.draw.rect(self.screen, (30, 25, 40), rect, 2)

                    center_x = x + self.cell_size // 2
                    center_y = y + self.cell_size // 2
                    Graphics.draw_hexagon(
                        self.screen,
                        (center_x, center_y),
                        self.cell_size // 3,
                        (50, 40, 60),
                        (30, 25, 40),
                        1,
                    )

    def draw_grid(self):
        if not self.show_debug:
            return

        grid_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(grid_surface, (40, 35, 50, 30), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(grid_surface, (40, 35, 50, 30), (0, y), (self.width, y))
        self.screen.blit(grid_surface, (0, 0))

    def draw_ui(self):
        ui_padding = 15
        ui_y = 15

        panel_rect = pygame.Rect(10, 10, 220, 140)
        panel_surface = pygame.Surface(
            (panel_rect.width, panel_rect.height), pygame.SRCALPHA
        )
        panel_surface.fill((20, 20, 35, 200))
        self.screen.blit(panel_surface, panel_rect)
        pygame.draw.rect(self.screen, (255, 255, 255, 30), panel_rect, 2)

        title_text = self.medium_font.render(GAME_NAME, True, (150, 200, 255))
        self.screen.blit(title_text, (ui_padding, ui_y))

        health_text = self.small_font.render(
            f"Vida: {self.player_health}/{self.max_player_health}",
            True,
            (255, 255, 255),
        )
        self.screen.blit(health_text, (ui_padding, ui_y + 35))

        health_bar_rect = pygame.Rect(ui_padding, ui_y + 55, 200, 8)
        pygame.draw.rect(self.screen, (50, 20, 20), health_bar_rect)
        health_fill = pygame.Rect(
            ui_padding,
            ui_y + 55,
            int(200 * (self.player_health / self.max_player_health)),
            8,
        )
        Graphics.draw_gradient_rect(
            self.screen, health_fill, (255, 80, 80), (200, 0, 0), False
        )
        border_surface = pygame.Surface(
            (health_bar_rect.width, health_bar_rect.height), pygame.SRCALPHA
        )
        pygame.draw.rect(
            border_surface,
            (255, 255, 255, 100),
            pygame.Rect(0, 0, health_bar_rect.width, health_bar_rect.height),
            1,
        )
        self.screen.blit(border_surface, health_bar_rect)

        time_text = self.small_font.render(
            f"Tempo: {self.time_alive:.1f}s", True, (200, 200, 255)
        )
        self.screen.blit(time_text, (ui_padding, ui_y + 70))

        npc_count = sum(1 for npc in self.npcs if npc.is_alive())
        npc_text = self.small_font.render(
            f"Caçadores: {npc_count}", True, (255, 200, 150)
        )
        self.screen.blit(npc_text, (ui_padding, ui_y + 90))

        legend_panel = pygame.Rect(10, self.height - 120, 250, 110)
        legend_surface = pygame.Surface(
            (legend_panel.width, legend_panel.height), pygame.SRCALPHA
        )
        legend_surface.fill((20, 20, 35, 200))
        self.screen.blit(legend_surface, legend_panel)
        pygame.draw.rect(self.screen, (255, 255, 255, 30), legend_panel, 2)

        legend_title = self.small_font.render(
            "Estados dos NPCs:", True, (200, 200, 255)
        )
        self.screen.blit(legend_title, (20, self.height - 110))

        state_legend = [
            ((100, 255, 100), "Patrulha"),
            ((255, 255, 100), "Perseguir"),
            ((255, 100, 100), "Atacar"),
            ((100, 150, 255), "Retornar"),
        ]

        y_offset = self.height - 85
        for i, (color, state_name) in enumerate(state_legend):
            pygame.draw.circle(self.screen, color, (30, y_offset + i * 20), 6)
            text = self.small_font.render(state_name, True, (255, 255, 255))
            self.screen.blit(text, (45, y_offset + i * 20 - 8))

        if not self.running:
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))

            game_over = self.title_font.render("GAME OVER", True, (255, 80, 80))
            text_rect = game_over.get_rect(
                center=(self.width // 2, self.height // 2 - 40)
            )
            Graphics.draw_shadow_rect(self.screen, text_rect, (255, 80, 80))
            self.screen.blit(game_over, text_rect)

            time_survived = self.medium_font.render(
                f"Tempo de Sobrevivência: {self.time_alive:.1f}s", True, (255, 255, 255)
            )
            time_rect = time_survived.get_rect(
                center=(self.width // 2, self.height // 2 + 20)
            )
            self.screen.blit(time_survived, time_rect)

            restart_text = self.small_font.render(
                "Pressione ESC para sair", True, (200, 200, 200)
            )
            restart_rect = restart_text.get_rect(
                center=(self.width // 2, self.height // 2 + 60)
            )
            self.screen.blit(restart_text, restart_rect)

    def draw_background(self):
        Graphics.draw_gradient_rect(
            self.screen,
            pygame.Rect(0, 0, self.width, self.height),
            self.background_gradient[0],
            self.background_gradient[1],
            True,
        )

        if not hasattr(self, "stars"):
            self.stars = [
                (
                    random.randint(0, self.width),
                    random.randint(0, self.height),
                    random.randint(1, 3),
                    random.randint(30, 80),
                )
                for _ in range(30)
            ]

        for x, y, size, alpha in self.stars:
            Graphics.draw_particle(self.screen, (x, y), (200, 200, 255), size, alpha)

    def draw_decorations(self):
        for deco in self.decorations:
            self.screen.blit(deco["sprite"], (deco["x"], deco["y"]))

    def draw_menu(self):
        if self.menu_sprite:
            if self.menu_fade_alpha < 255:
                self.menu_fade_alpha = min(255, self.menu_fade_alpha + 5)

            menu_surface = self.menu_sprite.copy()
            menu_surface.set_alpha(self.menu_fade_alpha)
            self.screen.blit(menu_surface, (0, 0))

            if self.show_debug:
                pygame.draw.rect(self.screen, (255, 0, 0), self.start_button_rect, 2)
                pygame.draw.rect(self.screen, (0, 255, 0), self.exit_button_rect, 2)
        else:
            self.screen.fill((20, 20, 30))
            title = self.title_font.render(GAME_NAME, True, (150, 200, 255))
            title_rect = title.get_rect(
                center=(self.width // 2, self.height // 2 - 100)
            )
            self.screen.blit(title, title_rect)

            start_text = self.medium_font.render(
                "Press SPACE to Start", True, (255, 255, 255)
            )
            start_rect = start_text.get_rect(
                center=(self.width // 2, self.height // 2 + 50)
            )
            self.screen.blit(start_text, start_rect)

    def draw_death_screen(self):
        if self.morreu_sprite:
            death_surface = self.morreu_sprite.copy()
            death_surface.set_alpha(self.death_fade_alpha)
            self.screen.blit(death_surface, (0, 0))
        else:
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, self.death_fade_alpha))
            self.screen.blit(overlay, (0, 0))

            game_over = self.title_font.render("YOU DIED", True, (255, 80, 80))
            text_rect = game_over.get_rect(center=(self.width // 2, self.height // 2))
            self.screen.blit(game_over, text_rect)

    def draw_credits_screen(self):
        if self.creditos_sprite:
            self.screen.blit(self.creditos_sprite, (0, 0))

            if self.show_debug:
                pygame.draw.rect(self.screen, (255, 0, 0), self.back_button_rect, 2)
        else:
            self.screen.fill((20, 20, 30))
            credits_text = self.title_font.render("CREDITS", True, (150, 200, 255))
            credits_rect = credits_text.get_rect(
                center=(self.width // 2, self.height // 2 - 100)
            )
            self.screen.blit(credits_text, credits_rect)

            back_text = self.medium_font.render(
                "Press ESC to go back", True, (255, 255, 255)
            )
            back_rect = back_text.get_rect(center=(self.width // 2, self.height - 50))
            self.screen.blit(back_text, back_rect)

    def draw_credits_screen(self):
        if self.creditos_sprite:
            self.screen.blit(self.creditos_sprite, (0, 0))

            if self.show_debug:
                pygame.draw.rect(self.screen, (255, 0, 0), self.back_button_rect, 2)
        else:
            self.screen.fill((20, 20, 30))
            credits_text = self.title_font.render("CREDITS", True, (150, 200, 255))
            credits_rect = credits_text.get_rect(
                center=(self.width // 2, self.height // 2 - 100)
            )
            self.screen.blit(credits_text, credits_rect)

            back_text = self.medium_font.render(
                "Press ESC to go back", True, (255, 255, 255)
            )
            back_rect = back_text.get_rect(center=(self.width // 2, self.height - 50))
            self.screen.blit(back_text, back_rect)

    def draw(self):
        if self.game_state == "menu":
            self.draw_menu()
        elif self.game_state == "credits":
            self.draw_credits_screen()
        elif self.game_state == "death":
            self.draw_death_screen()
        else:
            self.draw_background()
            self.draw_decorations()
            self.draw_grid()
            self.draw_obstacles()

            for npc in self.npcs:
                if npc.is_alive():
                    npc.draw(self.screen)

            if self.player_sprite:
                player_pos = (int(self.player_x), int(self.player_y))
                sprite_rect = self.player_sprite.get_rect(center=player_pos)
                self.screen.blit(self.player_sprite, sprite_rect)
            else:
                player_pos = (int(self.player_x), int(self.player_y))
                Graphics.draw_glow_circle(
                    self.screen, (100, 200, 255), player_pos, self.player_radius, 8
                )
                player_points = Graphics.draw_polygon_player(
                    self.screen, player_pos, self.player_radius, self.player_angle
                )
                pygame.draw.polygon(self.screen, (80, 180, 255), player_points)
                pygame.draw.polygon(self.screen, (150, 220, 255), player_points, 2)

            self.draw_ui()

        pygame.display.flip()

    def handle_menu_click(self, pos):
        if self.start_button_rect.collidepoint(pos):
            self.game_state = "playing"
            self.menu_fade_alpha = 255
            return True
        elif self.exit_button_rect.collidepoint(pos):
            self.running = False
            return True
        elif hasattr(
            self, "credits_button_rect"
        ) and self.credits_button_rect.collidepoint(pos):
            self.game_state = "credits"
            return True
        return False

    def handle_credits_click(self, pos):
        if hasattr(self, "back_button_rect") and self.back_button_rect.collidepoint(
            pos
        ):
            self.game_state = "menu"
            return True
        return False

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.game_state == "playing":
                            self.game_state = "menu"
                            self.reset_game()
                        elif self.game_state == "credits":
                            self.game_state = "menu"
                        else:
                            self.running = False
                    elif event.key == pygame.K_F1:
                        self.show_debug = not self.show_debug
                    elif event.key == pygame.K_SPACE:
                        if self.game_state == "menu":
                            self.game_state = "playing"
                            self.menu_fade_alpha = 255
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.game_state == "menu":
                            self.handle_menu_click(event.pos)
                        elif self.game_state == "credits":
                            self.handle_credits_click(event.pos)

            if self.game_state == "playing":
                self.handle_input()

            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()
