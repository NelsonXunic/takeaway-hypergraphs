from core.hypergraph import Hypergraph
from core.game import TakeAwayGame


def test_add_and_remove_vertex():
    hg = Hypergraph()
    hg.add_vertex("a")
    hg.add_vertex("b")
    assert "a" in hg.vertices
    assert "b" in hg.vertices

    hg.remove_vertex("a")
    assert "a" not in hg.vertices
    assert "b" in hg.vertices


def test_add_and_remove_edge():
    hg = Hypergraph()
    hg.add_vertex("a")
    hg.add_vertex("b")
    hg.add_edge({"a", "b"})
    assert {"a", "b"} in hg.edges

    hg.remove_edge({"a", "b"})
    assert {"a", "b"} not in hg.edges


def test_add_and_remove_face():
    hg = Hypergraph()
    for v in ["b", "c", "d", "e"]:
        hg.add_vertex(v)
    face = {"b", "c", "d", "e"}
    hg.add_face(face)
    assert face in hg.faces

    hg.remove_face(face)
    assert face not in hg.faces


def test_removal_of_vertex_cascades_edges_and_faces():
    hg = Hypergraph()
    for v in ["a", "b", "c", "d"]:
        hg.add_vertex(v)

    edge = {"a", "b"}
    face = {"b", "c", "d"}

    hg.add_edge(edge)
    hg.add_face(face)

    hg.remove_vertex("b")

    assert "b" not in hg.vertices
    assert edge not in hg.edges
    assert face not in hg.faces


def test_repr_for_debugging():
    hg = Hypergraph()
    hg.add_vertex("x")
    hg.add_edge({"x", "y"})
    hg.add_face({"x", "y", "z"})
    # Just check repr runs
    repr_output = repr(hg)
    assert isinstance(repr_output, str)


def test_basic_game():
    hg = Hypergraph()
    for v in ["a", "b", "c", "d"]:
        hg.add_vertex(v)
    hg.add_edge({"a", "b"})
    hg.add_face({"b", "c", "d"})

    game = TakeAwayGame(hg)
    game.move_vertex("a")
    assert "a" not in game.hypergraph.vertices
    game.move_hyperedge(["b", "c", "d"])
    assert len(game.hypergraph.faces) == 0
