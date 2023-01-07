import pygame
from import_anim import import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, bariers, enemies):
        super().__init__()
        self.bariers = bariers
        self.enemies = enemies
        self.import_assets()
        self.cur_frame = 0
        self.animation_speed = 0.15
        self.image = pygame.Surface((32, 52))
        self.image.fill('red')
        self.rect = self.image.get_rect(topleft=pos)
        self.mask = pygame.mask.from_surface(self.image)

        # Движение игрока
        self.cur_x_pos = 0
        self.direction = pygame.math.Vector2()
        self.speed = 7
        self.speed_decrement = 0.05
        self.gravity = 0.7
        self.jump_power = -21

        # Статус игрока
        self.status = 'idle'
        self.look_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
        self.stop_running = False

    def import_assets(self):
        path = '../sprites/player/'
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': [], 'jump_to_fall': [], 'run_end': []}

        for animation in self.animations.keys():
            full_path = path + animation
            self.animations[animation] = import_folder(full_path)

    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 6:
            self.status = 'fall'
        elif 1 < self.direction.y < 6:
            self.status = 'jump_to_fall'
        else:
            if self.direction.x != 0 and self.on_ground:
                if self.stop_running:
                    self.status = 'run_end'
                else:
                    self.status = 'run'
            else:
                self.status = 'idle'
        return self.status

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            if self.direction.x < 1:
                self.direction.x += self.speed_decrement
            if self.direction.x > 1:
                self.direction.x = 1
            self.look_right = True
            self.stop_running = False
        elif keys[pygame.K_a]:
            if self.direction.x > -1:
                self.direction.x -= self.speed_decrement
            if self.direction.x < -1:
                self.direction.x = -1
            self.look_right = False
            self.stop_running = False
        else:
            if self.direction.x != 0:
                if self.look_right and self.direction.x > 0:
                    self.direction.x -= self.speed_decrement
                elif not self.look_right and self.direction.x < 0:
                    self.direction.x += self.speed_decrement
                if abs(self.direction.x) < 0.0001:
                    self.direction.x = 0
                self.stop_running = True
            elif self.direction.x == 0:
                self.stop_running = False

        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()

    def jump(self):
        self.direction.y = self.jump_power

    def movement_collision(self, orientation):
        if orientation == 'hor':
            for sprite in self.bariers:
                if pygame.sprite.collide_mask(self, sprite):
                    if self.direction.x > 0:
                        self.rect.right = sprite.rect.left
                        self.on_right = True
                        self.cur_x_pos = self.rect.right
                        self.direction.x = 0
                    if self.direction.x < 0:
                        self.rect.left = sprite.rect.right
                        self.on_left = True
                        self.cur_x_pos = self.rect.left
                        self.direction.x = 0
            if self.on_left and (self.rect.left < self.cur_x_pos or self.direction.x >= 0):
                self.on_left = False
            if self.on_right and (self.rect.left > self.cur_x_pos or self.direction.x <= 0):
                self.on_right = False
        if orientation == 'ver':
            for sprite in self.bariers:
                if pygame.sprite.collide_mask(self, sprite):
                    if self.direction.y > 0:
                        self.rect.bottom = sprite.rect.top
                        self.direction.y = 0
                        self.on_ground = True
                    if self.direction.y < 0:
                        self.rect.top = sprite.rect.bottom
                        self.direction.y = 0
                        self.on_ceiling = True
            if self.on_ground and self.direction.y < 0 or self.direction.y > 1:
                self.on_ground = False
            if self.on_ceiling and self.direction.y > 0:
                self.on_ceiling = False

    def move(self, speed):
        if self.on_ground or self.on_ceiling:
            self.rect.x += self.direction.x * speed
            self.movement_collision('hor')
            self.rect.y += self.direction.y
            self.movement_collision('ver')
        else:
            self.rect.y += self.direction.y
            self.movement_collision('ver')
            self.rect.x += self.direction.x * speed
            self.movement_collision('hor')

    def apply_gravity(self):
        self.direction.y += self.gravity

    def update(self):
        self.get_input()
        self.apply_gravity()
        self.move(self.speed)
        print(self.get_status())

