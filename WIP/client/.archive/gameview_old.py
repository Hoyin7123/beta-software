import arcade
import numpy as np

from piece import Piece


# Constants
HEIGHT = 100
WIDTH = 100


class GameView(arcade.View):
    def __init__(self, win, board):
        super().__init__(win)
        self.board = board
        self.is_turn = False
        self.piece_list = arcade.SpriteList()
        self.passive_hint_list = arcade.SpriteList()
        self.aggressive_hint_list = arcade.SpriteList()
        self.selected_piece = None

    @staticmethod
    def draw_grids():
        for y in range(8):  # y-axis
            for x in range(8):  # x-axis
                if y % 2 == 0 and x % 2 == 0:
                    arcade.draw_rectangle_filled(100*x+50, 100*y+50, WIDTH, HEIGHT, color=arcade.color.BLACK)
                elif y % 2 != 0 and x % 2 != 0:
                    arcade.draw_rectangle_filled(100*x+50, 100*y+50, WIDTH, HEIGHT, color=arcade.color.BLACK)
                else:
                    arcade.draw_rectangle_filled(100*x+50, 100*y+50, WIDTH, HEIGHT, color=arcade.color.ASH_GREY)

    def draw_init_pieces(self):
        for row_index, row in enumerate(self.board):
            for column_index, val in enumerate(row):
                if val == 1:
                    self.piece_list.append(Piece(column_index, row_index, 1))
                elif val == 2:
                    self.piece_list.append(Piece(column_index, row_index, 2))

    def get_valid_moves(self, column: int, row: int, is_king: bool, color: int) -> tuple:
        passive_valid_moves = []
        aggressive_valid_moves = []
        try:
            if color == 1:  # Red (Bottom)
                if not is_king:  # If the pieces is not king
                    print(1)
                    print(self.board)
                    if self.board[row+1][column-1] == 0:  # NW
                        passive_valid_moves.append((row+1, column-1))
                    elif self.board[row + 1][column - 1] != color and self.board[row + 2][column - 2] == 0:  # Eatable
                        aggressive_valid_moves.append((row + 2, column - 2))

                    if self.board[row+1][column+1] == 0:  # NE
                        passive_valid_moves.append((row+1, column+1))
                    elif self.board[row + 1][column + 1] != color and self.board[row + 2][column + 2] == 0:  # Eatable
                        aggressive_valid_moves.append((row + 2, column + 2))

                else:
                    print(2)
                    if self.board[row+1][column-1] == 0:  # NW
                        passive_valid_moves.append((row+1, column-1))
                    elif self.board[row + 1][column - 1] != color and self.board[row + 2][column - 2] == 0:  # Eatable
                        aggressive_valid_moves.append((row + 2, column - 2))

                    if self.board[row+1][column+1] == 0:  # NE
                        passive_valid_moves.append((row+1, column+1))
                    elif self.board[row + 1][column + 1] != color and self.board[row + 2][column + 2] == 0:  # Eatable
                        aggressive_valid_moves.append((row + 2, column + 2))

                    if self.board[row-1][column-1] == 0:  # SW
                        passive_valid_moves.append((row-1, column-1))
                    elif self.board[row - 1][column - 1] != color and self.board[row - 2][column - 2] == 0:  # Eatable
                        aggressive_valid_moves.append((row - 2, column - 2))

                    if self.board[row-1][column+1] == 0:  # SE
                        passive_valid_moves.append((row-1, column+1))
                    elif self.board[row - 1][column + 1] != color and self.board[row - 2][column + 2] == 0:  # Eatable
                        aggressive_valid_moves.append((row - 2, column + 2))

            else:  # Blue (Top)
                if not is_king:
                    print(3)
                    if self.board[row-1][column-1] == 0:  # SW
                        passive_valid_moves.append((row-1, column-1))
                    elif self.board[row - 1][column - 1] != color and self.board[row - 2][column - 2] == 0:  # Eatable
                        aggressive_valid_moves.append((row - 2, column - 2))

                    if self.board[row-1][column+1] == 0:  # SE
                        passive_valid_moves.append((row-1, column+1))
                    elif self.board[row - 1][column + 1] != color and self.board[row - 2][column + 2] == 0:  # Eatable
                        aggressive_valid_moves.append((row - 2, column + 2))

                else:
                    print(4)
                    if self.board[row-1][column-1] == 0:  # SW
                        passive_valid_moves.append((row-1, column-1))
                    elif self.board[row - 1][column - 1] != color and self.board[row - 2][column - 2] == 0:  # Eatable
                        aggressive_valid_moves.append((row - 2, column - 2))

                    if self.board[row-1][column+1] == 0:  # SE
                        passive_valid_moves.append((row-1, column+1))
                    elif self.board[row - 1][column + 1] != color and self.board[row - 2][column + 2] == 0:  # Eatable
                        aggressive_valid_moves.append((row - 2, column + 2))

                    if self.board[row + 1][column - 1] == 0:  # NW
                        passive_valid_moves.append((row + 1, column - 1))
                    elif self.board[row + 1][column - 1] != color and self.board[row + 2][column - 2] == 0:  # Eatable
                        aggressive_valid_moves.append((row + 2, column - 2))

                    if self.board[row + 1][column + 1] == 0:  # NE
                        passive_valid_moves.append((row + 1, column + 1))
                    elif self.board[row + 1][column + 1] != color and self.board[row + 2][column + 2] == 0:  # Eatable
                        aggressive_valid_moves.append((row + 2, column + 2))

        except IndexError:  # Not the best idea perhaps, but it works so far.
            pass

        # for move in passive_valid_moves:
        #     if move[0] > 7 or move[0] < 0:
        #         passive_valid_moves.remove(move)
        #     elif move[1] > 7 or move[1] < 0:
        #         passive_valid_moves.remove(move)
        #
        # for move in aggressive_valid_moves:
        #     if move[0] > 7 or move[0] < 0:
        #         aggressive_valid_moves.remove(move)
        #     elif move[1] > 7 or move[1] < 0:
        #         aggressive_valid_moves.remove(move)

        return passive_valid_moves, aggressive_valid_moves

    @staticmethod
    def get_index_from_coords(x: int, y: int) -> tuple:
        return (y-50)/100, (x-50)/100

    @staticmethod
    def get_coords_from_index(column: int, row: int) -> tuple:
        return column*100+50, row*100+50

    @staticmethod
    def get_direction_from_two_points(ori_coord: tuple, new_coord: tuple) -> str:
        if new_coord[0] > ori_coord[0]:
            if new_coord[1] > ori_coord[1]:
                return "NE"
            else:
                return "SE"
        else:
            if new_coord[1] > ori_coord[1]:
                return "NW"
            else:
                return "SW"

    def on_show(self):
        self.draw_init_pieces()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        pieces = arcade.get_sprites_at_point((x, y), self.piece_list)  # User clicks on a piece, shows hint
        if pieces:
            self.passive_hint_list = arcade.SpriteList()
            self.aggressive_hint_list = arcade.SpriteList()
            valid_moves = self.get_valid_moves(pieces[0].column, pieces[0].row, pieces[0].is_king, pieces[0].col)

            passive_valid_moves, aggressive_valid_moves = valid_moves
            print(passive_valid_moves, aggressive_valid_moves)
            for move in passive_valid_moves:
                hint = arcade.Sprite(filename="../src/green_hint.png",
                                     center_y=move[0]*100+50,
                                     center_x=move[1]*100+50,
                                     scale=0.1)
                self.passive_hint_list.append(hint)

            for move in aggressive_valid_moves:
                hint = arcade.Sprite(filename="../src/light_blue_hint.png",
                                     center_y=move[0]*100+50,
                                     center_x=move[1]*100+50,
                                     scale=0.1)
                self.aggressive_hint_list.append(hint)
            self.selected_piece = (pieces[0].row, pieces[0].column)

        clicked_passive_hints = arcade.get_sprites_at_point((x, y), self.passive_hint_list)
        if clicked_passive_hints:
            selected_coords = self.get_coords_from_index(self.selected_piece[1], self.selected_piece[0])
            pieces = arcade.get_sprites_at_point(selected_coords, self.piece_list)
            if pieces:
                piece = pieces[0]
                clicked_passive_hint = clicked_passive_hints[0]
                direction = self.get_direction_from_two_points((piece.center_x, piece.center_y),
                                                               (clicked_passive_hint.center_x, clicked_passive_hint.center_y))
                self.passive_hint_list = arcade.SpriteList()

                if direction == "NE":
                    piece.move_NE_p()
                    piece.column += 1
                    piece.row += 1
                elif direction == "SE":
                    piece.move_SE_p()
                    piece.column += 1
                    piece.row -= 1
                elif direction == "NW":
                    piece.move_NW_p()
                    piece.column -= 1
                    piece.row += 1
                elif direction == "SW":
                    piece.move_SW_p()
                    piece.column -= 1
                    piece.row -= 1

        clicked_aggressive_hints = arcade.get_sprites_at_point((x, y), self.aggressive_hint_list)
        if clicked_aggressive_hints:
            selected_coords = self.get_coords_from_index(self.selected_piece[1], self.selected_piece[0])
            print(self.selected_piece, self.piece_list, selected_coords)
            pieces = arcade.get_sprites_at_point(selected_coords, self.piece_list)
            if pieces:
                piece = pieces[0]
                clicked_aggressive_hint = clicked_aggressive_hints[0]
                direction = self.get_direction_from_two_coords((piece.center_x, piece.center_y),
                                                               (clicked_aggressive_hint.center_x,
                                                                clicked_aggressive_hint.center_y))

                self.aggressive_hint_list = arcade.SpriteList()

                original_index = (piece.row, piece.column)
                if direction == "NE":
                    piece.move_NE_p()
                    piece.column += 1
                    piece.row += 1
                elif direction == "SE":
                    piece.move_SE_p()
                    piece.column += 1
                    piece.row -= 1
                elif direction == "NW":
                    piece.move_NW_p()
                    piece.column -= 1
                    piece.row += 1
                elif direction == "SW":
                    piece.move_SW_p()
                    piece.column -= 1
                    piece.row -= 1

                self.board[original_index[0]][original_index[1]] = 0
                self.board[piece.row][piece.column] = piece.color


    def on_update(self, delta_time: float):
        self.piece_list.update()

    def on_draw(self):
        arcade.start_render()
        self.draw_grids()
        self.piece_list.draw()
        self.passive_hint_list.draw()
        self.aggressive_hint_list.draw()


