import copy
from .hypergraph import Hypergraph
from .utils import calculate_grundy


class TakeAwayGame:
    def __init__(self, initial_hypergraph: Hypergraph):
        self.hypergraph = initial_hypergraph
        self.history = []  # track moves
        self.players = ["Player 1", "Player 2"]
        self.current_player_index = 0
        self.winner = None

    @property
    def current_player(self):
        return self.players[self.current_player_index]

    # Ensures the vertex exists, Saves current state to history (for undo)
    # Calls hypergraph.remove_vertex() — which removes: The vertex,
    # all incident edges and faces
    # Checks for win condition
    # Switches player
    def move_vertex(self, vertex):
        if vertex not in self.hypergraph.vertices:
            raise ValueError(f"Vertex {vertex} not found in hypergraph")  # noqa: E713

        self.history.append(copy.deepcopy(self.hypergraph))
        self.hypergraph.remove_vertex(vertex)
        # self.history.append((self.current_player, f"remove vertex {vertex}"))

        if not self.hypergraph.vertices:
            self.winner = self.current_player
        self._next_player()

    def move_hyperedge(self, h):
        self.hypergraph.remove_hyperedge(set(h))
        self.history.append((self.current_player, f"remove hyperedge {h}"))
        self._next_player()

    # Restores previous hypergraph state and reverts turn to previous player.
    def undo(self):
        if not self.history:
            return
        self.hypergraph = self.history.pop()
        self._next_player()

    # Returns True if no vertices remain.
    def is_game_over(self):
        return self.hypergraph.is_empty()

    # Switches the active player between "Player 1" and "Player 2"
    def _next_player(self):
        self.current_player_index = 1 - self.current_player_index

    def __repr__(self):
        return f"Current player: {self.current_player}\n{self.hypergraph}"

    def get_current_grundy_number(self) -> int:
        """
        Calculates the Grundy number of the current hypergraph state.
        """
        return calculate_grundy(self.hypergraph)

    def is_losing_position(self) -> bool:
        """
        Checks if the current hypergraph state is a P-position (losing position for the current player).
        A P-position has a Grundy number of 0.
        """
        return self.get_current_grundy_number() == 0

    def is_winning_position(self) -> bool:
        """
        Checks if the current hypergraph state is an N-position (winning position for the current player).
        An N-position has a Grundy number greater than 0.
        """
        return self.get_current_grundy_number() > 0


if __name__ == "__main__":
    hg = Hypergraph()
    for v in ["a", "b", "c"]:
        hg.add_vertex(v)
    hg.add_edge({"a", "b"})
    hg.add_face({"b", "c"})

    game = TakeAwayGame(hg)
    print(game)
    game.move_vertex("b")
    print(game)
    if game.is_game_over():
        print(f"Winner: {game.winner}")
