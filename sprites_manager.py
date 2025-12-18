import pygame
import os


class SpritesManager:
    def __init__(self):
        self.sprites = {}
        self.load_sprites()

    def load_sprites(self):
        sprite_dir = "sprites"

        try:
            self.sprites["hero"] = pygame.image.load(
                os.path.join(sprite_dir, "heroi.png")
            ).convert_alpha()

            for i in range(1, 5):
                sprite_name = f"inimigo{i}"
                sprite_path = os.path.join(sprite_dir, f"inimigo{i}.png")
                self.sprites[sprite_name] = pygame.image.load(
                    sprite_path
                ).convert_alpha()

            for i in range(1, 4):
                sprite_name = f"deco{i}"
                sprite_path = os.path.join(sprite_dir, f"deco{i}.png")
                self.sprites[sprite_name] = pygame.image.load(
                    sprite_path
                ).convert_alpha()

            menu_path = os.path.join(sprite_dir, "menu.png")
            if os.path.exists(menu_path):
                self.sprites["menu"] = pygame.image.load(menu_path).convert_alpha()

            morreu_path = os.path.join(sprite_dir, "morreu.png")
            if os.path.exists(morreu_path):
                self.sprites["morreu"] = pygame.image.load(morreu_path).convert_alpha()

            creditos_path = os.path.join(sprite_dir, "creditos.png")
            if os.path.exists(creditos_path):
                self.sprites["creditos"] = pygame.image.load(
                    creditos_path
                ).convert_alpha()

        except pygame.error as e:
            print(f"Erro ao carregar sprites: {e}")
            raise

    def get_sprite(self, name):
        return self.sprites.get(name)

    def get_sprite_size(self, name):
        sprite = self.sprites.get(name)
        if sprite:
            return sprite.get_size()
        return (0, 0)

    def scale_sprite(self, name, width, height):
        sprite = self.sprites.get(name)
        if sprite:
            return pygame.transform.scale(sprite, (width, height))
        return None
