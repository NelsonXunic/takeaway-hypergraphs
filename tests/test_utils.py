from src.core.utils import (
    calculate_mex,
    calculate_grundy,
    build_game_tree,
)
from src.core.hypergraph import Hypergraph


def test_mex_empty_set():
    """Test MEX with an empty set."""
    assert calculate_mex(set()) == 0


def test_mex_consecutive_from_zero():
    """Test MEX with consecutive numbers starting from zero."""
    assert calculate_mex({0, 1, 2}) == 3


def test_mex_missing_first_number():
    """Test MEX when 0 is missing."""
    assert calculate_mex({1, 2, 3}) == 0


def test_mex_missing_middle_number():
    """Test MEX when a number in the middle is missing."""
    assert calculate_mex({0, 2, 4}) == 1
    assert calculate_mex({0, 1, 3, 5}) == 2


def test_mex_large_numbers():
    """Test MEX with larger numbers, where 0 is missing."""
    assert calculate_mex({10, 20, 30}) == 0


def test_mex_unordered_input_with_duplicates():
    """Test MEX with an unordered set and duplicates."""
    # Python sets automatically handle duplicates and maintain no order,
    # so this test primarily checks the function's robustness.
    assert calculate_mex({3, 0, 1, 3, 2, 0}) == 4
    assert calculate_mex({5, 1, 0, 3}) == 2


def test_mex_single_number():
    """Test MEX with a single non-zero number."""
    assert calculate_mex({5}) == 0
    assert calculate_mex({0}) == 1


def test_grundy_empty_hypergraph():
    """Test Grundy number for an empty hypergraph (base case)."""
    hg = Hypergraph()
    assert calculate_grundy(hg) == 0


def test_grundy_single_isolated_vertex():
    """Test Grundy for a single isolated vertex."""
    hg = Hypergraph()
    hg.add_vertex("a")
    # Possible moves: remove "a" -> results in empty hypergraph (Grundy 0)
    # Reachable Grundy numbers: {0}
    # MEX({0}) = 1
    assert calculate_grundy(hg) == 1


def test_grundy_two_isolated_vertices():
    """Test Grundy for two isolated vertices."""
    hg = Hypergraph()
    hg.add_vertex("a")
    hg.add_vertex("b")
    # Possible moves:
    # 1. Remove "a" -> hypergraph with only "b" (Grundy 1)
    # 2. Remove "b" -> hypergraph with only "a" (Grundy 1)
    # Reachable Grundy numbers: {1}
    # MEX({1}) = 0
    assert calculate_grundy(hg) == 0


def test_grundy_hypergraph_with_one_edge():
    """Test Grundy for a hypergraph with two vertices and one edge."""
    hg = Hypergraph()
    hg.add_vertex("a")
    hg.add_vertex("b")
    hg.add_edge({"a", "b"})
    # Possible moves:
    # 1. Remove "a" -> hypergraph with "b", no edges (Grundy for {"b"} is 1)
    # 2. Remove "b" -> hypergraph with "a", no edges (Grundy for {"a"} is 1)
    # Reachable Grundy numbers: {1}
    # MEX({1}) = 0
    assert calculate_grundy(hg) == 0


def test_grundy_hypergraph_with_one_face():
    """Test Grundy for a hypergraph with three vertices and one face."""
    hg = Hypergraph()
    hg.add_vertex("a")
    hg.add_vertex("b")
    hg.add_vertex("c")
    hg.add_face({"a", "b", "c"})
    # Possible moves:
    # 1. Remove "a" -> hypergraph with {"b", "c"}, no faces (Grundy for {"b", "c"} is 0)
    # 2. Remove "b" -> hypergraph with {"a", "c"}, no faces (Grundy for {"a", "c"} is 0)
    # 3. Remove "c" -> hypergraph with {"a", "b"}, no faces (Grundy for {"a", "b"} is 0)
    # Reachable Grundy numbers: {0}
    # MEX({0}) = 1
    assert calculate_grundy(hg) == 1


