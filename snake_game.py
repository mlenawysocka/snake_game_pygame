import pygame
import random

pygame.font.init()

WIDTH, HEIGHT = 480, 480
SIZE = 20
WIDTH_BOX = WIDTH // SIZE
HEIGHT_BOX = HEIGHT // SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)


class Snake():
    def __init__(self):
        self.__len = 1
        self.__position = [(WIDTH // 2, HEIGHT // 2)]
        self.__move_direction = UP
        self.colour = GREEN
        self.score = 0

    def head_position(self):
        return self.__position[-1]  # zwracamy ostatni element z listy

    def direction(self, move_direction):
        if self.__len > 1 and (move_direction[0] * -1, move_direction[1] * -1) == self.__move_direction:
            return
        else:
            self.__move_direction = move_direction

    def move(self):
        head = self.head_position()
        x, y = self.__move_direction
        new_position = (((head[0] + (x * SIZE)) % WIDTH), (head[1] + (y * SIZE)) % HEIGHT)

        # uderzam w swoj ogon
        if len(self.__position) > 2 and new_position in self.__position[2:]:
            self.reset()
        # gdy uderzam w sufit lub podloge
        elif (new_position[1] == 0 and y == 1) or (new_position[1] == 460 and y == -1):
            self.reset()
        # gdy uderzam w prawa lub lewa sciane
        elif (new_position[0] == 0 and x == 1) or (new_position[0] == 460 and x == -1):
            self.reset()
        else:
            self.__position.append(new_position)
            if len(self.__position) > self.__len:
                del self.__position[0]

    def eat(self):
        self.__len += 1
        self.score += 1

    def reset(self):
        self.__len = 1
        self.__position = [(WIDTH // 2, HEIGHT // 2)]
        self.__move_direction = UP
        self.colour = GREEN
        self.score = 0

    def draw(self, win):
        for p in self.__position[::-1]:
            r = pygame.Rect((p[0], p[1]), (SIZE, SIZE))
            pygame.draw.rect(win, self.colour, r)


class Food():
    def __init__(self):
        self.position = (0, 0)
        self.colour = RED
        self.random_position()

    def random_position(self):
        self.position = (random.randint(0, WIDTH_BOX - 1) * SIZE, random.randint(0, HEIGHT_BOX - 1) * SIZE)

    def draw(self, win):
        rect = pygame.Rect(self.position, (SIZE, SIZE))
        pygame.draw.rect(win, self.colour, rect)


def draw_board(win):
    # tło
    win.fill(BLACK)

    # linie poziome
    for i in range(0, int(WIDTH_BOX)):
        pygame.draw.line(win, GRAY, (0, i * SIZE), (WIDTH, i * SIZE))
    # linie pionowe
    for i in range(0, int(WIDTH_BOX)):
        pygame.draw.line(win, GRAY, (i * SIZE, 0), (i * SIZE, WIDTH))


def main():
    pygame.init()

    # okno gry
    win = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
    pygame.display.set_caption('SNAKE GAME')

    # rysowanie siatki
    draw_board(win)

    # inicjalizacja obiektów z klas
    snake = Snake()
    food = Food()

    font = pygame.font.SysFont('arial', 24)

    # pętla głowna programu
    run = True
    while run:
        pygame.time.delay(100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.direction(UP)
                elif event.key == pygame.K_DOWN:
                    snake.direction(DOWN)
                elif event.key == pygame.K_LEFT:
                    snake.direction(LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake.direction(RIGHT)

        snake.move()
        if snake.head_position() == food.position:
            snake.eat()
            food.random_position()

        draw_board(win)
        snake.draw(win)
        food.draw(win)

        win.blit(win, (0, 0))

        result = font.render("Points: {0}".format(snake.score), 1, WHITE)
        win.blit(result, (10, HEIGHT - 30))

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
