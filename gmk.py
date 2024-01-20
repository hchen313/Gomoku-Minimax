import pygame
import math
import re
from copy import copy
from patterns import *
import random

pygame.init()
screen = pygame.display.set_mode((800, 800))
screen.fill((227, 165, 82))
clock = pygame.time.Clock()
running = True
black = (0, 0, 0)
white = (255, 255, 255)
clicked = False
main_grid = [0] * 225
black_grid = [0] * 225
white_grid = [0] * 225
black_turn = True
player_turn = True
test_range = set()
tt = {}
move_count = 0

def new_table():
    screen.fill((227, 165, 82))
    for i in range(15):
        pygame.draw.line(screen, black, (50 + i * 50, 50), (50 + i * 50, 750), 2)
        pygame.draw.line(screen, black, (50, 50 + i * 50), (750, 50 + i * 50), 2)

def valid_pos(pos):
    x = pos[0]
    y = pos[1]
    if x % 50 <= 10:
        x = x // 50 * 50
    elif x % 50 >= 40:
        x = x // 50 * 50
        x += 50
    if y % 50 <= 10:
        y = y // 50 * 50
    elif y % 50 >= 40:
        y = y // 50 * 50
        y += 50
    if x % 50 == 0 and y % 50 == 0:
        return (x, y)
    else:
        return None

def place_stone(pos, color):
    pygame.draw.circle(screen, color, pos, 25, 0)

def check_winner(grid):
    if 0 not in main_grid:
        return None
    binary_string = "".join(map(str, grid))
    if re.search(pattern_horizontal, binary_string):
        return True
    if re.search(pattern_vertical, binary_string):
        return True
    if re.search(pattern_dia, binary_string):
        return True
    if re.search(pattern_anti_dia, binary_string):
        return True
    return False

def check_force_plays(grid, black, white):
    value = None
    best_choice = False

    # horizontal
    for i in range(0, 225, 15):
        binary_string = "".join(map(str, grid[i:i+15]))
        match = re.search("022220|02222|22220", binary_string)
        if match:
            return match.start() + match.group().index("0") + i
        match = re.search("01111|11110", binary_string)
        if match:
            return match.start() + match.group().index("0") + i
        match = re.search("011110", binary_string)
        if match:
            return math.inf
        match = re.search("002220|022200", binary_string)
        if match:
            value = match.start() + match.group().find("0", match.group().find('0') + 1) + i
            best_choice = True
        if best_choice == False:
            match = re.search("(0)1110",binary_string)
            if match:
                value = match.start(1) + i
                # match for (01110)
                # option_1 = "21110"
                # option_2 = "01112"
                # new_string_1 = binary_string.replace(match.group(0), option_1)
                # new_string_2 = binary_string.replace(match.group(0), option_2)
                # arr_1 = grid[0:i] + [int(char) for char in new_string_1] + grid[i+15:225]
                # arr_2 = grid[0:i] + [int(char) for char in new_string_2] + grid[i+15:225]
                # if evaluate(arr_1, black, white) > evaluate(arr_2, black, white):
                #     value = match.start() + match.group().index("0") + i
                # else:
                #     value = match.start() + match.group().find("0", match.group().find('0') + 1) + i

    # vertical
    binary_string = "".join(map(str, grid))
    for pattern in fp_v:
        match = re.search(pattern, binary_string)
        if match:
            return match.start(1)
    match = re.search("0\d{14}1\d{14}1\d{14}1\d{14}1\d{14}0", binary_string)
    if match:
        return math.inf
    if best_choice == False:
        for pattern in fp_v_b:
            match = re.search(pattern, binary_string)
            if match:
                value = match.start(1)
    if best_choice == False:
        match = re.search("(0)\d{14}1\d{14}1\d{14}1\d{14}0", binary_string)
        if match:
            value = match.start(1)

    # diagonal
    for pattern in fp_d:
        match = re.search(pattern, binary_string)
        if match:
            return match.start(1)
    match = re.search("0\d{15}1\d{15}1\d{15}1\d{15}1\d{15}0", binary_string)
    if match:
        return math.inf
    if best_choice == False:
        for pattern in fp_d_b:
            match = re.search(pattern, binary_string)
            if match:
                value = match.start(1)
    if best_choice == False:
        match = re.search("(0)\d{15}1\d{15}1\d{15}1\d{15}0", binary_string)
        if match:
            value = match.start(1)

    # anti-diagonal
    for pattern in fp_a:
        match = re.search(pattern, binary_string)
        if match:
            return match.start(1)
    match = re.search("0\d{13}1\d{13}1\d{13}1\d{13}1\d{13}0", binary_string)
    if match:
        return math.inf
    if best_choice == False:
        for pattern in fp_a_b:
            match = re.search(pattern, binary_string)
            if match:
                value = match.start(1)
    if best_choice == False:
        match = re.search("(0)\d{13}1\d{13}1\d{13}1\d{13}0", binary_string)
        if match:
            value = match.start(1)
    return value