def test_grundy_memoization():
    """Test that memoization is working by clearing cache and re-running."""
    # This test relies on internal implementation detail (lru_cache.cache_info())
    # but is useful for verifying memoization.
    from src.core.utils import calculate_grundy  # Re-import to access cache_info

    # Clear the cache before running this specific test
    calculate_grundy.cache_clear()
    assert calculate_grundy.cache_info().hits == 0
    assert calculate_grundy.cache_info().misses == 0

    hg1 = Hypergraph()
    hg1.add_vertex("a")
    hg1.add_vertex("b")

    hg2 = Hypergraph()
    hg2.add_vertex("b")
    hg2.add_vertex(
        "a"
    )  # Same structure, different order, should hit cache on second call

    grundy_val_1 = calculate_grundy(hg1)
    assert (
        calculate_grundy.cache_info().misses == 4
    )  # Initial hg1, and its two successors ({"a"}, {"b"})

    grundy_val_2 = calculate_grundy(hg2)
    # hg2 is identical to hg1 (due to __eq__ and __hash__), so it should be a cache hit.
    # Its children ({"a"}, {"b"}) should also be cache hits.
    assert calculate_grundy.cache_info().hits == 2  # hg2 itself, plus its children

    assert (
        grundy_val_1 == grundy_val_2 == 0
    )  # Based on previous test_grundy_two_isolated_vertices

    # Verify that Grundy for an empty graph is also cached
    empty_hg = Hypergraph()
    calculate_grundy(
        empty_hg
    )  # This will be a cache hit if it was encountered during other runs

    # Expect more hits due to repeated calls on identical states (like empty graphs, single-vertex graphs)
    assert calculate_grundy.cache_info().hits > 0


def test_build_game_tree_empty_hypergraph():
    """Test building a game tree for an empty hypergraph (base case)."""
    hg = Hypergraph()
    tree = build_game_tree(hg)
    assert tree["state"] == str(hg)
    assert tree["grundy_number"] == 0
    assert tree["children"] == []
    assert "truncated" not in tree
    assert "cycle_detected" not in tree


def test_build_game_tree_single_isolated_vertex():
    """Test building a game tree for a single isolated vertex."""
    hg = Hypergraph()
    hg.add_vertex("a")
    tree = build_game_tree(hg)

    assert tree["state"] == str(hg)
    assert tree["grundy_number"] == 1
    assert len(tree["children"]) == 1

    child = tree["children"][0]
    expected_child_hg = Hypergraph()  # Empty hypergraph
    assert child["state"] == str(expected_child_hg)
    assert child["grundy_number"] == 0
    assert child["children"] == []


def test_build_game_tree_two_isolated_vertices():
    """Test building a game tree for two isolated vertices."""
    hg = Hypergraph()
    hg.add_vertex("a")
    hg.add_vertex("b")
    tree = build_game_tree(hg)

    assert tree["state"] == str(hg)
    assert tree["grundy_number"] == 0
    assert len(tree["children"]) == 2

    # Child 1: Remove 'a' -> {'b'}
    child1 = tree["children"][0]
    expected_child1_hg = Hypergraph()
    expected_child1_hg.add_vertex("b")
    assert child1["state"] == str(expected_child1_hg)
    assert child1["grundy_number"] == 1
    assert len(child1["children"]) == 1
    assert child1["children"][0]["state"] == str(Hypergraph())  # Grandchild is empty

    # Child 2: Remove 'b' -> {'a'}
    child2 = tree["children"][1]
    expected_child2_hg = Hypergraph()
    expected_child2_hg.add_vertex("a")
    assert child2["state"] == str(expected_child2_hg)
    assert child2["grundy_number"] == 1
    assert len(child2["children"]) == 1
    assert child2["children"][0]["state"] == str(Hypergraph())  # Grandchild is empty
