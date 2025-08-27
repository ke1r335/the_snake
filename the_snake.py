from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейкиfrom random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self, position):
        """
        Инициализация игрового объекта.

        Args:
            position (tuple): Начальная позиция объекта (x, y)
        """
        self.position = position
        self.body_color = None

    def draw(self):
        """Метод для отрисовки объекта."""
        pass


class Apple(GameObject):
    """Класс для представления яблока в игре."""

    def __init__(self, screen_width, screen_height, cell_size):
        """
        Инициализация яблока.

        Args:
            screen_width (int): Ширина игрового поля
            screen_height (int): Высота игрового поля
            cell_size (int): Размер одной клетки на игровом поле
        """
        super().__init__(position=(0, 0))
        self.body_color = (255, 0, 0)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.cell_size = cell_size
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайное положение яблока на игровом поле."""
        x = randint(0, (self.screen_width // self.cell_size) - 1) * self.cell_size
        y = randint(0, (self.screen_height // self.cell_size) - 1) * self.cell_size
        self.position = (x, y)

    def draw(self, screen):
        """
        Отрисовывает яблоко на игровом поле.

        Args:
            screen: Экран, на котором будет отрисовано яблоко
        """
        pygame.draw.rect(
            screen,
            self.body_color,
            pygame.Rect(self.position[0], self.position[1], self.cell_size, self.cell_size),
        )


class Snake(GameObject):
    """Класс для представления змейки в игре."""

    def __init__(self, initial_position, cell_size):
        """
        Инициализация змейки.

        Args:
            initial_position (tuple): Начальная позиция змейки
            cell_size (int): Размер одной клетки на игровом поле
        """
        super().__init__(position=initial_position)
        self.body_color = (0, 255, 0)
        self.cell_size = cell_size
        self.positions = [initial_position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self.length = 1

    def update_direction(self):
        """Обновляет направление движения змейки на следующее."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Перемещает змейку в текущем направлении."""
        current_head = self.positions[0]
        new_head = (
            (current_head[0] + self.direction[0] * self.cell_size) % SCREEN_WIDTH,
            (current_head[1] + self.direction[1] * self.cell_size) % SCREEN_HEIGHT,
        )

        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.positions.pop()

        self.last = self.positions[-1] if len(self.positions) > 0 else None

    def get_head_position(self):
        """
        Возвращает позицию головы змейки.

        Returns:
            tuple: Позиция головы змейки (x, y)
        """
        return self.positions[0]

    def reset(self, screen_width, screen_height):
        """
        Сбрасывает змейку в начальное состояние.

        Args:
            screen_width (int): Ширина экрана
            screen_height (int): Высота экрана
        """
        self.positions = [(screen_width // 2, screen_height // 2)]
        self.direction = RIGHT
        self.length = 1

    def draw(self, screen):
        """
        Отрисовывает змейку на игровом поле.

        Args:
            screen: Экран, на котором будет отрисована змейка
        """
        for position in self.positions:
            pygame.draw.rect(
                screen,
                self.body_color,
                pygame.Rect(position[0], position[1], self.cell_size, self.cell_size),
            )
            pygame.draw.rect(
                screen,
                BORDER_COLOR,
                pygame.Rect(position[0], position[1], self.cell_size, self.cell_size),
                1,
            )

        if self.last:
            last_rect = pygame.Rect(self.last[0], self.last[1], self.cell_size, self.cell_size)
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def handle_keys(self):
        """Обрабатывает нажатия клавиш для изменения направления движения змейки."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != DOWN:
                    self.next_direction = UP
                elif event.key == pygame.K_DOWN and self.direction != UP:
                    self.next_direction = DOWN
                elif event.key == pygame.K_LEFT and self.direction != RIGHT:
                    self.next_direction = LEFT
                elif event.key == pygame.K_RIGHT and self.direction != LEFT:
                    self.next_direction = RIGHT


def main():
    """Основная функция игры, содержащая главный игровой цикл."""
    pygame.init()

    snake = Snake((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), GRID_SIZE)
    apple = Apple(SCREEN_WIDTH, SCREEN_HEIGHT, GRID_SIZE)

    while True:
        clock.tick(SPEED)

        snake.handle_keys()
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset(SCREEN_WIDTH, SCREEN_HEIGHT)

        screen.fill((0, 0, 0))
        snake.draw(screen)
        apple.draw(screen)

        pygame.display.update()


if __name__ == "__main__":
    main()
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 12

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для всех игровых объектов."""
    
    def __init__(self, position):
        """
        Инициализация игрового объекта.
        Args:
            position (tuple): Начальная позиция объекта (x, y)
        """
        self.position = position
        self.body_color = None

    def draw(self):
        """Метод для отрисовки объекта."""
        pass


class Apple(GameObject):
    """Класс для представления яблока в игре."""
    
    def __init__(self, screen_width, screen_height, cell_size):
        """
        Инициализируем яблоко.
        Args:
            screen_width (int): Ширина игрового поля
            screen_height (int): Высота игрового поля
            cell_size (int): Размер одной клетки на игровом поле
        """
        super().__init__(position=(0, 0))
        self.body_color = (255, 0, 0)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.cell_size = cell_size
        self.randomize_position()

    def randomize_position(self):
        """Генерируем случайное положение яблока на игровом поле."""
        x = randint(0, (self.screen_width // self.cell_size) - 1) * self.cell_size
        y = randint(0, (self.screen_height // self.cell_size) - 1) * self.cell_size
        self.position = (x, y)

    def draw(self, screen):
        """
        Отрисовывает яблоко на игровом поле.
        Args:
            screen: Экран, на котором будет отрисовано яблоко
        """
        pygame.draw.rect(screen, self.body_color, 
                        pygame.Rect(self.position[0], self.position[1], 
                                   self.cell_size, self.cell_size))


class Snake(GameObject):
    """Класс для представления змейки в игре."""
    
    def __init__(self, initial_position, cell_size):
        """
        Инициализация змейки.
        Args:
            initial_position (tuple): Начальная позиция змейки
            cell_size (int): Размер одной клетки на игровом поле
        """
        super().__init__(position=initial_position)
        self.body_color = (0, 255, 0)
        self.cell_size = cell_size
        self.positions = [initial_position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self.length = 1

    def update_direction(self):
        """Обновляет направление движения змейки на следующее."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Перемещает змейку в текущем направлении."""
        current_head = self.positions[0]
        new_x = current_head[0] + self.direction[0] * self.cell_size
        new_y = current_head[1] + self.direction[1] * self.cell_size
    
        if new_x >= SCREEN_WIDTH:
            new_x = 0
        elif new_x < 0:
            new_x = SCREEN_WIDTH - self.cell_size
        if new_y >= SCREEN_HEIGHT:
            new_y = 0
        elif new_y < 0:
            new_y = SCREEN_HEIGHT - self.cell_size
    
        new_head = (new_x, new_y)
    
        # Добавляем новую голову
        self.positions.insert(0, new_head)
    
        # Если длина змейки больше, чем должна быть, удаляем последний сегмент
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def get_head_position(self):
        """
        Возвращает позицию головы змейки.
        Returns: tuple: Позиция головы змейки (x, y)
        """
        return self.positions[0]

    def reset(self, screen_width, screen_height):
        """
        Сбрасывает змейку в начальное состояние.
        Args:
            screen_width (int): Ширина экрана
            screen_height (int): Высота экрана
        """
        self.positions = [(screen_width // 2, screen_height // 2)]
        self.direction = RIGHT
        self.length = 1
        self.next_direction = None
        self.last = None

    def draw(self, screen):
        """
        Отрисовывает змейку на игровом поле.
        Args:
            screen: Экран, на котором будет отрисована змейка
        """
        # Отрисовка всех сегментов змейки
        for position in self.positions:
            rect = pygame.Rect(position[0], position[1], self.cell_size, self.cell_size)
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        
        # Удаление последнего сегмента, если он есть
        if self.last:
            last_rect = pygame.Rect(self.last[0], self.last[1], self.cell_size, self.cell_size)
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def handle_keys(self):
        """Обрабатывает нажатия клавиш для изменения направления движения змейки."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != DOWN:
                    self.next_direction = UP
                elif event.key == pygame.K_DOWN and self.direction != UP:
                    self.next_direction = DOWN
                elif event.key == pygame.K_LEFT and self.direction != RIGHT:
                    self.next_direction = LEFT
                elif event.key == pygame.K_RIGHT and self.direction != LEFT:
                    self.next_direction = RIGHT


def main():
    """Основная функция игры, содержащая главный игровой цикл."""
    # Инициализация PyGame:
    pygame.init()

    # Создание экземпляров классов:
    snake = Snake((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), GRID_SIZE)
    apple = Apple(SCREEN_WIDTH, SCREEN_HEIGHT, GRID_SIZE)

    # Основной игровой цикл:
    while True:
        clock.tick(SPEED)

        # Обработка событий клавиш:
        snake.handle_keys()

        # Обновление направления движения змейки:
        snake.update_direction()

        # Движение змейки:
        snake.move()

        # Проверка, съела ли змейка яблоко:
        if snake.get_head_position() == apple.position:
            snake.length += 1  # Увеличение длины змейки
            apple.randomize_position()  # Перемещение яблока

        # Проверка столкновения змейки с собой:
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset(SCREEN_WIDTH, SCREEN_HEIGHT)  # Сброс игры

        # Отрисовка объектов:
        screen.fill(BOARD_BACKGROUND_COLOR)  # Очистка экрана
        snake.draw(screen)
        apple.draw(screen)

        # Обновление экрана:
        pygame.display.update()


if __name__ == '__main__':
    main()