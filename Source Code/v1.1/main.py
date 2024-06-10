import pygame
import sys
import os
import re
import random
from pathlib import Path
pygame.init()
pygame.mixer.init()
pygame.font.init()


# Function for encoding and decoding text
characters = "a0bcdefg1h,jk@m_nop)qr.s/<tu3v!x8?;+7yzA6:B=#DE|FG2H'I(JKL^MN&%*OP$QRSTUB9W>5YZ34"
characters_len = len(characters)

def encode(text):
    encoded_text = ""

    for i in range(len(text)):
        digit_position = re.search(text[i], characters)
        encode = characters[(digit_position.start() + 2) % characters_len]
        random_char_1 = random.choice(list(characters))
        random_char_2 = random.choice(list(characters))
        encoded_text += random_char_1 + encode + random_char_2

    encoded_text += "Hk#@/.0"
    while len(encoded_text) < 50:
        random_char = random.choice(list(characters))
        encoded_text += random_char

    return encoded_text


def decode(text):
    decoded_text = ""

    end = re.search("Hk#@/.0", text)
    text = text[0:end.start() + 1]

    i = 1
    while i < len(text):
        digit_position = re.search(text[i], characters)
        decode = characters[(digit_position.start() - 2) % characters_len]
        decoded_text += decode
        i += 3

    return decoded_text

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
light_red = (255, 102, 102)
snake_color = (204, 204, 204)
score_background_color = (9, 153, 163)

# Creating Game Window
gameWindow = pygame.display.set_mode()

window_size = pygame.display.get_window_size()
screen_width = window_size[0]
screen_height = window_size[1]

# Game Title
pygame.display.set_caption("SnakX (iamdevdiv)")
pygame.display.update()
    

# Background Images
bg_numbers = []
game_background = None


def add_bg_numbers():
    while len(bg_numbers) != 5:
        random_number = random.randint(1, 5)
        if random_number not in bg_numbers:
            bg_numbers.append(random_number)
            

add_bg_numbers()


def change_game_background():
    global game_background
    random_background = bg_numbers.pop()
    if len(bg_numbers) == 0:
        add_bg_numbers()
    game_background = pygame.image.load(f"gallery/images/bg{random_background}.jpg")
    game_background = pygame.transform.scale(game_background, (screen_width, screen_height - 50)).convert_alpha()

welcome_background = pygame.image.load("gallery/images/welcome.jpg")
welcome_background = pygame.transform.scale(welcome_background, (screen_width, screen_height)).convert_alpha()

game_over_background = pygame.image.load("gallery/images/game_over.jpg")
game_over_background = pygame.transform.scale(game_over_background, (screen_width, screen_height)).convert_alpha()

change_game_background()

food = pygame.image.load("gallery/images/apple.png")

cheats_reference = pygame.image.load("gallery/images/cheatsheet.jpg")
cheats_reference = pygame.transform.scale(cheats_reference, (screen_width, screen_height)).convert_alpha()

paused_screen = pygame.image.load("gallery/images/paused.jpg")
paused_screen = pygame.transform.scale(paused_screen, (screen_width, screen_height)).convert_alpha()

# Background Music and Sound Effects
welcome_music = pygame.mixer.Sound("gallery/sounds/main_menu.mp3")
while_playing_music = pygame.mixer.Sound("gallery/sounds/while_playing.mp3")
while_playing_music.set_volume(0.3)
game_over_sound = pygame.mixer.Sound("gallery/sounds/game_over.mp3")
ping_sound = pygame.mixer.Sound("gallery/sounds/ping.mp3")
eat_sound = pygame.mixer.Sound("gallery/sounds/eat.mp3")

# Creating Clock
clock = pygame.time.Clock()
fps = 60

# Function to display score
font = pygame.font.Font("gallery/fonts/Baloo_Bhai_2_Medium.ttf", 35)
big_font = pygame.font.Font("gallery/fonts/Baloo_Bhai_2_Medium.ttf", 50)


def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])


def big_text_screen(text, color, x, y):
    screen_text = big_font.render(text, True, color)
    x -= font.size(text)[0] / 2
    gameWindow.blit(screen_text, [x, y])


