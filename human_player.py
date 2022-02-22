from game.player import Player
from game.board import Board, Move, Coord


def is_a_number(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


def alpha_to_column_number(alpha):
    order_in_alphabet = ord(alpha) - (ord('a') - 1)
    if ord(alpha) >= ord('i'):
        order_in_alphabet -= 1
    return order_in_alphabet - 1


def is_valid_coord(move_string):
    alpha = move_string[0].lower()
    if ord('a') <= ord(alpha) <= ord('t') and alpha != 'i':
        if is_a_number(move_string[1:]):
            return True


def is_pass(move_string):
    move_string = move_string.lower()
    if move_string == "p" or move_string == "pass":
        return True
    else:
        return False

def string_to_coord(coord_string: str) -> Coord:
    col = alpha_to_column_number(coord_string[0].lower())
    row = int(coord_string[1:]) - 1
    coord = Coord(row, col)
    return coord

def coord_to_string(coord: Coord) -> str:
    alpha = chr(coord.column + ord('a') + 1)
    num = str(coord.row + 1)
    return alpha + num

def get_valid_move():
    valid_coord = False
    coord = Coord
    pass_move = False
    while not valid_coord:
        entered_move= input("Enter move: ")
        if len(entered_move) > 0:
            valid_coord = is_valid_coord(entered_move)
            if not valid_coord:
                if is_pass(entered_move):
                    valid_coord = True
                    pass_move = True
                else:
                    print("Invalid coordinate.")
            else:
                coord = string_to_coord(entered_move)
        else:
            print("Please enter a valid coordinate.")
    return coord, pass_move


class HumanPlayer(Player):

    def get_move(self, game_board: Board) -> Move:
        move_complete = False
        move = Move()
        print("\nIt is " + game_board.turn + "'s turn.\n")
        while not move_complete:
            coordinate, pass_move = get_valid_move()
            move.coord = coordinate
            move.is_pass = pass_move
            legal, reason = game_board.is_legal_move(coordinate)
            if legal:
                move_complete = True
                return move
            else:
                print(reason)
