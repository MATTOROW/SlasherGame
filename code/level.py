import pygame
from random import randint
from settings import *
from tile import Tile
from player import Player
from background_particles import BackgroundParticles


class Level:
    def __init__(self, level_data):
        # Получение экрана
        self.display_surface = pygame.display.get_surface()
        self.level_map, self.level_width, self.level_height = level_data
        self.camera = None

        # Создание групп спрайтов
        self.all_sprites = pygame.sprite.Group()
        self.tile_group = pygame.sprite.Group()
        self.entities = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.background_part = pygame.sprite.Group()

        self.create_map()

        for _ in range(randint(100, 500)):
            self.create_background_part()

    def create_map(self):
        for r_index, row in enumerate(self.level_map):
            for c_index, col in enumerate(row):
                x = TILESIZE * c_index
                y = TILESIZE * r_index
                if col == 'x':
                    Tile((x, y), TILESIZE, [self.all_sprites, self.tile_group])
                if col == 'p':
                    player_spr = Player((x, y), self.tile_group, self.entities)
                    self.player.add(player_spr)
                    self.all_sprites.add(player_spr)
                    # Инициация камеры
                    self.camera = LevelCamera(self.player.sprite, self.all_sprites, self.display_surface)

    def create_background_part(self):
        player_x, player_y = self.player.sprite.get_current_pos()
        display_width, display_height = self.display_surface.get_width(), self.display_surface.get_height()
        borderl_x_left = player_x - display_width - 100
        borderl_x_right = player_x + display_width // 2
        borderl_y_top = player_y - display_height // 2
        borderl_y_bottom = player_y + display_height // 2
        borderb_y_bottom = player_y + display_height + 200
        borderb_y_top = player_y + display_height // 2
        broderr_x_left = player_x + display_width // 2
        borderr_x_right = player_x + display_width + 100
        bordert_y_bottom = player_y - display_height // 2
        bordert_y_top = player_y - display_height - 200
        LT_x_pos = randint(borderl_x_left, borderl_x_right)
        LT_y_pos = randint(-bordert_y_bottom, -bordert_y_top)
        BackgroundParticles([self.all_sprites, self.background_part], (LT_x_pos, LT_y_pos))

    def update_level(self):
        # Обновление спрайтов
        self.player.update()

        self.create_background_part()
        self.background_part.update()

        # Обновление камеры
        self.camera.update()
        self.camera.sprites_shift()
        self.camera.blit_sprites()


class LevelCamera:
    def __init__(self, target, objects, surface_data):
        self.target = target
        self.objects = objects
        self.surface = surface_data
        self.surface_data = (surface_data.get_width(), surface_data.get_height())
        self.surf_vect = pygame.math.Vector2(self.surface_data[0] // 2, self.surface_data[1] // 2)
        self.camera_vect = pygame.math.Vector2(self.target.rect.center)
        self.heading = None

    def update(self):
        self.heading = self.target.rect.center - self.camera_vect
        self.camera_vect += self.heading * 0.04

    def sprites_shift(self):
        offset = self.surf_vect - self.camera_vect
        offset = pygame.math.Vector2((int(offset[0]), int(offset[1])))
        return offset

    def blit_sprites(self):
        offset = self.sprites_shift()
        for sprite in self.objects:
            self.surface.blit(sprite.image, sprite.rect.topleft + offset + pygame.math.Vector2(0, 64))

    def change_target(self, target):
        self.target = target