# Function to plot snakes
def plot_snake(game_window, color, snk_list, snk_size):
    snk_list[0][2] = True
    # tail = snk_list[0]

    new_positions = []
    new_positions_len = 0
    prev_x = prev_y = None
    
    for pos in snk_list:
        x, y, block_plotting = pos

        if block_plotting:
            prev_x, prev_y = x, y
            continue

        if x == prev_x:
            while y > prev_y:
                new_positions_len += 1
                new_positions.append([x, prev_y])
                prev_y += 1

            while y < prev_y:
                new_positions_len += 1
                new_positions.append([x, prev_y])
                prev_y -= 1
        else:
            while x > prev_x:
                new_positions_len += 1
                new_positions.append([prev_x, y])
                prev_x += 1

            while x < prev_x:
                new_positions_len += 1
                new_positions.append([prev_x, y])
                prev_x -= 1
    
    snk_list[0][2] = False

    head_positions = tuple(range(new_positions_len - 6, new_positions_len))
    for index, pos in enumerate(new_positions):
        if index in head_positions:
            pygame.draw.circle(game_window, green, pos, snk_size)
        else:
            pygame.draw.circle(game_window, color, pos, snk_size)


# Checking and Getting High Score
def update_high_score(new_high_score):
    with open(high_score_path, "w") as f:
        f.writelines([high_score_warning, encode(str(new_high_score))])

high_score_path = "high_score.txt"
high_score_warning = "This is high score of SnakX game installed on your PC. DON'T TRY TO MODIFY OR DELETE IT! Doing so will reset your high score to 0.\n"

if not os.path.exists(high_score_path):
    update_high_score("0")

with open(high_score_path, "r") as file:
    try:
        past_high_score = file.readlines()[1]
        if len(past_high_score) != 50 or "Hk#@/.0" not in past_high_score:
            update_high_score("0")
            high_score = 0
        else:
            high_score = int(decode(past_high_score))
    except IndexError:
        update_high_score("0")
        high_score = 0


# Cheat Codes
activated = ""
cheats = ""
reset = ""

immortality = False
velocity_difference = 0
snake_length_increase = 4
near_food = 7


