import random

import pygame
import math
import sys
from button import Button
from player_class import Player
from platform_class import Platform
from pygame import mixer
import time

pygame.init()
mixer.init()
mixer.music.load("pygamemusic.mp3")
mixer.music.set_volume(0.4)

clock = pygame.time.Clock()

SCREEN_WIDTH = 720
SCREEN_HEIGHT = 360
ramen_rect = pygame.Rect(random.randint(0, SCREEN_WIDTH - 50), random.randint(0, SCREEN_HEIGHT - 50), 50, 50)
start_time = time.time()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Scroll Demo")
ramenimg = pygame.image.load('images/ramen.png')
start_button = Button(290, 260, 150, 50, (190, 0, 50), (220, 20, 60), "Start", 40, 30, 7)

continue_button = Button(260, 230, 200, 40, (105, 105, 105), (0, 0, 0), "Continue", 30, 40, 7)

play_button = Button(260, 100, 200, 60, (105, 105, 105), (0, 0, 0), "Play", 30, 70, 15)
leaderboard_button = Button(260, 170, 200, 60, (105, 105, 105), (0, 0, 0), "Leaderboard", 30, 19, 15)
back_button1 = Button(260, 240, 200, 60, (105, 105, 105), (0, 0, 0), "Back", 30, 70, 15)

resume_button = Button(260, 100, 200, 60, (105, 105, 105), (0, 0, 0), "Resume", 30, 50, 15)
menu_button = Button(260, 170, 200, 60, (105, 105, 105), (0, 0, 0), "Menu", 30, 70, 15)
quit_button = Button(260, 240, 200, 60, (105, 105, 105), (0, 0, 0), "Quit", 30, 70, 15)

pause_button = Button(680, 20, 30, 20, (105, 105, 105), (0, 0, 0), "Pause", 10, 2, 2)

back_button2 = Button(100, 20, 50, 25, (105, 105, 105), (0, 0, 0), "Back", 20, 4, 2)
ramen_x, ramen_y = random.randint(0, SCREEN_WIDTH - 50), random.randint(0, SCREEN_HEIGHT - 50)

def starting_screen():
    running = True
    while running:
        bg = pygame.image.load("images/starting.jpg").convert()
        bg = pygame.transform.scale(bg, (720, 360))
        rect = bg.get_rect()
        screen.blit(bg, rect)
        start_button.draw(screen)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if start_button.check_for_input(pos):
                    running = False
                    player_username_screen()
        pygame.display.update()
    return


def player_username_screen():
    bg = pygame.image.load("images/menu_bg.png").convert_alpha()
    bg = pygame.transform.scale(bg, (720, 360))
    rect = bg.get_rect()
    active = False
    base_font = pygame.font.Font(None, 32)
    color = pygame.Color('gray15')
    user_text = ''
    input_rect = pygame.Rect(200, 150, 300, 50)
    running = True
    while running:
        screen.blit(bg, rect)
        continue_button.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if input_rect.collidepoint(event.pos):
                    active = True
                if continue_button.check_for_input(pos):
                    running = False
                    update_score(user_text, 0)
                    main_menu()
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        user_text += event.unicode

        if active:
            color = pygame.Color('lightskyblue3')
        else:
            color = pygame.Color('gray15')

        pygame.draw.rect(screen, color, input_rect, 2)
        text_surface = base_font.render(user_text, True, (255, 255, 255))
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
        pygame.display.update()
    return

def main_menu():
    bg = pygame.image.load("images/menu_bg.png").convert_alpha()
    bg = pygame.transform.scale(bg, (720, 360))
    rect = bg.get_rect()
    screen.blit(bg, rect)
    running = True
    while running:
        play_button.draw(screen)
        leaderboard_button.draw(screen)
        back_button1.draw(screen)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if play_button.check_for_input(pos):
                    running = False
                    play()
                if leaderboard_button.check_for_input(pos):
                    running = False
                    display_leaderboard()
                if back_button1.check_for_input(pos):
                    running = False
                    player_username_screen()
        pygame.display.update()
    return

def pause_menu():
    screen.fill('white', (20, 20, 680, 320))
    paused = True
    while paused:
        pygame.mixer.music.pause()
        resume_button.draw(screen)
        menu_button.draw(screen)
        quit_button.draw(screen)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if resume_button.check_for_input(pos):
                    paused = False
                    pygame.mixer.music.unpause()
                if menu_button.check_for_input(pos):
                    paused = False
                    main_menu()
                    return
                if quit_button.check_for_input(pos):
                    starting_screen()
                    return
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    paused = False

        pygame.display.update()
    return


def update_score(name,score):
    global lines
    with open("leaderboard.txt","r") as f:
        lines = f.readlines()
        f.close()
    with open("leaderboard.txt", 'w') as file:
        if len(lines) > 0:
            for i in range(len(lines)):
                if lines[i].find(name) != -1:
                    x = lines[i].split(",")
                    if int(x[1]) > score:
                        score = x[1]
                    lines[i] = name + "," + str(score) + "\n"
                    file.writelines(lines)
                    return
        lines.append(name + "," + str(score)+"\n")
        file.writelines(lines)
        file.close()
    return

