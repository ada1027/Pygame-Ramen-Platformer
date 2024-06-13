import pygame
class Player:
    def __init__(self, x, y, screen, speed, jump_height,run_animation,jump_animation,idle_animation):
        self.x = x
        self.y = y
        self.screen = screen
        self.speed = speed
        self.jump_height = jump_height
        self.run_frame = 0
        self.jump_frame = 0
        self.idle_frame = 0
        self.run_animation = run_animation
        self.jump_animation = jump_animation
        self.idle_animation = idle_animation
        self.run = False
        self.jump = False
        self.idle = True
        self.rect = None
        self.y_velocity = 0
        self.gravity = 2
        self.character = pygame.image.load('adventurer-run-03.png')

    def draw(self):
        self.screen.blit(self.character, (self.x, self.y))

    def update_animation(self):
        if self.jump:
            self.character = self.jump_animation[self.jump_frame]
        elif self.run:
            self.character = self.run_animation[self.run_frame]
        else:
            self.character = self.idle_animation[self.idle_frame]

    def collision(self):
        self.rect = self.character.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def movement(self):
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.x -= self.speed
            self.run = True
            self.jump = False
            self.idle = False

        if keystate[pygame.K_RIGHT]:
            self.x += self.speed
            self.run = True
            self.jump = False
            self.idle = False

        if keystate[pygame.K_SPACE]:
            if not self.jump:
                self.y += self.jump_height
                self.jump = True
                self.run = False
        
        if not (keystate[pygame.K_LEFT] or keystate[pygame.K_RIGHT] or keystate[pygame.K_SPACE]):
            self.run = False
            self.jump = False
            self.idle = True

        if self.jump:
            self.jump_frame += 1
            if self.jump_frame >= len(self.jump_animation):
                self.jump_frame = 0

        if self.run:
            self.run_frame += 1
            if self.run_frame >= len(self.run_animation):
                self.run_frame = 0
              
        if not self.jump and not self.run:
            self.idle_frame += 1
            if self.idle_frame >= len(self.idle_animation):
                self.idle_frame = 0