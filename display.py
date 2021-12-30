from game.board import Board


class GameDisplay:
    def __init__(self):
        self._alpha = "ABCDEFGHJKLMNOPQRSTUVWXYZabcdefghjklmnopqrstuvwxyz"

        self._display_chars = {
            None: ".",
            "b": "X",
            "w": "O"}

    @staticmethod
    def double_digit_fill_left(number) -> str:
        if int(number) >= 10:
            return str(number)
        elif int(number) >= 100:
            raise RuntimeError()
        else:
            return " " + str(number)

    @staticmethod
    def double_digit_fill_right(number) -> str:
        if int(number) >= 10:
            return str(number)
        elif int(number) >= 100:
            raise RuntimeError()
        else:
            return str(number) + " "

    def format(self, b: Board):
        banner = "   " + " ".join(self._alpha[:b.size]) + "   \n"
        output = banner
        for i in range(b.size, 0, -1):
            output += self.double_digit_fill_right(i) + " "
            for c in b.grid[i - 1]:
                output += self._display_chars[c] + " "
            output += self.double_digit_fill_left(i) + "\n"
        output += banner
        return output
