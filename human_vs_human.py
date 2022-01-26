from human_player import HumanPlayer

from game.go_game import GoGame
import display


def main():
    g = GoGame(HumanPlayer(), HumanPlayer(), size=13)
    print(g.board.size)
    while not g.board.g_over:
        print(display.format(g.board))
        g.step()

    print("\n" + display.format(g.board) + "\n")
    winning_score = max(g.board.white_score, g.board.black_score)
    losing_score = min(g.board.white_score, g.board.black_score)
    print(g.board.winner, "has won, with", winning_score, "to", losing_score)


main()
