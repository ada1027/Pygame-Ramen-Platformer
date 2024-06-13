import random

import pygame
from platform_class import platforms

screen = pygame.display.set_mode((720, 360))
run_animation = []
jump_animation = []
idle_animation = []
run_animation_left = []

for i in range(0, 6):
    run_animation.append((pygame.image.load(f'images/adventurer-run-0{i}.png')))
for i in range(0, 4):
    jump_animation.append((pygame.image.load(f'images/adventurer-jump-0{i}.png')))
for i in range(2, -1, -1):
    jump_animation.append((pygame.image.load(f'images/adventurer-jump-0{i}.png')))
for i in range(0, 4):
    idle_animation.append((pygame.image.load(f'images/adventurer-idle-0{i}.png')))
for i in range(0, 6):
    run_animation_left.append((pygame.image.load(f'images/adventurer-run-left-0{i}.png')))
SCREEN_WIDTH = 720
SCREEN_HEIGHT = 360
ramen_rect = pygame.Rect(random.randint(0, SCREEN_WIDTH - 50), random.randint(0, SCREEN_HEIGHT - 50), 50, 50)
# Ramen collectibles
ramenimg = pygame.image.load('images/ramen.png')



class Player:
    def __init__(self, x, y, speed, jump_height):
        self.x = x
        self.y = y
        self.speed = speed
        self.jump_height = jump_height
        self.run_frame = 0
        self.jump_frame = 0
        self.idle_frame = 0
        self.run_animation = run_animation
        self.jump_animation = jump_animation
        self.idle_animation = idle_animation
        self.run_animation_left = run_animation_left
        self.run_right = False
        self.run_left = False
        self.jump = False
        self.idle = True
        self.rect = None
        self.y_velocity = 0
        self.gravity = 2
        self.character = pygame.image.load('images/adventurer-run-03.png')
        self.rect = self.character.get_rect()
        self.jump_count = 0

    def draw(self):
        screen.blit(self.character, (self.rect.x, self.rect.y))

    def update_animation(self):
        if self.jump:
            self.character = self.jump_animation[self.jump_frame]
        elif self.run_right:
            self.character = self.run_animation[self.run_frame]
        elif self.run_left:
            self.character = self.run_animation_left[self.run_frame]
        else:
            self.character = self.idle_animation[self.idle_frame]

    def handle_movement(self):
        keystate = pygame.key.get_pressed()
        if self.rect.x < 0:
            self.rect.x = 700
        if self.rect.x > 720:
            self.rect.x = 0
        if self.rect.y > 360:
            self.rect.y = 0
        if keystate[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.run_left = True
            self.run_right = False
            self.jump = False
            self.idle = False

        if keystate[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.run_left = False
            self.run_right = True
            self.jump = False
            self.idle = False

        if keystate[pygame.K_UP]:
            if not self.jump:
                self.jump = True
                self.run_left = False
                self.run_right = False
                self.idle = False

        if not (keystate[pygame.K_LEFT] or keystate[pygame.K_RIGHT] or keystate[pygame.K_SPACE]):
            self.run_right = False
            self.run_left = False
            self.jump = False
            self.idle = True

        if self.jump:
            self.jump_frame += 1
            if self.jump_frame >= len(self.jump_animation):
                self.jump_frame = 0

        if self.run_right or self.run_left:
            self.run_frame += 1
            if self.run_frame >= len(self.run_animation):
                self.run_frame = 0

        if not self.jump and not self.run_right and not self.run_left:
            self.idle_frame += 1
            if self.idle_frame >= len(self.idle_animation):
                self.idle_frame = 0

    def apply_gravity(self):
        if not self.jump or self.jump_count > 0:

            self.y_velocity += self.gravity
            self.rect.y += self.y_velocity
        elif self.jump and self.jump_count == 0:
            old_y = 0
            old_y = self.y
            self.y_velocity = -self.jump_height
            self.rect.y += self.y_velocity
            self.jump_count += 1
            if self.rect.y >= self.jump_height + old_y:
                self.jump = False

    def get_rect(self):
        player_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)
        return player_rect

    def check_collision(self):
        if self.rect.colliderect(ramen_rect):
            new_x, new_y = random.randint(0, SCREEN_WIDTH - 50), random.randint(0, SCREEN_HEIGHT - 50)
            ramen_rect.topleft = (new_x, new_y)
        player_rect = self.get_rect()
        for platform in platforms:
            platform_rect = pygame.Rect(platform[0], platform[1], 1, 20)
            if player_rect.colliderect(platform_rect):
                if self.rect.y + self.rect.height >= platform_rect.bottom and self.y_velocity != 0:
                    self.rect.y = platform_rect.bottom
                    self.jump = False
                    self.y_velocity = 0
                elif self.y_velocity > 0:
                    self.rect.y = platform_rect.y - player_rect.height
                    self.y_velocity = 0
                    self.jump = False
                    self.jump_count = 0