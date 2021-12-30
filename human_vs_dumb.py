from human_player import HumanPlayer
from dumb_player import DumbPlayer
from game.go_game import GoGame


def main():
    g = GoGame(HumanPlayer(), DumbPlayer())
    g.play()

    print("\n" + g.board.as_string() + "\n")
    winning_score = max(g.board.white_score, g.board.black_score)
    losing_score = min(g.board.white_score, g.board.black_score)
    print(g.board.winner, "has won, with", winning_score, "to", losing_score)


main()
