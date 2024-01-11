import pygame
import numpy as np
from random import sample

pygame.init()

screen = pygame.display.set_mode((800, 700))
pygame.display.set_caption("П`ятнашки")
icon = pygame.image.load("img/logo.jpg")
pygame.display.set_icon(icon)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SOFT_YELLOW = (238, 232, 170)

game_board = np.zeros((4, 4), dtype=int)

zero_positions_x = 3
zero_positions_y = 0

initial_point_x = 100
initial_point_y = 50

image_win_posit_x = 0
image_win_posit_y = 0

def game_board_randomizer():
    """ Функція, що заповнює масив game_board випадковими значеннями від 0 до 15.
        Значення вибираються таким чином, щоб існував спосіб переведення отриманої позиції у виграшну. """

    random_list = sample(range(1, 16), k=15)
    number_of_irregular_pairs = 0
    for i in range(15):
        current_number = random_list[i]
        for j in range(i + 1, 15):
            if current_number > random_list[j]:
                number_of_irregular_pairs += 1

    if number_of_irregular_pairs % 2 == 0:
        random_list[0], random_list[1] = random_list[1], random_list[0]

    random_list.append(0)
    number = 0
    regular_direction = True
    for i in range(4):
        for j in range(4):
            game_board[i, j] = random_list[number]
            if regular_direction and number % 4 == 3:
                number += 5
                regular_direction = not regular_direction
            elif not regular_direction and number % 4 == 0:
                number += 3
                regular_direction = not regular_direction

            if regular_direction:
                number += 1
            else:
                number -= 1


def game_board_descriptor():
    """Function to display the filled game board"""

    for i in range(4):
        for j in range(4):
            if game_board[i, j] != 0:
                try:
                    number_image = pygame.image.load("img/n_" + str(game_board[i, j]) + ".png")
                    screen.blit(number_image, (initial_point_x + 150*j, initial_point_y + 150*i))
                except pygame.error as e:
                    print(f"Error loading image: {e}")

winning_board = np.array([[1, 2, 3, 4,], [5, 6, 7, 8,], [9, 10, 11, 12,], [13, 14, 15, 0,]], dtype=int)

player_won = False

game_board_randomizer()
game_running = True

while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                if zero_positions_x - 1 >= 0:
                    game_board[zero_positions_x, zero_positions_y], game_board[zero_positions_x - 1, zero_positions_y] = \
                        game_board[zero_positions_x - 1, zero_positions_y], game_board[zero_positions_x, zero_positions_y]
                    zero_positions_x -= 1

            elif event.key == pygame.K_w or event.key == pygame.K_UP:
                if zero_positions_x + 1 <= 3:
                    game_board[zero_positions_x, zero_positions_y], game_board[zero_positions_x + 1, zero_positions_y] = \
                        game_board[zero_positions_x + 1, zero_positions_y], game_board[zero_positions_x, zero_positions_y]
                    zero_positions_x += 1

            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                if zero_positions_y + 1 <= 3:
                    game_board[zero_positions_x, zero_positions_y], game_board[zero_positions_x, zero_positions_y + 1] = \
                        game_board[zero_positions_x, zero_positions_y + 1], game_board[zero_positions_x, zero_positions_y]
                    zero_positions_y += 1

            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                if zero_positions_y - 1 >= 0:
                    game_board[zero_positions_x, zero_positions_y], game_board[zero_positions_x, zero_positions_y - 1] = \
                        game_board[zero_positions_x, zero_positions_y - 1], game_board[zero_positions_x, zero_positions_y]
                    zero_positions_y -= 1

    if player_won:
        winning_image = pygame.image.load("img/win.png")
        screen.blit(winning_image, (image_win_posit_x, image_win_posit_y))
        pygame.display.update()
        pygame.time.delay(2000)
        game_running = False
    else:
        screen.fill(WHITE)
        game_board_descriptor()  
        pygame.display.update()  
        pygame.time.delay(150)  


pygame.quit()
