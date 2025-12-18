import pygame
import math


class Graphics:
    @staticmethod
    def draw_glow_circle(surface, color, pos, radius, glow_radius=5):
        for i in range(glow_radius, 0, -1):
            alpha = int(50 * (1 - i / glow_radius))
            size = radius + i * 2
            s = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            glow_color = (*color[:3], alpha)
            pygame.draw.circle(s, glow_color, (size, size), size)
            surface.blit(
                s, (pos[0] - size, pos[1] - size), special_flags=pygame.BLEND_ALPHA_SDL2
            )
        pygame.draw.circle(surface, color, pos, radius)

    @staticmethod
    def draw_polygon_player(surface, pos, radius, angle=0):
        points = []
        for i in range(8):
            angle_rad = (angle + i * math.pi / 4) - math.pi / 2
            x = pos[0] + radius * math.cos(angle_rad)
            y = pos[1] + radius * math.sin(angle_rad)
            points.append((x, y))
        return points

    @staticmethod
    def draw_hexagon(surface, pos, radius, color, border_color=None, border_width=2):
        points = []
        for i in range(6):
            angle = i * math.pi / 3
            x = pos[0] + radius * math.cos(angle)
            y = pos[1] + radius * math.sin(angle)
            points.append((x, y))
        pygame.draw.polygon(surface, color, points)
        if border_color:
            pygame.draw.polygon(surface, border_color, points, border_width)

    @staticmethod
    def draw_shadow_rect(surface, rect, color, shadow_offset=3):
        shadow_rect = rect.copy()
        shadow_rect.x += shadow_offset
        shadow_rect.y += shadow_offset
        shadow_surface = pygame.Surface(
            (shadow_rect.width, shadow_rect.height), pygame.SRCALPHA
        )
        shadow_surface.fill((0, 0, 0, 100))
        surface.blit(shadow_surface, shadow_rect)
        pygame.draw.rect(surface, color, rect)

    @staticmethod
    def draw_gradient_rect(surface, rect, start_color, end_color, vertical=True):
        if vertical:
            for y in range(rect.height):
                ratio = y / rect.height
                r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
                g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
                b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
                pygame.draw.line(
                    surface,
                    (r, g, b),
                    (rect.x, rect.y + y),
                    (rect.x + rect.width, rect.y + y),
                )
        else:
            for x in range(rect.width):
                ratio = x / rect.width
                r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
                g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
                b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
                pygame.draw.line(
                    surface,
                    (r, g, b),
                    (rect.x + x, rect.y),
                    (rect.x + x, rect.y + rect.height),
                )

    @staticmethod
    def draw_particle(surface, pos, color, size, alpha=255):
        s = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*color, alpha), (size, size), size)
        surface.blit(
            s, (pos[0] - size, pos[1] - size), special_flags=pygame.BLEND_ALPHA_SDL2
        )

    @staticmethod
    def draw_modern_button(
        surface, rect, text, font, bg_color, text_color, hover=False
    ):
        if hover:
            bg_color = tuple(min(255, c + 20) for c in bg_color)

        Graphics.draw_shadow_rect(surface, rect, bg_color)

        border_rect = pygame.Rect(
            rect.x - 2, rect.y - 2, rect.width + 4, rect.height + 4
        )
        pygame.draw.rect(surface, (255, 255, 255, 50), border_rect, 2)

        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        surface.blit(text_surface, text_rect)
