import copy


class Coord:
    def __init__(self, r, c):
        self.row = r
        self.column = c

    def __eq__(self, other):
        return (self.row == other.row) and (self.column == other.column)

    def __str__(self):
        return "[" + str(self.row) + ", " + str(self.column) + "]"


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
    def __init__(self, komi=6.5):

        self._grid = []
        for i in range(19):
            row = []
            for j in range(19):
                row += [None]
            self._grid += [row]

        self.komi = komi
        self._turn = "b"
        self._winner = ""
        self._g_over = False
        self._black_score = 0
        self._white_score = 0

        self._consecutive_passes = 0
        self._white_captures = 0
        self._black_captures = 0

        self._display_chars = {
            None: ".",
            "b": "X",
            "w": "O"}

        self._position_history = [copy.deepcopy(self._grid)]

    @property
    def turn(self):
        return self._turn

    @property
    def winner(self):
        return self._winner

    @property
    def g_over(self):
        return self._g_over

    @property
    def position_history(self):
        return self._position_history

    @property
    def white_score(self):
        return self._white_score

    @property
    def black_score(self):
        return self._black_score

    def _get_contents(self, crd):
        return self._grid[crd.row][crd.column]

    def _set_contents(self, crd, value):
        self._grid[crd.row][crd.column] = value

    def as_string(self):
        output = "   A B C D E F G H J K L M N O P Q R S T   \n"
        for i in range(19, 0, -1):
            output += double_digit_fill_right(i) + " "
            for c in self._grid[i - 1]:
                output += self._display_chars[c] + " "
            output += double_digit_fill_left(i) + "\n"
        output += "   A B C D E F G H J K L M N O P Q R S T   \n"
        return output

    @staticmethod
    def _get_neighbours(crd):
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

    @staticmethod
    def _other_player(player):
        if player == "b":
            return "w"
        else:
            return "b"

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
            if self._get_contents(stone) == "w":
                self._black_captures += 1
            else:
                self._white_captures += 1
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
        self._turn = self._other_player(self._turn)

    def _is_suicide(self, coord):
        test_board = copy.deepcopy(self)
        test_board.make_move(coord)
        if test_board._get_contents(coord) is None:
            return True
        else:
            return False

    def _is_superko(self, coord):
        test_board = copy.deepcopy(self)
        test_board.make_move(coord)
        if len(self._position_history) > 2 and test_board._grid in self._position_history:
            return True
        else:
            return False

    def _get_empty_chains(self):
        empty_chains = []
        checked = []
        for i in range(len(self._grid)):
            for j in range(len(self._grid)):
                pos = Coord(i, j)
                if self._get_contents(pos) is None and pos not in checked:
                    chain = self._get_chain(pos)
                    checked += chain
                    empty_chains.append(chain)
        return empty_chains

    def _get_owner(self, empty_chain):
        neighbouring_colours = []
        for crd in empty_chain:
            n = self._get_neighbours(crd)
            for i in n:
                colour = self._get_contents(i)
                if i not in empty_chain and colour not in neighbouring_colours:
                    neighbouring_colours.append(colour)
        unique_neighbours = remove_duplicates(neighbouring_colours)
        if len(unique_neighbours) == 1:
            return unique_neighbours[0]
        else:
            return None

    def _get_territories(self):
        b_terr = 0
        w_terr = 0
        empty_chains = self._get_empty_chains()
        for c in empty_chains:
            ownership = self._get_owner(c)
            if ownership == "b":
                b_terr += len(c)
            elif ownership == "w":
                w_terr += len(c)
        return b_terr, w_terr

    def _end_game(self):
        self._turn = ""

        black_territory, white_territory = self._get_territories()
        self._black_score = black_territory - self._white_captures
        self._white_score = white_territory - self._black_captures + self.komi

        if self._white_score > self._black_score:
            self._winner = "w"
        else:
            self._winner = "b"

    def is_legal_move(self, coord):
        if (0 <= coord.row <= 18) and (0 <= coord.row <= 18):
            if self._get_contents(coord) is None:
                if not self._is_suicide(coord):
                    if not self._is_superko(coord):
                        return True, ""
                    else:
                        return False, "Repeats last board position"
                else:
                    return False, "Move results in suicide"
            else:
                return False, "Stones cannot be placed on other stones"
        else:
            return False, "Coordinates must be within the grid"

    def make_move(self, move_coord):
        self._place_stone(move_coord, self._turn)
        self._position_history.append(copy.deepcopy(self._grid))
        self._consecutive_passes = 0
        self._next_turn()

    def pass_turn(self):
        self._consecutive_passes += 1
        if self._consecutive_passes == 2:
            self._g_over = True
            self._end_game()
        else:
            self._next_turn()
