## Тема ###

"""
10. Симулятор работы интернета
Описание: На поле расположены узлы (компьютеры) и связи между ними. Пользователь может отправлять "пакеты данных" между узлами, а программа будет находить оптимальный маршрут (алгоритм Дейкстры или Флойда).

Особенности:

Визуализация передачи данных.

Возможность добавления "заторов" на узлах.

Сложность: Высокая.
"""


import pygame
import random
import networkx as nx
import sys
from pygame.color import THECOLORS ## https://python-course.readthedocs.io/projects/elementary/en/latest/lessons/18-pygame.html

### ПЕРЕМЕННЫЕ+ИНИТ ###
WIDTH, HEIGHT = 640, 640
MARGIN = 40
hello_image_index = 0
selected_nodes = []
user_balance = random.randint(100, 1000)
G = nx.gnm_random_graph(5, 6)
pos = nx.spring_layout(G, seed=42)
edges_cost = {edge: random.randint(1, 10) for edge in G.edges}
node_positions = {i: (int((pos[i][0] + 1) * (WIDTH - 2 * MARGIN) / 2) + MARGIN,
                      int((pos[i][1] + 1) * (HEIGHT - 2 * MARGIN) / 2) + MARGIN) for i in G.nodes}

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Internetik")
clock = pygame.time.Clock()
FPS = 60

## ИЗОБРАЖЕНИЯ ##
laptop_images = [
    pygame.transform.scale(pygame.image.load("Images/LaptopDark.png"), (50, 50)),
    pygame.transform.scale(pygame.image.load("Images/LaptopLight.png"), (50, 50))
]
hello_images = [
    pygame.transform.scale(pygame.image.load(f"Images/hello_image{i}.png"), (400, 200)) for i in range(1, 4)
]
character_image = pygame.transform.scale(pygame.image.load("Images/charecter.png"), (200, 400))
button_earn = pygame.transform.scale(pygame.image.load("Images/button_start.png"), (200, 50))
button_start = pygame.transform.scale(pygame.image.load("Images/button_start.png"), (200, 50))
button_play = pygame.transform.scale(pygame.image.load("Images/button_play.png"), (200, 50))
background_image = pygame.image.load('Images/BackgroundImage.jpg')
background_image2 = pygame.image.load('Images/BackgroundImage2.jpg')

node_images = {i: random.choice(laptop_images) for i in G.nodes} # Вот тут было тяжко сначала
zator_nodes = set()  # Узлы с затором

## РАМКА ##
def draw_frame():
    """
            Эта функция рисует рамочку вокруг у меня ж все пиксельное
            :return: рамочка
    """
    pygame.draw.rect(screen, (200, 200, 200), (MARGIN, MARGIN, WIDTH - 2 * MARGIN, HEIGHT - 2 * MARGIN), 3)

## Нужно входное окошко где пользователь нажимает старт (Из проекта предыдущего)
#### ДОДЕЛАТЬ!!! кнопки чтоб не вылетали почему-то стали вылетать

