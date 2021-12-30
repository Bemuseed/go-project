from game import player, board
from random import choice

class DumbPlayer(player.Player):
    def get_move(self, game_board: board.Board):
        legals = []
        for r in range(len(game_board.grid)):
            for c in range(len(game_board.grid)):
                crd = board.Coord(r, c)
                if game_board.is_legal_move(crd):
                    legals.append(crd)
        legals.append(board.Coord(-1, -1))

        action = choice(legals)
        if action.row == -1:
            game_board.pass_turn()
        else:
            game_board.make_move(action)

        return game_board
