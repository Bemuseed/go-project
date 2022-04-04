import copy
from typing import Optional, Tuple

from game.queue import Queue


class Coord:
    def __init__(self, r: int, c: int):
        self.row = r
        self.column = c

    def __eq__(self, other):
        return (self.row == other.row) and (self.column == other.column)

    def __repr__(self):
        return "<" + str(self.row) + ", " + str(self.column) + ">"

    def __str__(self):
        return self.__repr__()

    def __hash__(self):
        return int(str(self.row) + str(self.column))


class Move:
    def __init__(self, coord: Coord = None, is_pass: bool = False):
        self.coord = coord
        self.is_pass = is_pass

    def __eq__(self, other):
        return (self.coord == other.coord) and (self.is_pass == other.is_pass)

    def __hash__(self):
        return int(str(hash(self.coord)) + str(int(self.is_pass)))

    def __str__(self):
        if self.is_pass:
            return "[pass]"
        else:
            return str(self.coord)

    def __repr__(self):
        return self.__str__()


class Board:
    def __init__(self, komi: float = 6.5, size: int = 19):
        self.SIZE = size
        self.KOMI = komi

        grid_type = list[list[str]]
        self._grid: grid_type = []
        for i in range(self.SIZE):
            row = []
            for j in range(self.SIZE):
                row += [None]
            self._grid += [row]

        self._turn: str = "b"
        self._winner: str = ""
        self._g_over: bool = False
        self._black_score: float = 0
        self._white_score: float = 0

        self._consecutive_passes: int = 0
        self._white_captures: int = 0
        self._black_captures: int = 0
        self._position_history: list[grid_type] = [copy.deepcopy(self._grid)]

    def __eq__(self, other):
        if self.grid == other.grid:
            return True
        else:
            return False

    def __str__(self):
        return str(self._grid)

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

    @property
    def grid(self):
        return self._grid

    def _get_contents(self, crd: Coord) -> str:
        return self._grid[crd.row][crd.column]

    def _set_contents(self, crd: Coord, value: Optional[str]):
        self._grid[crd.row][crd.column] = value

    def _get_neighbours(self, crd: Coord) -> list[Coord]:
        r = crd.row
        c = crd.column

        neighbours = [Coord(r - 1, c),
                      Coord(r, c - 1),
                      Coord(r + 1, c),
                      Coord(r, c + 1)]
        valid_neighbours = []
        for i in range(4):
            if ((0 <= neighbours[i].row <= self.SIZE - 1) and
                    (0 <= neighbours[i].column <= self.SIZE - 1)):
                valid_neighbours += [neighbours[i]]
        return valid_neighbours

    @staticmethod
    def _other_player(player: str) -> str:
        if player == "b":
            return "w"
        else:
            return "b"

    def _get_chain(self, coord: Coord) -> list[Coord]:
        chain = [coord]
        to_check = Queue()
        to_check.enqueue(coord)
        colour = self._get_contents(coord)

        while not to_check.is_empty():
            neighbours = self._get_neighbours(to_check.dequeue())
            for i in neighbours:
                if self._get_contents(i) == colour:
                    if not (i in chain):
                        to_check.enqueue(i)
                        chain.append(i)
        return chain

    def _has_liberties(self, chain: list[Coord]) -> bool:
        for stone in chain:
            neighbours = self._get_neighbours(stone)
            for n in neighbours:
                if self._get_contents(n) is None:
                    return True
        return False

    def _capture(self, chain: list[Coord]):
        for stone in chain:
            if self._get_contents(stone) == "w":
                self._black_captures += 1
            else:
                self._white_captures += 1
            self._set_contents(stone, None)

    def _capture_if_without_liberties(self, crd: Coord):
        if self._get_contents(crd) is not None:
            chain = self._get_chain(crd)
            if not (self._has_liberties(chain)):
                self._capture(chain)

    def _place_stone(self, placement: Coord, colour: str):
        self._set_contents(placement, colour)
        affected_stones = self._get_neighbours(placement)
        affected_stones += [placement]
        for s in affected_stones:
            self._capture_if_without_liberties(s)

    def _next_turn(self):
        if self._turn != "":
            self._turn = self._other_player(self._turn)

    def _is_suicide(self, coord: Coord) -> bool:
        test_board = copy.deepcopy(self)
        test_board._make_move(coord)
        if test_board._get_contents(coord) is None:
            return True
        else:
            return False

    def _is_superko(self, coord: Coord) -> bool:
        test_board = copy.deepcopy(self)
        test_board._make_move(coord)
        if len(self._position_history) > 2 and test_board._grid in self._position_history:
            return True
        else:
            return False

    def _get_empty_chains(self) -> list[list[Coord]]:
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

    def _get_owner(self, empty_chain: list[Coord]) -> Optional[str]:
        neighbouring_colours = []
        for crd in empty_chain:
            n = self._get_neighbours(crd)
            for i in n:
                colour = self._get_contents(i)
                if i not in empty_chain and colour not in neighbouring_colours:
                    neighbouring_colours.append(colour)
        unique_neighbours = list(set(neighbouring_colours))
        if len(unique_neighbours) == 1:
            return unique_neighbours[0]
        else:
            return None

    def _get_territories(self) -> Tuple[int, int]:
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
        self._white_score = white_territory - self._black_captures + self.KOMI

        if self._white_score > self._black_score:
            self._winner = "w"
        elif self._black_score > self._white_score:
            self._winner = "b"
        else:
            self._winner = "-"

    def is_legal_move(self, move: Move) -> Tuple[bool, str]:
        if move.is_pass:
            return True, ""
        coord = move.coord
        if (0 <= coord.row <= self.SIZE - 1) and (0 <= coord.row <= self.SIZE - 1):
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

    def _make_move(self, move_coord: Coord):
        self._place_stone(move_coord, self._turn)
        self._consecutive_passes = 0
        self._position_history.append(copy.deepcopy(self._grid))

    def _pass_turn(self):
        self._consecutive_passes += 1
        if self._consecutive_passes == 2:
            self._g_over = True
            self._end_game()

    def take_turn(self, move: Move):
        if move.is_pass:
            self._pass_turn()
        else:
            self._make_move(move.coord)
        self._next_turn()
