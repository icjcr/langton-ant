import signal


class Ant:
    def __init__(
        self, pos_x: int, pos_y: int, dirn_x: int = -1, dirn_y: int = 0
    ) -> None:
        self.dirn = [dirn_x, dirn_y]
        self.pos = [pos_x, pos_y]

    def turn(self, color):
        if color:
            self.dirn[0], self.dirn[1] = self.dirn[1], -1 * self.dirn[0]
        else:
            self.dirn[0], self.dirn[1] = -1 * self.dirn[1], self.dirn[0]

    def step(self) -> None:
        if self.dirn[1] == 0:
            self.pos[0] += self.dirn[0]
        else:
            self.pos[1] += self.dirn[1]

    def convert_pos(self, width: int) -> int:
        return self.pos[1] * width + self.pos[0]


class Board:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.grid: list[int] = [0] * width * height

    def get_cell_color(self, pos):
        return self.grid[pos]

    def convert_pos(self, x: int, y: int) -> int:
        return y * self.width + x

    def invert_cell_color(self, pos):
        # negate
        self.grid[pos] = 1 - self.grid[pos]

    def draw(self) -> str:
        """
        :return: Drawing of the grid with "#" for black and " " for white.
        """
        # columns
        drawn_grid = "\n".join(
            # rows
            "".join(
                "#" if c else " "
                for i, c in enumerate(
                    self.grid[self.height * y: self.height * y + self.height]
                )
            )
            for y in range(self.height)
        )
        return drawn_grid


def main(board_: Board, ant_: Ant) -> None:
    signal.signal(signal.SIGINT, lambda signum, frame: exit())

    width = board_.width
    try:
        while True:
            print(board_.draw())
            print('-' * 13)
            pos = ant_.convert_pos(width)
            color = board_.get_cell_color(pos)
            ant_.turn(color)
            ant_.step()
            board_.invert_cell_color(pos)
    except (KeyboardInterrupt, EOFError, IndexError):
        exit()


if __name__ == "__main__":
    board_height = 10
    board_width = 10

    board = Board(height=board_height, width=board_width)
    ant = Ant(pos_x=board_width // 2, pos_y=board_height // 2)
    main(board, ant)
