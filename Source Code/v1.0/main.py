import pygame
import sys
import os
import random
from pathlib import Path
pygame.init()
pygame.mixer.init()
pygame.font.init()


# Colors
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)
light_red = (255, 102, 102)
score_background_color = (9, 153, 163)

# Creating Game Window
gameWindow = pygame.display.set_mode()

window_size = pygame.display.get_window_size()
screen_width = window_size[0]
screen_height = window_size[1]

# Game Title
pygame.display.set_caption("Snakes (By Divyanshu)")
pygame.display.update()

# Background Image
welcome_background = pygame.image.load("gallery/images/welcome.jpeg")
welcome_background = pygame.transform.scale(welcome_background, (screen_width, screen_height)).convert_alpha()

game_over_background = pygame.image.load("gallery/images/game_over.jpg")
game_over_background = pygame.transform.scale(game_over_background, (screen_width, screen_height)).convert_alpha()

gradient_background = pygame.image.load("gallery/images/gradient.jpeg")
gradient_background = pygame.transform.scale(gradient_background, (screen_width, screen_height)).convert_alpha()

cheats_reference = pygame.image.load("gallery/images/cheats.jpg")
cheats_reference = pygame.transform.scale(cheats_reference, (screen_width, screen_height)).convert_alpha()

paused_screen = pygame.image.load("gallery/images/paused.jpg")
paused_screen = pygame.transform.scale(paused_screen, (screen_width, screen_height)).convert_alpha()

# Background Music and Sound Effects
welcome_music = pygame.mixer.Sound("gallery/sounds/main_menu.mp3")
while_playing_music = pygame.mixer.Sound("gallery/sounds/while_playing.mp3")
while_playing_music.set_volume(0.3)
game_over_sound = pygame.mixer.Sound("gallery/sounds/game_over.mp3")
pygame.mixer.music.load("gallery/sounds/ping.mp3")
eat_sound = pygame.mixer.Sound("gallery/sounds/eat.mp3")

# Creating Clock
clock = pygame.time.Clock()
fps = 60

# Function to display score
font = pygame.font.Font("gallery/fonts/Baloo_Bhai_2_Medium.ttf", 35)


def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])


# Function to plot snakes
def plot_snake(game_window, color, snk_list, snk_size):
    for x, y in snk_list:
        pygame.draw.circle(game_window, color, [x, y], snk_size)


# Checking and Getting High Score
if not os.path.exists(Path.home()/"Saved Games"/"Snakes"):
    os.mkdir(str(Path.home()/"Saved Games"/"Snakes"))

high_score_path = str(Path.home()/"Saved Games"/"Snakes"/"high_score.txt")

if not os.path.exists(Path.home()/"Saved Games"/"Snakes"/"high_score.txt"):
    with open(high_score_path, "w") as hs:
        hs.write("0")

with open(high_score_path, "r") as file:
    high_score = file.read()

# Cheat Codes
activated = ""
cheats = ""
reset = ""

immortality = False
immortal = ""

century = ""

malnutrition = ""
snake_length_increase = 4

magnet = ""
near_food = 7


# Welcome Screen
def welcome():
    exit_game = False
    blit_what = welcome_background
    global activated, cheats, immortal, immortality, century, malnutrition, snake_length_increase, near_food, magnet, high_score, reset
    welcome_music.play(loops=-1)
    while not exit_game:
        gameWindow.blit(blit_what, [0, 0])
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                exit_game = True

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and "cheats" not in cheats:
                exit_game = True
                welcome_music.stop()
                while_playing_music.play(loops=-1)
                game_loop()

            if event.type == pygame.KEYDOWN:
                activated += event.unicode.lower()
                cheats += event.unicode.lower()
                reset  += event.unicode.lower()
                if "immortal" in activated:
                    immortality = True
                    pygame.mixer.music.load("gallery/sounds/ping.mp3")
                    pygame.mixer.music.play()
                    activated = ""
                if "malnutrition" in activated and snake_length_increase > 1:
                    snake_length_increase -= 1
                    pygame.mixer.music.load("gallery/sounds/ping.mp3")
                    pygame.mixer.music.play()
                    activated = ""
                if "magnet" in activated:
                    near_food = 100
                    pygame.mixer.music.load("gallery/sounds/ping.mp3")
                    pygame.mixer.music.play()
                    activated = ""
                if "cheats" in cheats:
                    blit_what = cheats_reference
                    pygame.mixer.pause()
                    if event.key == pygame.K_RETURN:
                        blit_what = welcome_background
                        pygame.mixer.unpause()
                        cheats = ""
                if "reset" in reset:
                    high_score = 0
                    with open(high_score_path, "w") as f:
                        f.write(str(high_score))
                    reset = ""
                    cheats = ""
                    activated = ""
                    welcome_music.stop()
                    exit_game = True
                    welcome()
        pygame.display.update()
        clock.tick(fps)