def next_move(grid, black, white):
    move = None
    force_plays = None
    if move_count > 5:
        force_plays = check_force_plays(grid, black, white)
    if force_plays == None:
        score = -math.inf if black_turn else math.inf
        for i in test_range:
            if grid[i] == 0:
                grid[i] = 1 if black_turn else 2
                if black_turn:
                    black[i] = 1
                else:
                    white[i] = 1
                res = minimax(grid, black, white, 1, not black_turn, -math.inf, math.inf)
                grid[i] = 0
                if black_turn:
                    black[i] = 0
                    if res > score:
                        score = res
                        move = i
                else:
                    white[i] = 0
                    if res < score:
                        score = res
                        move = i
    else:
        move = force_plays
    if move == math.inf:
        move = None
    return move

def evaluate(grid, black, white):
    if check_winner(black) == True:
        return math.inf
    if check_winner(white) == True:
        return -math.inf
    if check_winner(black) == None:
        return 0
    black_score = 0
    white_score = 0

    # horizontal
    for i in range(0, 225, 15):
        binary_string_h = "".join(map(str, grid[i:i+15]))
        # black
        for key, value in pt_black_h.items():
            matches = re.findall(key, binary_string_h)
            if len(matches) != 0:
                binary_string_h = re.sub(key, lambda match: match.group().replace("1", "3"), binary_string_h)
                black_score += len(matches) * value
        # white
        for key, value in pt_white_h.items():
            matches = re.findall(key, binary_string_h)
            if len(matches) != 0:
                binary_string_h = re.sub(key, lambda match: match.group().replace("2", "3"), binary_string_h)
                white_score -= len(matches) * value

    # vertical
    binary_string_v = "".join(map(str, grid))
    # black
    for key, value in pt_black_v.items():
        match = re.search(key, binary_string_v)
        if match:
            black_score += len(re.findall(key, binary_string_v)) * value
            binary_string_v = binary_string_v.replace(match.group(0), "3".join(match.groups()))
    # white
    for key, value in pt_white_v.items():
        match = re.search(key, binary_string_v)
        if match:
            white_score -= len(re.findall(key, binary_string_v)) * value
            binary_string_v = binary_string_v.replace(match.group(0), "3".join(match.groups()))

    # diagonal
    binary_string_d = "".join(map(str, grid))
    # black
    for key, value in pt_black_d.items():
        match = re.search(key, binary_string_d)
        if match:
            black_score += len(re.findall(key, binary_string_d)) * value
            binary_string_d = binary_string_d.replace(match.group(0), "3".join(match.groups()))
    # white
    for key, value in pt_white_d.items():
        match = re.search(key, binary_string_d)
        if match:
            white_score -= len(re.findall(key, binary_string_d)) * value
            binary_string_d = binary_string_d.replace(match.group(0), "3".join(match.groups()))

   # anti-diagonal
    binary_string_a = "".join(map(str, grid))
    # black
    for key, value in pt_black_a.items():
        match = re.search(key, binary_string_a)
        if match:
            black_score += len(re.findall(key, binary_string_a)) * value
            binary_string_a = binary_string_a.replace(match.group(0), "3".join(match.groups()))
    # white
    for key, value in pt_white_a.items():
        match = re.search(key, binary_string_a)
        if match:
            white_score -= len(re.findall(key, binary_string_a)) * value
            binary_string_a = binary_string_a.replace(match.group(0), "3".join(match.groups()))

    return black_score + white_score


