from board import *


def is_a_number(string):
    try:
        int(string)
        return True
    except:
        return False


def input_whole_num(prompt="", invalid_msg="", excepts=None):
    if excepts is None:
        excepts = []
    inp_str = ""
    num_entered = False
    while not num_entered:
        inp_str = input(prompt)
        if is_a_number(inp_str):
            num_entered = True
        elif inp_str.lower() in excepts:
            return -1
        else:
            print(invalid_msg, end="")
    return int(inp_str)


def move_prompt(board):
    valid_move = False
    coordinate = Coord(1, 1)
    print("\nIt is " + board.turn + "'s turn.\n")
    while valid_move is False:
        row = input_whole_num("Enter row for stone:  ",
                              "Coords must be numbers\n", ["p", "pass"])

        if row == -1:
            return Coord(-1, -1)

        col = input_whole_num("Enter column for stone:  ",
                              "Coords must be numbers\n")

        coordinate.row = row - 1
        coordinate.column = col - 1
        val = board.is_valid_move(coordinate)
        if val is True:
            valid_move = True
        else:
            print(val)
    return coordinate


def main():
    b = Board()
    while b.g_over is not True:
        print(b.as_string())
        coord = move_prompt(b)
        if coord.row == -1:
            b.pass_turn()
        else:
            b.make_move(coord)

        print(b.as_string())


main()
