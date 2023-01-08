import pygame
from random import randint


class BackgroundParticles(pygame.sprite.Sprite):
    def __init__(self, groups, pos):
        super().__init__(groups)
        size = randint(5, 15)
        color_sheme = randint(102, 153)
        speed = randint(1, 3)
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=pos)
        self.image.fill(pygame.color.Color((color_sheme, 0, 0)))
        self.speed = speed

    def move(self):
        self.rect.y += self.speed

    def update(self):
        self.move()
