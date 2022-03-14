from human_player import HumanPlayer

from game.go_game import GoGame
import display
from typing import Tuple


def get_names() -> Tuple[str, str]:
    choice = input("Assign custom names [y/n]?  ").lower()
    if choice == "n":
        return "Black", "White"

    name_a = ""
    name_b = ""
    while not name_a:
        entry = input("Enter black player's name:  ")
        if bool(entry):
            name_a = entry

    while not name_b:
        entry = input("Enter white player's name:  ")
        if bool(entry):
            name_b = entry

    return name_a, name_b

def main():
    name_a, name_b = get_names()
    g = GoGame(HumanPlayer(name_a), HumanPlayer(name_b))
    while not g.board.g_over:
        print(display.format(g.board))
        g.step()

    print("\n" + display.format(g.board) + "\n")
    winning_score = max(g.board.white_score, g.board.black_score)
    losing_score = min(g.board.white_score, g.board.black_score)
    print(g.players[g.board.winner].name, "has won, with", winning_score, "to", losing_score)
