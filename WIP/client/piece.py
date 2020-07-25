import arcade

# Constants
SCALE = 0.095


class Piece(arcade.Sprite):
    def __init__(self, indices: tuple, color: int):
        row, column = indices
        pos_x = column * 100 + 50
        pos_y = row * 100 + 50
        self.col = color
        self.is_king = False
        self.king_texture_red = arcade.load_texture("./src/red_king.png")
        self.king_texture_blue = arcade.load_texture("./src/blue_king.png")
        self.destination = (pos_x, pos_y)
        self.direction = None
        self.vel = 10

        if color == 1:
            filename = "src/red_norm.png"
        else:
            filename = "src/blue_norm.png"
        super().__init__(center_x=pos_x, center_y=pos_y, scale=SCALE, filename=filename)

    def move(self, direction: str, blocks: int = 1):
        if direction.lower() == "ne":
            self.destination = (self.center_x + blocks * 100, self.center_y + blocks * 100)
        elif direction.lower() == "nw":
            self.destination = (self.center_x - blocks * 100, self.center_y + blocks * 100)
        elif direction.lower() == "se":
            self.destination = (self.center_x + blocks * 100, self.center_y - blocks * 100)
        elif direction.lower() == "sw":
            self.destination = (self.center_x - blocks * 100, self.center_y - blocks * 100)

    def update(self):
        if self.center_x != self.destination[0]:
            if self.center_x > self.destination[0]:
                self.center_x -= self.vel
            else:
                self.center_x += self.vel
        if self.center_y != self.destination[1]:
            if self.center_y > self.destination[1]:
                self.center_y -= self.vel
            else:
                self.center_y += self.vel

        if self.is_king and self.col == 1:
            self.texture = self.king_texture_red

        elif self.is_king and self.col == 2:
            self.texture = self.king_texture_blue
