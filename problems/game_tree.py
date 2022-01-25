import copy
from game.board import Board, Coord

class GameNode:
    def __init__(self, game_state: Board, comment=None):
        self._children = {}
        self.game_state = game_state
        self.comment = comment
        self.end_node = False

    def __str__(self):
        return self.game_state

    @property
    def children(self) -> dict:
        return self._children

    @property
    def child_moves(self) -> list[Coord]:
        return list(self._children.keys())

    @property
    def child_nodes(self) -> list:
        return list(self._children.values())

    @property
    def child_states(self) -> list[Board]:
        return [n.game_state for n in self.child_nodes]

    def get_child_from_move(self, move: Coord):
        return self._children[move]

    def get_child_from_state(self, state: Board):
        for n in self.child_nodes:
            if n.game_state == state:
                return n
        raise RuntimeError("State not found.")

    def add_child(self, move: Coord):
        state_copy = copy.deepcopy(self.game_state)
        state_copy.make_move(move)
        child_node = GameNode(state_copy)
        self._children[move] = child_node

class GameTree:
    def __init__(self, root: GameNode):
        self._root = root

    @property
    def nodes(self):
        node_count = 1
        for c in self._root.child_nodes:
            t = GameTree(c)
            node_count += t.nodes
        return node_count

    @property
    def root(self):
        return self._root

    def traverse(self, moves: list[Coord]):
        nd = self.root
        for m in moves:
            nd = nd.children[m]
        return nd

    def add_line(self, base_node: GameNode, moves: list[Coord]):
        current_node = base_node
        for m in moves:
            current_node.add_child(m)
            current_node = current_node.child_nodes[-1]