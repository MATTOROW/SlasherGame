import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size, group):
        super().__init__(group)
        self.image = pygame.Surface((size, size))
        self.image.fill('grey')
        self.rect = self.image.get_rect(topleft=pos)
        # self.mask = pygame.mask.from_surface(self.image)