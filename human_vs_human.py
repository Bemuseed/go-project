from game.board import Board
from human_player import HumanPlayer

from game.go_game import GoGame
import display
from typing import Tuple


def get_names() -> Tuple[str, str]:
    choice = input("Assign custom names [y/n]?  ").lower()
    if choice != "y":
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


def get_komi() -> float:
    komi = input("Komi for this game [default: 6.5]:  ")
    if komi.isnumeric():
        return float(komi)
    else:
        return 6.5

def get_size() -> int:
    size = input("Size of the board [between 5 and 30; default 19]:  ")
    if size.isnumeric():
        size = int(size)
        if 5 <= size <= 50:
            return size
    return 19


def main():
    size = get_size()
    name_a, name_b = get_names()
    komi = get_komi()
    g = GoGame(HumanPlayer(name_a), HumanPlayer(name_b), board=Board(komi=komi, size=size))
    while not g.board.g_over:
        print(display.format(g.board))
        g.step()

    print("\n" + display.format(g.board) + "\n")
    winning_score = max(g.board.white_score, g.board.black_score)
    losing_score = min(g.board.white_score, g.board.black_score)
    winner = g.board.winner
    if winner != "-":
        print(g.players[g.board.winner].name, "has won, with", winning_score, "to", losing_score)
    else:
        print(f"{list(g.players.values())[0].name} and {list(g.players.values())[1].name} have drawn with {winning_score} to {winning_score}!")
