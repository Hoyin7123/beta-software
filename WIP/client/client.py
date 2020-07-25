import arcade
import numpy as np

from gameview import GameView


# BOARD = np.zeros((8, 8), dtype=int)
# for y in range(3):
#     for x in range(8):
#         if y % 2 == 0 and x % 2 == 0:
#             BOARD[y][x] = 1
#         elif y % 2 != 0 and x % 2 != 0:
#             BOARD[y][x] = 1
#
# for y in range(5, 8):
#     for x in range(8):
#         if y % 2 == 0 and x % 2 == 0:
#             BOARD[y][x] = 2
#         elif y % 2 != 0 and x % 2 != 0:
#             BOARD[y][x] = 2

COLOR = 1

if __name__ == "__main__":
    win = arcade.Window(800, 800, "Checkers")
    win.show_view(GameView(win, COLOR))
    arcade.run()