# Welcome Screen
def welcome():
    exit_game = False
    blit_what = welcome_background
    global activated, cheats, immortality, snake_length_increase, near_food, high_score, reset
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
                cheats += event.unicode.lower()
                reset  += event.unicode.lower()

                if "cheats" in cheats:
                    blit_what = cheats_reference
                    pygame.mixer.pause()
                    if event.key == pygame.K_RETURN:
                        blit_what = welcome_background
                        pygame.mixer.unpause()
                        cheats = ""
                elif "reset" in reset:
                    high_score = 0
                    update_high_score(high_score)
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

    blit_what = game_background
    display_in_paused = paused_screen

    velocity_x = 0
    velocity_y = 0
    initial_velocity = 5
    velocity = 5

    food_x = random.randint(50, screen_width - 50)
    food_y = random.randint(100, screen_height - 50)

    score = 0

    snake_list = [
        [80, 150, False], [85, 150, False], [90, 150, False], [95, 150, False], [100, 150, False],
        [105, 150, False], [110, 150, False], [115, 150, False], [120, 150, False], [125, 150, False],
    ]
    snake_length = len(snake_list)
    snake_size = 15
    
    snake_x = snake_list[-1][0]
    snake_y = snake_list[-1][1]
    block_plotting = False

    global activated, cheats, immortality, snake_length_increase, near_food, high_score, reset, snake_color, velocity_difference

    # Game Loop
    while not exit_game:
        if not game_paused:
            if game_over:
                change_game_background()
                while_playing_music.stop()
                update_high_score(high_score)
                gameWindow.blit(blit_what, [0, 0])
                if blit_what == game_over_background:
                    big_text_screen(str(score), white, screen_width / 2, 75)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        update_high_score(high_score)
                        exit_game = True

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        pygame.mixer.pause()
                        if score == int(high_score):
                            update_high_score(high_score)
                        game_paused = True

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and "cheats" not in cheats:
                        game_over_sound.stop()
                        while_playing_music.play(loops=-1)
                        game_loop()

                    if event.type == pygame.KEYDOWN:
                        cheats += event.unicode.lower()
                        reset += event.unicode.lower()
                        
                        if "cheats" in cheats:
                            blit_what = cheats_reference
                            pygame.mixer.pause()
                            if event.key == pygame.K_RETURN:
                                blit_what = game_over_background
                                pygame.mixer.unpause()
                                cheats = ""
                        elif "reset" in reset:
                            high_score = 0
                            update_high_score(high_score)
                            reset = ""
                            cheats = ""
                            activated = ""
                            exit_game = True
                            welcome()
            else:
                level = score // 100
                if level > 10:
                    level = 10

                velocity = initial_velocity + level + velocity_difference
                if velocity > 15:
                    velocity = 15

                if velocity_x:
                    velocity_x = velocity * (velocity_x / abs(velocity_x))
                elif velocity_y:
                    velocity_y = velocity * (velocity_y / abs(velocity_y))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        update_high_score(high_score)
                        exit_game = True

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        pygame.mixer.pause()
                        if score == int(high_score):
                            update_high_score(high_score)
                        game_paused = True

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT and "cheats" not in cheats:
                        velocity_x = velocity
                        velocity_y = 0

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT and "cheats" not in cheats:
                        velocity_x = -velocity
                        velocity_y = 0

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_UP and "cheats" not in cheats:
                        velocity_y = -velocity
                        velocity_x = 0

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN and "cheats" not in cheats:
                        velocity_y = velocity
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
                            immortality = not immortality
                            ping_sound.play()
                            activated = ""
                        elif "century" in activated:
                            score += 100
                            snake_length += snake_length_increase * 10
                            if score > int(high_score):
                                high_score = score
                                update_high_score(high_score)
                            ping_sound.play()
                            activated = ""
                        elif "badapple" in activated and snake_length_increase > 4:
                            snake_length_increase -= 2
                            ping_sound.play()
                            activated = ""
                        elif "goodapple" in activated and snake_length_increase < 10:
                            snake_length_increase += 2
                            ping_sound.play()
                            activated = ""
                        elif "magnet" in activated:
                            near_food = 100
                            ping_sound.play()
                            activated = ""
                        elif "upstairs" in activated:
                            if velocity < 15:
                                velocity_difference += 1
                                ping_sound.play()
                            activated = ""
                        elif "downstairs" in activated:
                            if velocity > 5:
                                velocity_difference -= 1
                                ping_sound.play()
                            activated = ""
                        elif "cheats" in cheats:
                            blit_what = cheats_reference
                            pygame.mixer.pause()
                            if event.key == pygame.K_RETURN:
                                blit_what = game_background
                                pygame.mixer.unpause()
                                cheats = ""
                        elif "reset" in reset:
                            high_score = 0
                            update_high_score(high_score)
                            reset = ""
                            cheats = ""
                            activated = ""
                            while_playing_music.stop()
                            exit_game = True
                            welcome()

                if "cheats" not in cheats:
                    snake_x += velocity_x
                    snake_y += velocity_y

                if abs(snake_x - (food_x + 15)) < near_food and abs(snake_y - (food_y + 25)) < near_food:
                    score += 10
                    eat_sound.play()
                    food_x = random.randint(50, screen_width - 50)
                    food_y = random.randint(100, screen_height - 50)
                    snake_length += snake_length_increase
                    if score > int(high_score):
                        high_score = score

                if blit_what == cheats_reference:
                    gameWindow.blit(blit_what, [0, 0])
                else:
                    gameWindow.blit(blit_what, [0, 50])
                
                head = [snake_x, snake_y, block_plotting]
                block_plotting = False

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
                        block_plotting = True
                    elif snake_x >= screen_width:
                        snake_x = 0
                        block_plotting = True
                    if snake_y <= 50:
                        snake_y = screen_height
                        block_plotting = True
                    elif snake_y >= screen_height:
                        snake_y = 50
                        block_plotting = True

                if blit_what == game_background:
                    gameWindow.blit(food, (food_x, food_y))
                    plot_snake(gameWindow, snake_color, snake_list, snake_size)
                    pygame.draw.rect(gameWindow, score_background_color, [0, 0, screen_width, 50])
                    text_screen("Score: " + str(score), green, 150, 0)
                    text_screen("High Score: " + str(high_score), green, screen_width - 400, 0)

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
                        immortality = not immortality
                        ping_sound.play()
                        activated = ""
                    elif "century" in activated:
                        score += 100
                        snake_length += snake_length_increase * 10
                        if score > int(high_score):
                            update_high_score(high_score)
                        ping_sound.play()
                        activated = ""
                    elif "badapple" in activated and snake_length_increase > 4:
                        snake_length_increase -= 2
                        ping_sound.play()
                        activated = ""
                    elif "goodapple" in activated and snake_length_increase < 10:
                        snake_length_increase += 2
                        ping_sound.play()
                        activated = ""
                    elif "magnet" in activated:
                        near_food = 100
                        ping_sound.play()
                        activated = ""
                    elif "upstairs" in activated:
                            if velocity < 15:
                                velocity_difference += 1
                                ping_sound.play()
                            activated = ""
                    elif "downstairs" in activated:
                        if velocity > 5:
                            velocity_difference -= 1
                            ping_sound.play()
                        activated = ""
                    elif "cheats" in cheats:
                        display_in_paused = cheats_reference
                        if event.key == pygame.K_RETURN:
                            display_in_paused = paused_screen
                            cheats = ""
                    elif "reset" in reset:
                        high_score = 0
                        update_high_score(high_score)
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
