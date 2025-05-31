import pytest
from src.core.utils import (
    calculate_mex,
    calculate_grundy,
    build_game_tree,
    print_game_tree,
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

    # Define expected child states
    expected_child_hg_a = Hypergraph()  # Hypergraph with only 'a'
    expected_child_hg_a.add_vertex("a")

    expected_child_hg_b = Hypergraph()  # Hypergraph with only 'b'
    expected_child_hg_b.add_vertex("b")

    expected_child_states = {str(expected_child_hg_a), str(expected_child_hg_b)}

    # Extract actual child states
    actual_child_states = {child["state"] for child in tree["children"]}

    # Assert that the set of actual states matches the set of expected states
    assert actual_child_states == expected_child_states

    # Now, verify properties of each child by searching for its state
    for child in tree["children"]:
        if child["state"] == str(expected_child_hg_a):
            assert child["grundy_number"] == 1
            assert len(child["children"]) == 1
            assert child["children"][0]["state"] == str(
                Hypergraph()
            )  # Grandchild should be empty
        elif child["state"] == str(expected_child_hg_b):
            assert child["grundy_number"] == 1
            assert len(child["children"]) == 1
            assert child["children"][0]["state"] == str(
                Hypergraph()
            )  # Grandchild should be empty
        else:
            pytest.fail(f"Unexpected child state found: {child['state']}")


def test_build_game_tree_max_depth_truncation():
    """Test that max_depth correctly truncates the tree."""
    hg = Hypergraph()
    hg.add_vertex("a")
    hg.add_vertex("b")  # Grundy 0

    # Max depth 0: Only the root node
    tree_depth_0 = build_game_tree(hg, max_depth=0)
    assert tree_depth_0["state"] == str(hg)
    assert tree_depth_0["grundy_number"] == 0
    assert tree_depth_0["children"] == []
    assert tree_depth_0["truncated"] is True

    # Max depth 1: Root node and its direct children
    tree_depth_1 = build_game_tree(hg, max_depth=1)
    assert tree_depth_1["state"] == str(hg)
    assert tree_depth_1["grundy_number"] == 0
    assert len(tree_depth_1["children"]) == 2
    assert "truncated" not in tree_depth_1  # Root is not truncated

    # Children should be truncated
    for child in tree_depth_1["children"]:
        assert len(child["children"]) == 0
        assert child["truncated"] is True
        assert child["grundy_number"] == 1  # Single vertex Grundy


# Test print_game_tree (manual verification, but a simple test can ensure it runs)
def test_print_game_tree_runs_without_error(capsys):
    """Test that print_game_tree executes without errors and produces some output."""
    hg = Hypergraph()
    hg.add_vertex("x")
    hg.add_vertex("y")
    tree = build_game_tree(hg)

    print_game_tree(tree)
    captured = capsys.readouterr()  # Capture stdout/stderr
    assert "State: V" in captured.out
    assert "Grundy: 0 (P-position)" in captured.out
    assert "Grundy: 1 (N-position)" in captured.out
    assert "TRUNCATED" not in captured.out  # Should not be truncated
    assert "CYCLE DETECTED" not in captured.out  # Should not have cycles