## ПРИВЕТСТВЕННЫЙ ЭКРАН ##
def welcome_screen():
    global hello_image_index  ## Позволяет функции изменять значение глобальной переменной, а не создавать новую локальную переменную с тем же именем но по моему, мы уже такое использовали

    running = True
    while running:
        screen.blit(background_image2, (0, 0))
        draw_frame()
        screen.blit(character_image, (MARGIN, HEIGHT // 2 - 100))

        start_button_rect = button_start.get_rect(bottomright=(WIDTH - MARGIN, HEIGHT - MARGIN - 60))
        play_button_rect = button_play.get_rect(bottomright=(WIDTH - MARGIN, HEIGHT - MARGIN))

        screen.blit(button_start, start_button_rect.topleft)
        screen.blit(button_play, play_button_rect.topleft)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    hello_image_index = (hello_image_index + 1) % 3
                elif play_button_rect.collidepoint(event.pos):
                    running = False

        pygame.display.update()
        clock.tick(FPS)

## РИСУЕМ ГРАФ ##
def draw_graph():
    """
        Рисуем граф
        :return:
    """
    global user_balance
    screen.blit(background_image, (0, 0))
    draw_frame()
    ## Ребрышки
    # Отрисовка рёбер с весами
    for (u, v), cost in edges_cost.items():
        pygame.draw.line(screen, (100, 100, 100), node_positions[u], node_positions[v], 2)
        mid_x = (node_positions[u][0] + node_positions[v][0]) // 2
        mid_y = (node_positions[u][1] + node_positions[v][1]) // 2
        font = pygame.font.Font(None, 24)
        text = font.render(str(cost) + '$', True, (255, 255, 255))
        screen.blit(text, (mid_x + 10, mid_y + 10))

    ## Вершинки
    # Отрисовка вершин
    for i, pos in node_positions.items():
        screen.blit(node_images[i], (pos[0] - 25, pos[1] - 25))
        # КВАДРАТЫ
        if i in selected_nodes:
            color = (255, 255, 255) if selected_nodes.index(i) == 0 else (255, 0, 0)
            pygame.draw.rect(screen, color, (pos[0] - 30, pos[1] - 30, 60, 60), 3)
        if i in zator_nodes:
            pygame.draw.circle(screen, (255, 165, 0), pos, 10)

    font = pygame.font.Font(None, 36)
    # Отображение баланса пользователя ну это понятно
    balance_text = font.render(f'Баланс карты: {user_balance}$', True, (255, 255, 255))
    screen.blit(balance_text, (MARGIN, MARGIN - 30))

## ЕСЛИ НЕ ЗВАТАЕТ ДЕНЕГ ##
def not_enough_money(screen):
    # Размеры окна
    window_width, window_height = 300, 200
    window_x = (screen.get_width() - window_width) // 2
    window_y = (screen.get_height() - window_height) // 2
    # Новое окно для тго чтобы у
    ## ВЫЛЕТАЕТ!!!! ПОПРАВИТЬ
    message_window = pygame.Surface((window_width, window_height))
    ## Uhbans
    font = pygame.font.Font(None, 36)
    text = font.render("Пополните баланс", True, (255, 255, 255))
    text_rect = text.get_rect(center=(window_width // 2, window_height // 2 - 20))
    # Кнопка "OK"
    ## После того как пользоваель на нее нажал, не все закрывается, а только это окошко маленькое!!!
    ### Поправить местоположение кнопки, слетела вдевл
    button_font = pygame.font.Font(None, 30)
    button_text = button_font.render("OK", True, (0, 0, 0))
    button_rect = pygame.Rect(0, 0, 80, 40)
    button_rect.center = (window_width // 2, window_height // 2 + 40)
    button_color = (200, 200, 200)

    running = True
    while running:
        screen.fill((30, 30, 30)) # Затемняем экран типо красиво будет
        message_window.fill((50, 50, 50)) # Текст и кнопка
        pygame.draw.rect(message_window, (255, 255, 255), message_window.get_rect(), 2)
        message_window.blit(text, text_rect)
        pygame.draw.rect(message_window, button_color, button_rect)
        pygame.draw.rect(message_window, (0, 0, 0), button_rect, 2)
        message_window.blit(button_text, button_text.get_rect(center=button_rect.center))
        screen.blit(message_window, (window_x, window_y)) # Отрисовываем окно
        pygame.display.flip()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos[0] - window_x, event.pos[1] - window_y):
                    running = False

        pygame.time.Clock().tick(30)

## ОСНОВНОЙ АЛГОРИТМ ##
def find_shortest_path():
    """
    Расчитываем самый короткий путь
    :return:
    """

    ## https://habr.com/ru/articles/125898/ вот отс/да как работать с shortest. path lambda и всякое такое, но с дямюдой конкретно мне помог чат гпт, извините, я пыталачь разобраться час сапма что писать в этой ямбде и мне стало ленб
    ### https://en.wikipedia.org/wiki/NetworkX?utm.com про алгоритм
    ## А ТЕПРЕЬ ЭТО ПО ДРУГОМУ: https://www.geeksforgeeks.org/a-search-algorithm/
    #### https://www.datacamp.com/tutorial/a-star-algorithm
    if len(selected_nodes) == 2:
        try:
            return nx.shortest_path(G, source=selected_nodes[0], target=selected_nodes[1],
                                    weight=lambda u, v, d: edges_cost.get((u, v), edges_cost.get((v, u))) +
                                                           (5 if u in zator_nodes or v in zator_nodes else 0))
        except nx.NetworkXNoPath:
            return []
    return []


def calculate_path_cost(path):
    return sum(
        edges_cost.get((path[i], path[i + 1]), edges_cost.get((path[i + 1], path[i]))) +
        (5 if path[i] in zator_nodes or path[i + 1] in zator_nodes else 0)
        for i in range(len(path) - 1))


def animate_packet(path):
    for i in range(len(path) - 1):
        u_pos = node_positions[path[i]]
        v_pos = node_positions[path[i + 1]]
        for t in range(0, 101, 5):
            x = u_pos[0] + (v_pos[0] - u_pos[0]) * t / 100
            y = u_pos[1] + (v_pos[1] - u_pos[1]) * t / 100
            draw_graph()
            pygame.draw.circle(screen, (255, 0, 0), (int(x), int(y)), 10)
            pygame.display.update()
            clock.tick(30)


# Создаем рандомный лабиринт
### https://www.youtube.com/watch?v=nXe1b-ZeQS0
## https://habr.com/ru/articles/262345/
#### https://github.com/Yan-Minotskiy/labyrinth_generating
##  ДОписать!! Криво работает, когда дозодишь до конца ничего не происхзодит
# !!! Вылеи=тает когда доходишь до конца
def generate_maze(rows, cols):
    maze = [[1] * (cols * 2 + 1) for _ in range(rows * 2 + 1)]
    stack = [(1, 1)]
    maze[1][1] = 0
    while stack:
        x, y = stack[-1]
        neighbors = []
        for dx, dy in [(2, 0), (-2, 0), (0, 2), (0, -2)]:
            nx_, ny_ = x + dx, y + dy
            if 1 <= nx_ < rows * 2 and 1 <= ny_ < cols * 2 and maze[nx_][ny_] == 1:
                neighbors.append((nx_, ny_))
        if neighbors:
            nx_, ny_ = random.choice(neighbors)
            maze[(x + nx_) // 2][(y + ny_) // 2] = 0
            maze[nx_][ny_] = 0
            stack.append((nx_, ny_))
        else:
            stack.pop()
    return maze

# Функция игры в лабиринт
## Это я делала по туториалу отсюда https://thepythoncode.com/article/build-a-maze-game-in-python?utm.com
### И отсюда https://electronstudio.github.io/pygame-zero-book/chapters/maze.html
def play_maze_game():
    WIDTH, HEIGHT = 700, 700
    ROWS, COLS = 11, 11
    CELL_SIZE = WIDTH // (COLS * 2 + 1)
    maze = generate_maze(ROWS, COLS)
    player_pos = [1, 1]
    goal_pos = [ROWS * 2 - 1, COLS * 2 - 1]
    maze_screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    while True:
        maze_screen.fill((178, 102, 255))
        for y in range(len(maze)):
            for x in range(len(maze[0])):
                color = (255, 255, 255) if maze[y][x] == 1 else (50, 50, 50)
                pygame.draw.rect(maze_screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # игрок - зеленый
        pygame.draw.rect(maze_screen, (0, 255, 0),
                         (player_pos[1] * CELL_SIZE, player_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(maze_screen, (255, 0, 0),
                         (goal_pos[1] * CELL_SIZE, goal_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        ##Шежевры налево, направо и так далеее

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                dx, dy = 0, 0
                if event.key == pygame.K_LEFT: dx = -1
                elif event.key == pygame.K_RIGHT: dx = 1
                elif event.key == pygame.K_UP: dy = -1
                elif event.key == pygame.K_DOWN: dy = 1
                nx_, ny_ = player_pos[0] + dy, player_pos[1] + dx
                if maze[nx_][ny_] == 0: # Проходим по пустым клеткаммм
                    player_pos = [nx_, ny_]
                if player_pos == goal_pos:
                    return "done"

        pygame.display.update()
        clock.tick(30)


welcome_screen()
running = True
while running:
    draw_graph()
    path = find_shortest_path()
    if len(path) > 1:
        for i in range(len(path) - 1):
            pygame.draw.line(screen, (255, 255, 255), node_positions[path[i]], node_positions[path[i + 1]], 4)

    earn_button_rect = button_earn.get_rect(topright=(WIDTH - MARGIN, HEIGHT - MARGIN - 50))
    screen.blit(button_earn, earn_button_rect.topleft)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, pos in node_positions.items():
                if pos[0] - 25 < event.pos[0] < pos[0] + 25 and pos[1] - 25 < event.pos[1] < pos[1] + 25:
                    if event.button == 1:
                        if len(selected_nodes) < 2 and i not in selected_nodes:
                            selected_nodes.append(i)
                        elif i in selected_nodes:
                            selected_nodes.remove(i)
                        elif len(selected_nodes) == 2:
                            selected_nodes = [i]
                    elif event.button == 3:
                        if i in zator_nodes:
                            zator_nodes.remove(i)
                        else:
                            zator_nodes.add(i)
            if earn_button_rect.collidepoint(event.pos):
                if len(path) > 1:
                    cost = calculate_path_cost(path)
                    if user_balance >= cost:
                        animate_packet(path)
                        user_balance -= cost
                        selected_nodes.clear()
                    else:
                        not_enough_money(screen)
                        result = play_maze_game() # Запускаем игру с лаюиринтом
                        if result == "quit":
                            running = False # Закрываем игру полностью, если игрок закрыл окно лабиринта
                        user_balance += 40

    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