def minimax(grid, black, white, depth, black_turn, alpha, beta):
    res = check_winner(black) if black_turn else check_winner(white)
    if res is not False:
        return evaluate(grid, black, white)
    if depth == 0:
        binary_string = "".join(map(str, grid))
        if binary_string not in tt:
            tt[binary_string] = evaluate(grid, black, white)
        return tt[binary_string]

    if black_turn:
        val = -math.inf
        for i in test_range:
            if grid[i] == 0:
                grid[i] = 1
                black[i] = 1
                score = minimax(grid, black, white, depth - 1, not black_turn, alpha, beta)
                grid[i] = 0
                black[i] = 0
                val = max(score, val)
                alpha = max(score, alpha)
                if beta <= alpha:
                    break
        return val
    else:
        val = math.inf
        for i in test_range:
            if grid[i] == 0:
                grid[i] = 2
                white[i] = 1
                score = minimax(grid, black, white, depth - 1, not black_turn, alpha, beta)
                grid[i] = 0
                white[i] = 0
                val = min(score, val)
                beta = min(score, beta)
                if beta <= alpha:
                    break
        return val


def add_range(pos):
    global test_range
    vertical = range(-1, 2)
    horizontal = range(-1, 2)

    if pos % 15 == 0:
        horizontal = range(0, 2)
    elif pos % 15 == 14:
        horizontal = range(-1, 1)

    if pos // 15 == 0:
        vertical = range(0, 2)
    elif pos // 15 == 14:
        vertical = range(-1, 1)

    for i in vertical:
        for j in horizontal:
            test_range.add(i * 15 + pos + j)
    test_range.remove(pos)

def best_move():
    move = next_move(copy(main_grid), copy(black_grid), copy(white_grid))
    if move == None:
        move = -1
        while move == -1 or main_grid[move] != 0 or move not in test_range:
            move = random.randint(0, 224)
    if move is not None:
        place_stone((((move % 15) * 50) + 50, ((move // 15) * 50) + 50), (black if black_turn else white))
        main_grid[move] = 1 if black_turn else 2
        if black_turn:
            black_grid[move] = 1
        else:
            white_grid[move] = 1
        add_range(move)


new_table()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        if event.type == pygame.MOUSEBUTTONUP and clicked:
            clicked = False
            pos = pygame.mouse.get_pos()
            pos = valid_pos(pos)
            if pos is not None:
                grid_pos = ((pos[0] - 50) // 50) + ((pos[1] - 50) // 50) * 15
                if main_grid[grid_pos] == 0:
                    place_stone(pos, (black if black_turn else white))
                    main_grid[grid_pos] = 1 if black_turn else 2
                    if black_turn:
                        black_grid[grid_pos] = 1
                    else:
                        white_grid[grid_pos] = 1
                    add_range(grid_pos)
                    res = check_winner(black_grid if black_turn else white_grid)
                    if res == True or res == None:
                        running = False
                    black_turn = not black_turn
                    player_turn = not player_turn
                    move_count += 1
                    best_move()
                    res = check_winner(black_grid if black_turn else white_grid)
                    if res == True or res == None:
                        running = False
                    black_turn = not black_turn
                    player_turn = not player_turn
                    move_count += 1

    pygame.display.update()
    clock.tick(60)
pygame.quit()
