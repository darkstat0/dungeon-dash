import random
import os
import time
import sys
from pynput import keyboard

# Инициализация
MAP_SIZE = 20  # Сделаем карту квадратной (20x20)
PLAYER = "@"
EMPTY = " "
WALL = "#"
EXIT = "X"
START = "S"

# Генерация карты
def generate_map():
    game_map = [[WALL for _ in range(MAP_SIZE)] for _ in range(MAP_SIZE)]  # Сначала заполняем карту стенами

    # Расставляем пустые места
    for y in range(1, MAP_SIZE - 1):
        for x in range(1, MAP_SIZE - 1):
            if random.random() < 0.7:  # 70% вероятность сделать клетку пустой
                game_map[y][x] = EMPTY

    # Устанавливаем стартовую позицию
    start_x, start_y = random.randint(1, MAP_SIZE - 2), random.randint(1, MAP_SIZE - 2)
    game_map[start_y][start_x] = START

    # Устанавливаем выход
    exit_x, exit_y = random.randint(1, MAP_SIZE - 2), random.randint(1, MAP_SIZE - 2)
    game_map[exit_y][exit_x] = EXIT

    return game_map, start_x, start_y

# Отображение карты
def print_map(game_map, player_x, player_y, level):
    os.system("cls" if sys.platform == "win32" else "clear")  # Очищаем экран
    print(f"Level: {level}")
    print("----------------------")
    for y in range(MAP_SIZE):
        for x in range(MAP_SIZE):
            if x == player_x and y == player_y:
                print(PLAYER, end=" ")
            else:
                print(game_map[y][x], end=" ")
        print()

# Управление игроком
player_x, player_y = 1, 1  # Начальная позиция игрока
level = 1  # Начальный уровень
game_map, player_x, player_y = generate_map()  # Генерация карты

# Флаги для движения
move_up = move_down = move_left = move_right = False

# Обработчик нажатий клавиш
def on_press(key):
    global move_up, move_down, move_left, move_right

    try:
        if key == keyboard.Key.up:
            move_up = True
        elif key == keyboard.Key.down:
            move_down = True
        elif key == keyboard.Key.left:
            move_left = True
        elif key == keyboard.Key.right:
            move_right = True
        elif key.char == 'w':
            move_up = True
        elif key.char == 's':
            move_down = True
        elif key.char == 'a':
            move_left = True
        elif key.char == 'd':
            move_right = True
    except AttributeError:
        pass

# Обработчик отпускания клавиш
def on_release(key):
    global move_up, move_down, move_left, move_right

    try:
        if key == keyboard.Key.up:
            move_up = False
        elif key == keyboard.Key.down:
            move_down = False
        elif key == keyboard.Key.left:
            move_left = False
        elif key == keyboard.Key.right:
            move_right = False
        elif key.char == 'w':
            move_up = False
        elif key.char == 's':
            move_down = False
        elif key.char == 'a':
            move_left = False
        elif key.char == 'd':
            move_right = False
    except AttributeError:
        pass

# Основная логика игры
def game_loop():
    global player_x, player_y, game_map, level

    # Настроим прослушивание клавиш (один раз, чтобы не возникало ошибок)
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()  # Запуск прослушивания клавиш

    while True:
        print_map(game_map, player_x, player_y, level)

        # Проверка на победу (если игрок достиг выхода)
        if game_map[player_y][player_x] == EXIT:
            print("Поздравляем, вы нашли выход!")
            level += 1  # Переход на новый уровень
            game_map, player_x, player_y = generate_map()  # Генерация новой карты
            continue

        # Управление игроком
        if move_up and player_y > 0 and game_map[player_y - 1][player_x] != WALL:
            player_y -= 1
        if move_down and player_y < MAP_SIZE - 1 and game_map[player_y + 1][player_x] != WALL:
            player_y += 1
        if move_left and player_x > 0 and game_map[player_y][player_x - 1] != WALL:
            player_x -= 1
        if move_right and player_x < MAP_SIZE - 1 and game_map[player_y][player_x + 1] != WALL:
            player_x += 1

        time.sleep(0.1)  # Уменьшена задержка для улучшения производительности

    listener.join()  # Ожидание завершения прослушивателя

# Запуск игры
if __name__ == "__main__":
    game_loop()
