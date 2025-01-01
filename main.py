import random
import os
import time
from pynput import keyboard

# Константы
MAP_SIZE = 20
PLAYER = "@"
EMPTY = " "
WALL = "#"
EXIT = "X"
START = "S"

# Генерация карты
def generate_map():
    game_map = [[WALL for _ in range(MAP_SIZE)] for _ in range(MAP_SIZE)]

    for y in range(1, MAP_SIZE - 1):
        for x in range(1, MAP_SIZE - 1):
            if random.random() < 0.7:
                game_map[y][x] = EMPTY

    start_x, start_y = random.randint(1, MAP_SIZE - 2), random.randint(1, MAP_SIZE - 2)
    game_map[start_y][start_x] = START

    while True:
        exit_x, exit_y = random.randint(1, MAP_SIZE - 2), random.randint(1, MAP_SIZE - 2)
        if (exit_x, exit_y) != (start_x, start_y):
            game_map[exit_y][exit_x] = EXIT
            break

    return game_map, start_x, start_y

# Отображение карты
def print_map(game_map, player_x, player_y, level):
    os.system("cls" if os.name == "nt" else "clear")
    print(f"Level: {level}")
    print("----------------------")
    for y in range(MAP_SIZE):
        for x in range(MAP_SIZE):
            if x == player_x and y == player_y:
                print(PLAYER, end=" ")
            else:
                print(game_map[y][x], end=" ")
        print()

# Управление
move_up = move_down = move_left = move_right = False

def on_press(key):
    global move_up, move_down, move_left, move_right
    try:
        if key in [keyboard.Key.up, 'w']:
            move_up = True
        elif key in [keyboard.Key.down, 's']:
            move_down = True
        elif key in [keyboard.Key.left, 'a']:
            move_left = True
        elif key in [keyboard.Key.right, 'd']:
            move_right = True
    except AttributeError:
        pass

def on_release(key):
    global move_up, move_down, move_left, move_right
    try:
        if key in [keyboard.Key.up, 'w']:
            move_up = False
        elif key in [keyboard.Key.down, 's']:
            move_down = False
        elif key in [keyboard.Key.left, 'a']:
            move_left = False
        elif key in [keyboard.Key.right, 'd']:
            move_right = False
    except AttributeError:
        pass

# Основной игровой цикл
def game_loop():
    global move_up, move_down, move_left, move_right
    game_map, player_x, player_y = generate_map()
    level = 1

    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    try:
        while True:
            print_map(game_map, player_x, player_y, level)

            if game_map[player_y][player_x] == EXIT:
                print("Поздравляем, вы нашли выход!")
                level += 1
                time.sleep(1)
                game_map, player_x, player_y = generate_map()
                continue

            if move_up and player_y > 0 and game_map[player_y - 1][player_x] != WALL:
                player_y -= 1
            if move_down and player_y < MAP_SIZE - 1 and game_map[player_y + 1][player_x] != WALL:
                player_y += 1
            if move_left and player_x > 0 and game_map[player_y][player_x - 1] != WALL:
                player_x -= 1
            if move_right and player_x < MAP_SIZE - 1 and game_map[player_y][player_x + 1] != WALL:
                player_x += 1

            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nИгра завершена.")
    finally:
        listener.stop()

if __name__ == "__main__":
    game_loop()
