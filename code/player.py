import pygame
from import_anim import import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, bariers, enemies, group):
        super().__init__(group)
        self.bariers = bariers
        self.enemies = enemies
        self.animations = None
        self.import_assets()
        self.cur_frame = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.cur_frame]
        self.rect = self.image.get_rect(topleft=pos)

        # Движение игрока
        self.cur_x_pos = 0
        self.direction = pygame.math.Vector2()
        self.speed = 6
        self.speed_decrement = 0.05
        self.gravity = 0.7
        self.jump_power = -21
        self.double_jump = True

        # Статус игрока
        self.status = 'idle'
        self.look_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
        self.stop_running = False
        self.dashing = False

        # Рывок игрока
        self.dash_time = 5
        self.dash_speed = 6
        self.dash_cooldown = 50
        self.dash_cd_timer = 0
        self.dash_timer = self.dash_time

    # Импорт спрайтов для анимаций
    def import_assets(self):
        path = '../sprites/player/'
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': [], 'jump_to_fall': [], 'run_end': [],
                           'dash_g': [], 'dash_a': []}

        for animation in self.animations.keys():
            full_path = path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations[self.status]

        self.cur_frame += self.animation_speed
        if self.cur_frame >= len(animation):
            self.cur_frame = 0

        temp = animation[int(self.cur_frame)]
        if self.look_right:
            self.image = temp
        else:
            self.image = pygame.transform.flip(temp, True, False)

        # Обновление rect
        if self.on_ground:
            if self.on_right:
                self.rect = self.image.get_rect(right=self.rect.right, bottom=self.rect.bottom)
            elif self.on_left:
                self.rect = self.image.get_rect(left=self.rect.left, bottom=self.rect.bottom)
            else:
                self.rect = self.image.get_rect(centerx=self.rect.centerx, bottom=self.rect.bottom)
        if self.on_ceiling:
            if self.on_right:
                self.rect = self.image.get_rect(right=self.rect.right, top=self.rect.top)
            elif self.on_left:
                self.rect = self.image.get_rect(left=self.rect.left, top=self.rect.top)
            else:
                self.rect = self.image.get_rect(centerx=self.rect.centerx, top=self.rect.top)
        if not (self.on_ground or self.on_ceiling):
            if self.on_right:
                self.rect = self.image.get_rect(right=self.rect.right, centery=self.rect.centery)
            elif self.on_left:
                self.rect = self.image.get_rect(left=self.rect.left, centery=self.rect.centery)
            else:
                if self.look_right:
                    self.rect = self.image.get_rect(left=self.rect.left, centery=self.rect.centery)
                else:
                    self.rect = self.image.get_rect(right=self.rect.right, centery=self.rect.centery)

    # Получение статуса игрока
    def get_status(self):
        # if self.dashing:
        #     if self.on_ground:
        #         self.status = 'dash_g'
        #     else:
        #         self.status = 'dash_a'
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 6:
            self.status = 'fall'
        elif 2 < self.direction.y < 6:
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

    # Получение нажатий клавиш и их обработка
    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] and not self.dashing:
            self.direction.x = -1
            self.look_right = False
            self.stop_running = False
        elif keys[pygame.K_d] and not self.dashing:
            self.direction.x = 1
            self.look_right = True
            self.stop_running = False
        elif not self.dashing and not (keys[pygame.K_d] or keys[pygame.K_a]):
            if self.direction.x != 0:
                if self.direction.x > 0:
                    self.direction.x -= self.speed_decrement
                elif self.direction.x < 0:
                    self.direction.x += self.speed_decrement
                if abs(self.direction.x) < 0.001:
                    self.direction.x = 0
                self.stop_running = True
            if self.direction.x == 0:
                self.stop_running = False

        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()

        if keys[pygame.K_LSHIFT] and not self.dash_cd_timer:
            self.dash()

    # Функция прыжка
    def jump(self):
        self.direction.y = self.jump_power

    # Функция рывка
    def dash(self):
        self.dash_cd_timer = self.dash_cooldown
        self.dash_timer = self.dash_time
        if self.look_right:
            self.direction.x = self.dash_speed
        else:
            self.direction.x = -self.dash_speed
        self.direction.y = 0
        self.dashing = True

    # Функция обновления продолжительности рывка
    def update_dash_time(self):
        if self.dashing:
            if self.dash_timer:
                self.dash_timer -= 1
            if self.dash_timer == 0:
                self.dashing = False
                if self.look_right:
                    self.direction.x = 1
                else:
                    self.direction.x = -1

    # Функция обновления таймера перезарядки рывка
    def update_dash_cooldown(self):
        if self.dash_cd_timer != 0:
            self.dash_cd_timer -= 1
        if self.dash_cd_timer == 0:
            self.dash_timer = self.dash_time

    # Проверка на столкновение с "землей"
    def movement_collision(self, orientation):
        if orientation == 'hor':
            for sprite in self.bariers:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0:
                        if self.rect.right < sprite.rect.right:
                            self.rect.right = sprite.rect.left
                            self.on_right = True
                            self.cur_x_pos = self.rect.right
                    if self.direction.x < 0:
                        self.rect.left = sprite.rect.right
                        self.on_left = True
                        self.cur_x_pos = self.rect.left
                    self.dashing = False
                    self.dash_timer = 0
                    self.direction.x = 0
            if self.on_left and (self.rect.left < self.cur_x_pos or self.direction.x > 0):
                self.on_left = False
            if self.on_right and (self.rect.right > self.cur_x_pos or self.direction.x < 0):
                self.on_right = False
        if orientation == 'ver':
            for sprite in self.bariers:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y > 0:
                        if self.rect.bottom < sprite.rect.bottom:
                            self.rect.bottom = sprite.rect.top
                            self.on_ground = True
                            self.double_jump = True
                        else:
                            self.rect.top = sprite.rect.bottom
                            self.on_ceiling = True
                    if self.direction.y < 0:
                        self.rect.top = sprite.rect.bottom
                        self.on_ceiling = True
                    self.direction.y = 0
            if self.on_ground and self.direction.y < 0 or self.direction.y > 1:
                self.on_ground = False
            if self.on_ceiling and self.direction.y > 0:
                self.on_ceiling = False

    # Функция передвижения
    def move(self, speed):
        self.rect.x += self.direction.x * speed
        self.movement_collision('hor')
        self.rect.y += self.direction.y
        self.movement_collision('ver')

    # Функция гравитации игрока
    def apply_gravity(self):
        self.direction.y += self.gravity

    # Обновление даннных игрока
    def update(self):
        self.get_input()
        if not self.dashing:
            self.apply_gravity()
        self.move(self.speed)
        self.get_status()
        self.animate()
        self.update_dash_cooldown()
        self.update_dash_time()

    def get_current_pos(self):
        return self.rect.topleft
