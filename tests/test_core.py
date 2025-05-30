from core.hypergraph import Hypergraph


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
    assert frozenset({"a", "b"}) in hg.edges
    assert len(hg.edges) == 1

    hg.remove_edge({"a", "b"})
    assert frozenset({"a", "b"}) not in hg.edges
    assert len(hg.edges) == 0


def test_add_and_remove_face():
    hg = Hypergraph()
    for v in ["b", "c", "d", "e"]:
        hg.add_vertex(v)
    face = {"b", "c", "d", "e"}
    hg.add_face(face)
    assert frozenset(face) in hg.faces
    assert len(hg.faces) == 1

    hg.remove_face(face)
    assert frozenset(face) not in hg.faces
    assert len(hg.faces) == 0


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
    assert frozenset(edge) not in hg.edges
    assert frozenset(face) not in hg.faces


def test_repr_for_debugging():
    hg = Hypergraph()
    hg.add_vertex("x")
    hg.add_vertex("y")
    hg.add_vertex("z")
    # Add edges and faces
    hg.add_edge({"x", "y"})
    hg.add_face({"x", "y", "z"})
    # Just check repr runs
    repr_output = repr(hg)
    assert isinstance(repr_output, str)
    # Check if it contains expected components
    assert "vertices=['x', 'y', 'z']" in repr_output
    # check for edges and faces as sorted tuples
    assert "[('x', 'y')]" in repr_output
    assert "[('x', 'y', 'z')]" in repr_output


def test_basic_game():
    from src.core.game import TakeAwayGame

    hg = Hypergraph()
    for v in ["a", "b", "c", "d"]:
        hg.add_vertex(v)
    hg.add_edge({"a", "b"})
    hg.add_face({"b", "c", "d"})

    game = TakeAwayGame(hg)
    game.move_vertex("a")
    assert "a" not in game.hypergraph.vertices
    # game.move_hyperedge(["b", "c", "d"])
    # assert len(game.hypergraph.faces) == 0


def test_hypergraph_equality():
    hg1 = Hypergraph()
    hg1.add_vertex("a")
    hg1.add_vertex("b")
    hg1.add_edge({"a", "b"})

    hg2 = Hypergraph()
    hg2.add_vertex("a")
    hg2.add_vertex("b")
    hg2.add_edge({"a", "b"})

    assert hg1 == hg2, "Two identical hypergraphs should be equal"

    hg3 = Hypergraph()
    hg3.add_vertex("a")
    hg3.add_vertex("c")  # Different vertex
    hg3.add_vertex("b")  # Also add b to avoid edge error
    # Same edge structure, but different vertices overall
    hg3.add_edge({"a", "b"})

    assert hg1 != hg3, "Hypergraphs with different vertex sets should not be equal"

    # Test with different order of adding vertices/edges, should still be equal
    hg4 = Hypergraph()
    hg4.add_vertex("b")  # Add in different order
    hg4.add_vertex("a")
    hg4.add_edge(
        {"b", "a"}
    )  # Order doesn't matter for frozenset, but ensure vertices exist

    assert hg1 == hg4, "Order of adding elements should not affect equality"

    # Test with faces
    hg5 = Hypergraph()
    hg5.add_vertex("x")
    hg5.add_vertex("y")
    hg5.add_vertex("z")
    hg5.add_face({"x", "y", "z"})

    hg6 = Hypergraph()
    hg6.add_vertex("z")  # Add in different order
    hg6.add_vertex("x")
    hg6.add_vertex("y")
    hg6.add_face({"z", "x", "y"})  # Face added in different order

    assert (
        hg5 == hg6
    ), "Hypergraphs with identical faces added in different order should be equal"

    hg7 = Hypergraph()
    hg7.add_vertex("x")
    hg7.add_vertex("y")
    hg7.add_vertex("w")  # Different face vertex
    hg7.add_face({"x", "y", "w"})

    assert hg5 != hg7, "Hypergraphs with different faces should not be equal"


def test_hypergraph_hashing():
    hg1 = Hypergraph()
    hg1.add_vertex("a")
    hg1.add_vertex("b")
    hg1.add_edge({"a", "b"})

    hg2 = Hypergraph()
    hg2.add_vertex("b")  # Different order of adding vertices
    hg2.add_vertex("a")
    hg2.add_edge({"b", "a"})  # Different order in edge set

    assert hash(hg1) == hash(hg2), "Identical hypergraphs should have the same hash"

    hg_dict = {}
    hg_dict[hg1] = "State 1"
    assert (
        hg_dict[hg2] == "State 1"
    ), "Hashing should allow retrieving identical states from dict"

    hg3 = Hypergraph()
    hg3.add_vertex("c")  # Different state
    hg3.add_vertex("d")
    hg3.add_edge({"c", "d"})

    assert hash(hg1) != hash(hg3), "Different hypergraphs should have different hashes"
    assert hg3 not in hg_dict, "Different hypergraphs should not be found in dict"

    # Test hashing with faces
    hg4 = Hypergraph()
    hg4.add_vertex("x")
    hg4.add_vertex("y")
    hg4.add_vertex("z")
    hg4.add_face({"x", "y", "z"})

    hg5 = Hypergraph()
    hg5.add_vertex("z")
    hg5.add_vertex("x")
    hg5.add_vertex("y")
    hg5.add_face({"z", "x", "y"})

    assert hash(hg4) == hash(
        hg5
    ), "Identical hypergraphs with faces should hash equally regardless of add order"
