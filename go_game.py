from board import *


def is_a_number(string):
    try:
        int(string)
        return True
    except:
        return False


def alpha_to_column_number(alpha):
    order_in_alphabet = ord(alpha) - (ord('a') - 1)
    if ord(alpha) >= ord('i'):
        order_in_alphabet -= 1
    return order_in_alphabet


def is_valid_move(move_string):
    if len(move_string) == 2:
        alpha = move_string[0].lower()
        if ord('a') <= ord(alpha) <= ord('t') and alpha != 'i':
            if is_a_number(move_string[1]):
                if 1 <= int(move_string[1]) <= 19:
                    return True


def is_pass(move_string):
    move_string = move_string.lower()
    if move_string == "p" or move_string == "pass":
        return True
    else:
        return False


def get_move():
    valid_move = False
    row, col = 0, 0
    while not valid_move:
        move = input("Enter move: ")
        valid_move = is_valid_move(move)
        if valid_move:
            col = alpha_to_column_number(move[0].lower())
            row = int(move[1])
        else:
            if not is_pass(move):
                print("Invalid coordinate.")
            else:
                valid_move = True
    return Coord(row-1, col-1)


def move_prompt(illegal_move_list, turn):
    legal_move = False
    coordinate = Coord(1, 1)
    print("\nIt is " + turn + "'s turn.\n")
    while legal_move is False:
        coordinate = get_move()

        in_list = False
        for i in illegal_move_list:
            if coordinate == i[0]:
                print(i[1])
                in_list = True

        if not in_list:
            legal_move = True

    return coordinate


def main():
    b = Board()
    while b.g_over is not True:
        print(b.as_string())
        illegal_moves = b.get_illegal_moves()
        turn = b.turn
        coord = move_prompt(illegal_moves, turn)
        if coord.row == -1:
            b.pass_turn()
        else:
            b.make_move(coord)

        print(b.as_string())


main()
