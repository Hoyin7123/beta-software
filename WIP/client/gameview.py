import arcade
import numpy as np
from typing import Union, Optional

from piece import Piece
from error import *

# Constants
GRID_WIDTH = 100
GRID_HEIGHT = 100


class GameView(arcade.View):
    def __init__(self, win: arcade.Window, color: int):
        super().__init__(win)
        self.color = color
        self.piece_list = arcade.SpriteList()
        self.board = np.zeros((8, 8), dtype=int)
        self.passive_hints = arcade.SpriteList()
        self.aggro_hints = arcade.SpriteList()
        self.selected = None

        # Generate the initial board(2d array)
        for x in range(8):  # 1: Red
            for y in range(3):
                if y % 2 == 0 and x % 2 == 0:
                    self.board[y][x] = 1
                elif y % 2 != 0 and x % 2 != 0:
                    self.board[y][x] = 1

        for y in range(5, 8):  # 2: Blue
            for x in range(8):
                if y % 2 == 0 and x % 2 == 0:
                    self.board[y][x] = 2
                elif y % 2 != 0 and x % 2 != 0:
                    self.board[y][x] = 2

        self.is_turn = False

    @staticmethod
    def draw_grids():
        for y in range(8):  # y-axis
            for x in range(8):  # x-axis
                if y % 2 == 0 and x % 2 == 0:
                    arcade.draw_rectangle_filled(100 * x + 50, 100 * y + 50, GRID_WIDTH, GRID_HEIGHT,
                                                 color=arcade.color.BLACK)
                elif y % 2 != 0 and x % 2 != 0:
                    arcade.draw_rectangle_filled(100 * x + 50, 100 * y + 50, GRID_WIDTH, GRID_HEIGHT,
                                                 color=arcade.color.BLACK)
                else:
                    arcade.draw_rectangle_filled(100 * x + 50, 100 * y + 50, GRID_WIDTH, GRID_HEIGHT,
                                                 color=arcade.color.ASH_GREY)

    def draw_init_pieces(self):
        for row_index, row in enumerate(self.board):
            for column_index, val in enumerate(row):
                if val == 1:
                    self.piece_list.append(Piece((row_index, column_index), 1))
                elif val == 2:
                    self.piece_list.append(Piece((row_index, column_index), 2))

    @staticmethod
    def get_indices_from_coords(x: Union[int, float], y: Union[float, int]) -> tuple:
        x, y = int(x), int(y)
        return int((y - 50) / 100), int((x - 50) / 100)

    @staticmethod
    def get_coords_from_indices(indices: tuple) -> tuple:
        row, column = indices
        return column * 100 + 50, row * 100 + 50

    @staticmethod
    def get_direction_from_two_points(ori_coord: tuple, new_coord: tuple) -> str:
        if new_coord[0] > ori_coord[0]:
            if new_coord[1] > ori_coord[1]:
                return "ne"
            else:
                return "se"
        else:
            if new_coord[1] > ori_coord[1]:
                return "nw"
            else:
                return "sw"

    def get_passive_moves(self, indices: tuple, is_king: bool):
        print(indices)
        row, col = indices
        color = self.board[row][col]
        b = self.board
        passive_moves = []

        if color == 0:  # Neither 1 or 2 (Must be 0) --> Empty position
            raise EmptyPositionError("The indices passed is empty on board.")

        else:
            if color == 1:  # Red
                if row != 7 and col != 7:
                    if b[row + 1][col + 1] == 0:  # NE(SE)
                        passive_moves.append((row + 1, col + 1))
                if row != 7 and col != 0:
                    if b[row + 1][col - 1] == 0:  # NW(SW)
                        passive_moves.append((row + 1, col - 1))
                if is_king:
                    if row != 0 and col != 7:
                        if b[row - 1][col + 1] == 0:  # SE(NE)
                            passive_moves.append((row - 1, col + 1))
                    if row != 0 and col != 0:
                        if b[row - 1][col - 1] == 0:  # SW(NW)
                            passive_moves.append((row - 1, col - 1))
            else:
                if row != 0 and col != 7:
                    if b[row - 1][col + 1] == 0:  # SE(NE)
                        passive_moves.append((row - 1, col + 1))
                if row != 0 and col != 0:
                    if b[row - 1][col - 1] == 0:  # SW(NW)
                        passive_moves.append((row - 1, col - 1))
                if is_king:
                    if row != 7 and col != 7:
                        if b[row + 1][col + 1] == 0:  # NE(SE)
                            passive_moves.append((row + 1, col + 1))
                    if row != 7 and col != 0:
                        if b[row + 1][col - 1] == 0:  # NW(SW)
                            passive_moves.append((row + 1, col - 1))

        return passive_moves

    def get_aggro_moves(self, indices: tuple, is_king: bool):
        row, col = indices
        color = self.board[row][col]
        b = self.board
        aggro_moves = []

        if color == 0:  # Neither 1 or 2 (Must be 0) --> Empty position
            raise EmptyPositionError("The indices passed is empty on board.")

        else:
            if color == 1:  # Red
                if row < 6 and col < 6:
                    if b[row + 2][col + 2] == 0 and b[row + 1][col + 1] not in (0, color):
                        aggro_moves.append((row + 2, col + 2))
                if row < 6 and col > 1:
                    if b[row + 2][col - 2] == 0 and b[row + 1][col - 1] not in (0, color):
                        aggro_moves.append((row + 2, col - 2))

                if is_king:
                    if row > 1 and col < 6:
                        if b[row - 2][col + 2] == 0 and b[row - 1][col + 1] not in (0, color):
                            aggro_moves.append((row - 2, col + 2))
                    if row > 1 and col > 1:
                        if b[row - 2][col - 2] == 0 and b[row - 1][col - 1] not in (0, color):
                            aggro_moves.append((row - 2, col - 2))

            else:
                if row > 1 and col < 6:
                    if b[row - 2][col + 2] == 0 and b[row - 1][col + 1] not in (0, color):
                        aggro_moves.append((row - 2, col + 2))
                if row > 1 and col > 1:
                    if b[row - 2][col - 2] == 0 and b[row - 1][col - 1] not in (0, color):
                        aggro_moves.append((row - 2, col - 2))

                if is_king:
                    if row < 6 and col < 6:
                        if b[row + 2][col + 2] == 0 and b[row + 1][col + 1] not in (0, color):
                            aggro_moves.append((row + 2, col + 2))
                    if row < 6 and col > 1:
                        if b[row + 2][col - 2] == 0 and b[row + 1][col - 1] not in (0, color):
                            aggro_moves.append((row + 2, col - 2))

        return aggro_moves

    def move_piece(self, piece: Piece, direction: str, blocks: int, indices: Optional[tuple] = None) -> tuple:
        piece.move(direction, blocks)
        if not indices:
            x, y = piece.center_x, piece.center_y
            indices = self.get_indices_from_coords(x, y)
        row, col = indices
        color = self.board[row][col]
        if blocks == 1:
            if direction == "ne":
                dest_row, dest_col = row + 1, col + 1

            elif direction == "nw":
                dest_row, dest_col = row + 1, col - 1

            elif direction == "se":
                dest_row, dest_col = row - 1, col + 1

            elif direction == "sw":
                dest_row, dest_col = row - 1, col - 1

            else:
                raise Exception("Invalid Argument: direction passed!")

            self.board[row][col] = 0
            self.board[dest_row][dest_col] = color

            # point = self.get_coords_from_indices((dest_row, dest_col))
            # moved_pieces = arcade.get_sprites_at_point(point, self.piece_list)

        elif blocks == 2:
            if direction == "ne":
                dest_row, dest_col = row + 2, col + 2
                eaten_row, eaten_col = row + 1, col + 1

            elif direction == "nw":
                dest_row, dest_col = row + 2, col - 2
                eaten_row, eaten_col = row + 1, col - 1

            elif direction == "se":
                dest_row, dest_col = row - 2, col + 2
                eaten_row, eaten_col = row - 1, col + 1

            elif direction == "sw":
                dest_row, dest_col = row - 2, col - 2
                eaten_row, eaten_col = row - 1, col - 1

            else:
                raise Exception("Invalid Argument: direction passed!")

            self.board[row][col] = 0
            self.board[eaten_row][eaten_col] = 0
            self.board[dest_row][dest_col] = color

            x, y = self.get_coords_from_indices((eaten_row, eaten_col))
            eaten_piece = (arcade.get_sprites_at_point((x, y), self.piece_list))[0]
            self.piece_list.remove(eaten_piece)

            self.check_king_mutation(piece)

    def check_king_mutation(self, piece: Piece):
        row, _ = self.get_indices_from_coords(piece.center_x, piece.center_y)
        color = piece.col
        if color == 1 and row == 7:  # Red
            piece.is_king = True
        elif color == 2 and row == 0:  # Blue
            piece.is_king = True

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        clicked_p_hints = arcade.get_sprites_at_point((x, y), self.passive_hints)
        if clicked_p_hints:
            print("Passive hint clicked")
            p_hint = clicked_p_hints[0]
            self.passive_hints = arcade.SpriteList()
            self.aggro_hints = arcade.SpriteList()

            row, col = self.selected
            ori_x, ori_y = self.get_coords_from_indices((row, col))
            piece = (arcade.get_sprites_at_point((ori_x, ori_y), self.piece_list))[0]
            new_x, new_y = p_hint.center_x, p_hint.center_y

            direction = self.get_direction_from_two_points((ori_x, ori_y), (new_x, new_y))

            self.move_piece(piece, direction, 1)

            # self.is_turn = False

        clicked_a_hints = arcade.get_sprites_at_point((x, y), self.aggro_hints)
        if clicked_a_hints:
            print("Aggressive hint clicked")
            a_hint = clicked_a_hints[0]
            self.passive_hints = arcade.SpriteList()
            self.aggro_hints = arcade.SpriteList()

            row, col = self.selected
            ori_x, ori_y = self.get_coords_from_indices((row, col))
            piece = (arcade.get_sprites_at_point((ori_x, ori_y), self.piece_list))[0]
            new_x, new_y = a_hint.center_x, a_hint.center_y

            direction = self.get_direction_from_two_points((ori_x, ori_y), (new_x, new_y))

            self.move_piece(piece, direction, 2)

            # self.is_turn = False

        pieces = arcade.get_sprites_at_point((x, y), self.piece_list)
        if pieces:
            print("Pieces clicked")
            self.passive_hints = arcade.SpriteList()
            self.aggro_hints = arcade.SpriteList()
            piece = pieces[0]
            indices = self.get_indices_from_coords(piece.center_x, piece.center_y)
            passive_hints = self.get_passive_moves(indices, piece.is_king)
            aggro_hints = self.get_aggro_moves(indices, piece.is_king)

            self.selected = indices

            for i in passive_hints:
                x, y = self.get_coords_from_indices(i)
                hint = arcade.Sprite("src/green_hint.png", 0.1, center_x=x, center_y=y)
                self.passive_hints.append(hint)

            for i in aggro_hints:
                x, y = self.get_coords_from_indices(i)
                hint = arcade.Sprite("src/light_blue_hint.png", 0.1, center_x=x, center_y=y)
                self.aggro_hints.append(hint)

    def on_show(self):
        self.draw_init_pieces()
        # self.board[3][5] = 2
        # self.piece_list.append(Piece((3, 5), 2))

    def on_update(self, delta_time: float):
        self.piece_list.update()
        for piece in self.piece_list:
            self.check_king_mutation(piece)

    def on_draw(self):
        arcade.start_render()
        self.draw_grids()
        self.piece_list.draw()
        self.passive_hints.draw()
        self.aggro_hints.draw()
