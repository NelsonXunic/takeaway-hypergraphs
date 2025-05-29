import pytest
from core.hypergraph import Hypergraph
from core.game import TakeAwayGame


def setup_hypergraph():
    hg = Hypergraph()
    for v in ["a", "b", "c"]:
        hg.add_vertex(v)
    hg.add_edge({"a", "b"})
    hg.add_face({"b", "c"})
    return hg


def test_initial_state():
    hg = setup_hypergraph()
    game = TakeAwayGame(hg)
    assert game.current_player == "Player 1"
    assert not game.is_game_over()
    assert game.winner is None


def test_player_switching():
    hg = setup_hypergraph()
    game = TakeAwayGame(hg)
    assert game.current_player == "Player 1"
    game._next_player()
    assert game.current_player == "Player 2"
    game._next_player()
    assert game.current_player == "Player 1"


def test_move_vertex_and_win():
    hg = Hypergraph()
    hg.add_vertex("x")
    game = TakeAwayGame(hg)
    game.move_vertex("x")
    assert game.is_game_over()
    assert game.winner == "Player 1"


def test_move_vertex_and_edge_removal():
    hg = setup_hypergraph()
    game = TakeAwayGame(hg)
    game.move_vertex("b")
    assert "b" not in game.hypergraph.vertices
    assert {"a", "b"} not in game.hypergraph.edges
    assert {"b", "c"} not in game.hypergraph.faces


def test_invalid_move_raises():
    hg = setup_hypergraph()
    game = TakeAwayGame(hg)
    with pytest.raises(ValueError):
        game.move_vertex("z")


def test_undo():
    hg = setup_hypergraph()
    game = TakeAwayGame(hg)
    game.move_vertex("a")
    assert "a" not in game.hypergraph.vertices
    game.undo()
    assert "a" in game.hypergraph.vertices
    assert game.current_player == "Player 1"
