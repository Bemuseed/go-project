from board import *


"""Returns true if the string contains only numberical character"""
def is_a_number(string):
    try:
        int(string)
        return True
    except:
        return False


"""Prompts the user until they enter a whole number, returns this as
 an integer"""
def input_whole_num(prompt="", invalid_msg="", excepts=[]):
    num_entered = False
    while (not num_entered):
        inp_str = input(prompt)
        if (is_a_number(inp_str)):
            num_entered = True
        elif (inp_str.lower() in excepts):
            return -1
        else:
            print(invalid_msg, end="")
    return int(inp_str)


"""Prompts the current player for valid move coords, returns grid indeces"""
def move_prompt(board):
    valid_move = False
    print("\nIt is " + board.turn + "'s turn.\n")
    while (valid_move == False):
        row = input_whole_num("Enter row for stone:  ",
                              "Coords must be numbers\n", ["p", "pass"])

        if (row == -1):
            return coord(-1, -1)

        col = input_whole_num("Enter column for stone:  ",
                              "Coords must be numbers\n")

        row -= 1
        col -= 1
        coordinate = coord(row, col)
        val = board.is_valid_move(coordinate)
        if (val == True):
            valid_move = True
        else:
            print(val)
    return coordinate


def main():
    b = board()
    while (b.g_over != True):
        print(b.as_string())
        coord = move_prompt(b)
        if (coord.row == -1):
            b.pass_turn()
        else:
            b.make_move(coord)

        print(b.as_string())


main()
