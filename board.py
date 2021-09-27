class Coord:
    def __init__(self, r, c):
        self.row = r
        self.column = c

    def __eq__(self, other):
        return (self.row == other.row) and (self.column == other.column)


def double_digit_fill_left(number) -> str:
    if int(number) >= 10:
        return str(number)
    elif int(number) >= 100:
        raise RuntimeError()
    else:
        return " " + str(number)


def double_digit_fill_right(number) -> str:
    if int(number) >= 10:
        return str(number)
    elif int(number) >= 100:
        raise RuntimeError()
    else:
        return str(number) + " "


def remove_duplicates(lst):
    unique_lst = []
    for i in lst:
        if not (i in unique_lst):
            unique_lst += [i]
    return unique_lst


class Board:
    def __init__(self):

        self.grid = []
        for i in range(19):
            row = []
            for j in range(19):
                row += [None]
            self.grid += [row]

        self.turn = "b"
        self.winner = ""
        self.g_over = False

        self.display_chars = {
            None: ".",
            "b": "X",
            "w": "O"}

    def _get_contents(self, crd):
        return self.grid[crd.row][crd.column]

    def _set_contents(self, crd, value):
        self.grid[crd.row][crd.column] = value

    """Outputs an ASCII representation of the grid to the console"""

    def as_string(self):
        output = "   A B C D E F G H J K L M N O P Q R S T   \n"
        for i in range(19, 0, -1):
            output += double_digit_fill_right(i) + " "
            for c in self.grid[i - 1]:
                output += self.display_chars[c] + " "
            output += double_digit_fill_left(i) + "\n"
        output += "   A B C D E F G H J K L M N O P Q R S T   \n"
        return output

    def _other_player(self, player):
        if player == "b":
            return "w"
        else:
            return "b"

    def _is_valid_move(self, coord):
        if (0 <= coord.row <= 18) and (0 <= coord.row <= 18):
            if self._get_contents(coord) is None:
                return True
            else:
                return "Stones cannot be placed on other stones"
        else:
            return "Coordinates must be within the grid"

    def _get_neighbours(self, crd):
        r = crd.row
        c = crd.column

        neighbours = [Coord(r - 1, c),
                      Coord(r, c - 1),
                      Coord(r + 1, c),
                      Coord(r, c + 1)]
        valid_neighbours = []
        for i in range(4):
            if ((0 <= neighbours[i].row <= 18) and
                    (0 <= neighbours[i].column <= 18)):
                valid_neighbours += [neighbours[i]]
        return valid_neighbours

    def _get_chain(self, coord):
        chain = [coord]
        current = coord
        to_check = []
        colour = self._get_contents(coord)

        done = False
        while not done:
            neighbours = self._get_neighbours(current)
            for i in neighbours:
                if self._get_contents(i) == colour:
                    if not (i in chain):
                        to_check += [i]
                        chain += [i]
            if not to_check:
                done = True
            else:
                current = to_check[0]
                del to_check[0]
        return chain

    def _has_liberties(self, chain):
        for stone in chain:
            neighbours = self._get_neighbours(stone)
            for n in neighbours:
                if self._get_contents(n) is None:
                    return True
        return False

    def _capture(self, chain):
        for stone in chain:
            self._set_contents(stone, None)

    def _capture_if_without_liberties(self, crd):
        if self._get_contents(crd) is not None:
            chain = self._get_chain(crd)
            if not (self._has_liberties(chain)):
                self._capture(chain)

    def _place_stone(self, placed, colour):
        self._set_contents(placed, colour)
        affected_stones = self._get_neighbours(placed)
        affected_stones += [placed]
        for s in affected_stones:
            self._capture_if_without_liberties(s)

    def _next_turn(self):
        self.turn = self._other_player(self.turn)

    def make_move(self, move_coord):
        self._place_stone(move_coord, self.turn)
        self._next_turn()

    def pass_turn(self):
        self._next_turn()