def game_loop():
    # Game Specific Variables
    exit_game = False
    game_over = False
    game_started = False
    game_paused = False

    blit_what = gradient_background
    display_in_paused = paused_screen

    snake_x = 70
    snake_y = 100
    snake_size = 15

    velocity_x = 0
    velocity_y = 0
    initial_velocity = 5

    food_x = random.randint(50, screen_width - 50)
    food_y = random.randint(100, screen_height - 50)
    food_size = 13

    score = 0

    snake_list = [[45, 100], [50, 100], [55, 100], [60, 100], [65, 100]]
    snake_length = 5

    global activated, cheats, immortal, immortality, century, malnutrition, snake_length_increase, near_food, magnet, high_score, reset

    # Game Loop
    while not exit_game:
        if not game_paused:
            if game_over:
                while_playing_music.stop()
                with open(high_score_path, "w") as f:
                    f.write(str(high_score))
                gameWindow.blit(blit_what, [0, 0])
                if blit_what == game_over_background:
                    text_screen("Your score is " + str(score), light_red, 10, screen_height - 50)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        with open(high_score_path, "w") as f:
                            f.write(str(high_score))
                        exit_game = True

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        pygame.mixer.pause()
                        if score == int(high_score):
                            with open(high_score_path, "w") as f:
                                f.write(str(high_score))
                        game_paused = True

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and "cheats" not in cheats:
                        game_over_sound.stop()
                        while_playing_music.play(loops=-1)
                        game_loop()

                    if event.type == pygame.KEYDOWN:
                        activated += event.unicode.lower()
                        cheats += event.unicode.lower()
                        reset += event.unicode.lower()
                        if "immortal" in activated:
                            immortality = True
                            pygame.mixer.music.load("gallery/sounds/ping.mp3")
                            pygame.mixer.music.play()
                            activated = ""
                        if "century" in activated:
                            score += 100
                            snake_length += snake_length_increase * 10
                            if score > int(high_score):
                                high_score = score
                                with open(high_score_path, "w") as f:
                                    f.write(str(high_score))
                            pygame.mixer.music.load("gallery/sounds/ping.mp3")
                            pygame.mixer.music.play()
                            activated = ""
                        if "malnutrition" in activated and snake_length_increase > 1:
                            snake_length_increase -= 1
                            pygame.mixer.music.load("gallery/sounds/ping.mp3")
                            pygame.mixer.music.play()
                            activated = ""
                        if "magnet" in activated:
                            near_food = 100
                            pygame.mixer.music.load("gallery/sounds/ping.mp3")
                            pygame.mixer.music.play()
                            activated = ""
                        if "cheats" in cheats:
                            blit_what = cheats_reference
                            pygame.mixer.pause()
                            if event.key == pygame.K_RETURN:
                                blit_what = game_over_background
                                pygame.mixer.unpause()
                                cheats = ""
                        if "reset" in reset:
                            high_score = 0
                            with open(high_score_path, "w") as f:
                                f.write(str(high_score))
                            reset = ""
                            cheats = ""
                            activated = ""
                            exit_game = True
                            welcome()
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        with open(high_score_path, "w") as f:
                            f.write(str(high_score))
                        exit_game = True

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        pygame.mixer.pause()
                        if score == int(high_score):
                            with open(high_score_path, "w") as f:
                                f.write(str(high_score))
                        game_paused = True

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT and "cheats" not in cheats:
                        velocity_x = initial_velocity
                        velocity_y = 0

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT and "cheats" not in cheats:
                        velocity_x = -initial_velocity
                        velocity_y = 0

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_UP and "cheats" not in cheats:
                        velocity_y = -initial_velocity
                        velocity_x = 0

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN and "cheats" not in cheats:
                        velocity_y = initial_velocity
                        velocity_x = 0

                    if not game_started:
                        if event.type == pygame.KEYDOWN \
                                and (event.key == pygame.K_UP or event.key == pygame.K_DOWN or
                                     event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT) \
                                and "cheats" not in cheats:
                            game_started = True
                    if event.type == pygame.KEYDOWN:
                        activated += event.unicode.lower()
                        cheats += event.unicode.lower()
                        reset += event.unicode.lower()
                        if "immortal" in activated:
                            immortality = True
                            pygame.mixer.music.load("gallery/sounds/ping.mp3")
                            pygame.mixer.music.play()
                            activated = ""
                        if "century" in activated:
                            score += 100
                            snake_length += snake_length_increase * 10
                            if score > int(high_score):
                                high_score = score
                                with open(high_score_path, "w") as f:
                                    f.write(str(high_score))
                            pygame.mixer.music.load("gallery/sounds/ping.mp3")
                            pygame.mixer.music.play()
                            activated = ""
                        if "malnutrition" in activated and snake_length_increase > 1:
                            snake_length_increase -= 1
                            pygame.mixer.music.load("gallery/sounds/ping.mp3")
                            pygame.mixer.music.play()
                            activated = ""
                        if "magnet" in activated:
                            near_food = 100
                            pygame.mixer.music.load("gallery/sounds/ping.mp3")
                            pygame.mixer.music.play()
                            activated = ""
                        if "cheats" in cheats:
                            blit_what = cheats_reference
                            pygame.mixer.pause()
                            if event.key == pygame.K_RETURN:
                                blit_what = gradient_background
                                pygame.mixer.unpause()
                                cheats = ""
                        if "reset" in reset:
                            high_score = 0
                            with open(high_score_path, "w") as f:
                                f.write(str(high_score))
                            reset = ""
                            cheats = ""
                            activated = ""
                            while_playing_music.stop()
                            exit_game = True
                            welcome()

                if "cheats" not in cheats:
                    snake_x += velocity_x
                    snake_y += velocity_y

                if abs(snake_x - food_x) < near_food and abs(snake_y - food_y) < near_food:
                    score += 10
                    eat_sound.play()
                    food_x = random.randint(50, screen_width - 50)
                    food_y = random.randint(100, screen_height - 50)
                    snake_length += snake_length_increase
                    if score > int(high_score):
                        high_score = score

                gameWindow.blit(blit_what, [0, 0])

                head = [snake_x, snake_y]
                if game_started and "cheats" not in cheats:
                    snake_list.append(head)

                if len(snake_list) > snake_length:
                    del snake_list[0]

                if not immortality:
                    if snake_x <= 0 or snake_x >= screen_width or snake_y <= 50 or snake_y >= screen_height:
                        game_over = True
                        blit_what = game_over_background
                        game_over_sound.play()
                    if head in snake_list[:-1]:
                        game_over = True
                        blit_what = game_over_background
                        game_over_sound.play()
                else:
                    if snake_x <= 0:
                        snake_x = screen_width
                    elif snake_x >= screen_width:
                        snake_x = 0
                    if snake_y <= 50:
                        snake_y = screen_height
                    elif snake_y >= screen_height:
                        snake_y = 50

                if blit_what == gradient_background:
                    pygame.draw.circle(gameWindow, red, [food_x, food_y], food_size)
                    plot_snake(gameWindow, black, snake_list, snake_size)
                    pygame.draw.rect(gameWindow, score_background_color, [0, 0, screen_width, 50])
                    text_screen("Score: " + str(score), green, 150, 0)
                    text_screen("High Score: " + str(high_score), green, screen_width - 400, 0)
                    pygame.draw.rect(gameWindow, red, [0, 50, screen_width, 5])
                    pygame.draw.rect(gameWindow, red, [0, screen_height - 5, screen_width, 5])
                    pygame.draw.rect(gameWindow, red, [0, 50, 5, screen_height])
                    pygame.draw.rect(gameWindow, red, [screen_width - 5, 50, 5, screen_height])
        else:
            gameWindow.blit(display_in_paused, [0, 0])
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    pygame.mixer.unpause()
                    game_paused = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    activated += event.unicode.lower()
                    cheats += event.unicode.lower()
                    reset += event.unicode.lower()
                    if "immortal" in activated:
                        immortality = True
                        pygame.mixer.music.load("gallery/sounds/ping.mp3")
                        pygame.mixer.music.play()
                        activated = ""
                    if "century" in activated:
                        score += 100
                        snake_length += snake_length_increase * 10
                        if score > int(high_score):
                            with open(high_score_path, "w") as f:
                                f.write(str(high_score))
                        pygame.mixer.music.load("gallery/sounds/ping.mp3")
                        pygame.mixer.music.play()
                        activated = ""
                    if "malnutrition" in activated and snake_length_increase > 1:
                        snake_length_increase -= 1
                        pygame.mixer.music.load("gallery/sounds/ping.mp3")
                        pygame.mixer.music.play()
                        activated = ""
                    if "magnet" in activated:
                        near_food = 100
                        pygame.mixer.music.load("gallery/sounds/ping.mp3")
                        pygame.mixer.music.play()
                        activated = ""
                    if "cheats" in cheats:
                        display_in_paused = cheats_reference
                        if event.key == pygame.K_RETURN:
                            display_in_paused = paused_screen
                            cheats = ""
                    if "reset" in reset:
                        high_score = 0
                        with open(high_score_path, "w") as f:
                            f.write(str(high_score))
                        reset = ""
                        cheats = ""
                        activated = ""
                        exit_game = True
                        welcome()

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    sys.exit()


welcome()
