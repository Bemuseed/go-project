from game.board import Board


ALPHA = "ABCDEFGHJKLMNOPQRSTUVWXYZabcdefghjklmnopqrstuvwxyz"
DISPLAY_CHARS = {
    None: ".",
    "b": "X",
    "w": "O"}


def double_digit_fill_left(number: str) -> str:
    if int(number) >= 10:
        return str(number)
    elif int(number) >= 100:
        raise RuntimeError()
    else:
        return " " + str(number)


def double_digit_fill_right(number: str) -> str:
    if int(number) >= 10:
        return str(number)
    elif int(number) >= 100:
        raise RuntimeError()
    else:
        return str(number) + " "


def format(b: Board) -> str:
    banner = "   " + " ".join(ALPHA[:b.size]) + "   \n"
    output = banner
    for i in range(b.size, 0, -1):
        output += double_digit_fill_right(i) + " "
        for c in b.grid[i - 1]:
            output += DISPLAY_CHARS[c] + " "
        output += double_digit_fill_left(i) + "\n"
    output += banner
    return output