def sort_leaderboard():
    tupleScores = []
    with open("leaderboard.txt", "r") as f:
        lines = f.readlines()
    for line in lines:
        x = line.split(",")
        x[1] = int(x[1])
        tupleScores.append(tuple(x))
    f.close()
    tupleScores.sort(key = lambda x : x[1], reverse=True)
    with open("leaderboard.txt","w") as f:
        f.writelines(lines)
        f.close()
    return tupleScores

def display_leaderboard():
    scores = sort_leaderboard()
    screen.fill((255,0,0))
    font1 = pygame.font.SysFont('freesansbold.ttf', 40)
    font2 = pygame.font.SysFont('didot.ttc', 30)
    leaderboardTitle = font1.render("Top 10 Scores", True, (255,255,255))
    screen.blit(leaderboardTitle,(250,15))
    running = True
    while running:
        back_button2.draw(screen)
        for i in range(len(scores)):
            if i <= 10:
                user = scores[i]
                (name,score) = user
                nameDisplay = font2.render(str(i+1)+".  "+name,True,(255,255,255))
                screen.blit(nameDisplay, (250, 60+i*30 ))
                scoreDisplay = font2.render(str(score),True,(255,255,255))
                screen.blit(scoreDisplay,(420, 60+i*30))
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if back_button2.check_for_input(pos):
                        running = False
                        main_menu()
        pygame.display.update()
    return


def play():
    # Load up background
    bg = pygame.image.load("images/clouds.jpg").convert()
    bg_width = bg.get_width()
    bg_rect = bg.get_rect()

    # Scroll speed initially set to 0
    scrollSpeed = 0
    # Rounds up the amount of tiles shown on screen
    tiles = math.ceil(SCREEN_WIDTH / bg_width) + 1

    # Define variables
    playerx = 100
    playery = 200
    player_speed = 5
    player_jump_height = 15
    running = True
    font = pygame.font.Font(None, 36)

    # Create player object
    player = Player(playerx, playery, player_speed, player_jump_height)
    platform = Platform()

    # Start time
    start_time = time.time()
    countdown_time = 180  # Countdown time in seconds

    # Game loop
    pygame.mixer.music.play()
    running = True
    while running:
        clock.tick(50)

        # should look smt like this if it works
        # ---------------------------------------------------------------------
        """
        for f in ramenPos:
            if f.colliderect(player_rect):
                ramenPos.remove(f)
                update_score()
        """
        # ---------------------------------------------------------------------
        # Calculate elapsed time
        elapsed_time = time.time() - start_time
        remaining_time = countdown_time - elapsed_time
        if remaining_time <= 0:
            remaining_time = 0

        # Check if time is up
        if elapsed_time >= countdown_time:
            starting_screen()

        for i in range(0, tiles):
            screen.blit(bg, (i * bg_width + scrollSpeed, 0))

        scrollSpeed -= 5
        if abs(scrollSpeed) > bg_width:
            scrollSpeed = 0

        pause_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pause_button.check_for_input(pos):
                    pause_menu()

        platform_positions = [
            (565, 280, 3),
            (280, 280, 6),
            (-160, 250, 13),
            (672, 250, 10),
            (450, 280, 3),
            (120, 280, 3),
            (235, 250, 2),
            (380, 250, 2),
            (-160, 340, 60),
            (120, 190, 3),
            (-160, 150, 13),
            # !!!staircase so collision is kinda ehhh u can decide if u want items on that or not
            (145, 115, 1),
            (161, 105, 1),
            (177, 95, 1),
            # stair case ends!!!
            (210, 95, 1),
            (419, 95, 1),
            # !!!wall do not let items spawn ontop
            (210, 111, 1),
            (210, 127, 1),
            (210, 143, 1),
            (210, 159, 1),
            (419, 111, 1),
            (419, 143, 1),
            (419, 159, 1),
            (419, 127, 1),
            # wall Ends!!!
            (242, 127, 10),
            (306, 65, 2),
            (512, 190, 6),
            (672, 150, 10),
            (607, 132, 1),
            (546, 120, 1),
            (495, 98, 1)

        ]
        for i in platform_positions:
            platform.draw(i[0], i[1], i[2])

        player.draw()
        player.update_animation()
        player.handle_movement()
        player.apply_gravity()
        player.check_collision()

        minutes = int(remaining_time // 60)
        seconds = int(remaining_time % 60)

        # Render countdown timer text
        timer_text = font.render(f" {minutes}:{seconds} seconds", True, (255, 255, 255))
        screen.blit(timer_text, (10, 10))
        screen.blit(ramenimg, (ramen_x, ramen_y))
        pygame.display.flip()
        clock.tick(20)

    pygame.quit()


if __name__ == "__main__":
    starting_screen()