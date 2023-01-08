import pygame, sys
from settings import *
from level import Level


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.state = 'RUNNING'

        self.level = Level((LEVEL_MAP, LEVEL_WIDTH, LEVEL_HEIGHT))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        if self.state == 'RUNNING':
                            self.state = 'PAUSE'
                        else:
                            self.state = 'RUNNING'

            self.screen.fill('#e6e6e6')
            if self.state == 'RUNNING':
                self.level.update_level()
            self.level.camera.blit_sprites()
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
