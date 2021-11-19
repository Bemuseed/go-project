from game import player, board


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
    return order_in_alphabet


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


def get_valid_move():
    valid_coord = False
    row, col = 0, 0
    pass_move = False
    while not valid_coord:
        move = input("Enter move: ")
        if len(move) > 0:
            valid_coord = is_valid_coord(move)
            if not valid_coord:
                if is_pass(move):
                    valid_coord = True
                    pass_move = True
                else:
                    print("Invalid coordinate.")
            else:
                col = alpha_to_column_number(move[0].lower())
                row = int(move[1:])
        else:
            print("Please enter a valid coordinate.")
    return board.Coord(row - 1, col - 1), pass_move


class HumanPlayer(player.Player):

    def get_move(self, game_board: board.Board) -> board.Board:
        move_complete = False
        print("\nIt is " + game_board.turn + "'s turn.\n")
        while not move_complete:
            coordinate, pass_move = get_valid_move()
            legal, reason = game_board.is_legal_move(coordinate)
            if legal:
                game_board.make_move(coordinate)
                move_complete = True
            elif pass_move:
                game_board.pass_turn()
                move_complete = True
            else:
                print(reason)
        return game_board
