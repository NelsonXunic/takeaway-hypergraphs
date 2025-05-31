from functools import lru_cache
from src.core.hypergraph import Hypergraph


def calculate_mex(s: set[int]) -> int:
    """
    Calculates the Minimum Excluded (MEX) value from a set of non-negative integers.
    The MEX is the smallest non-negative integer not present in the set.

    Args:
        s: A set of non-negative integers.

    Returns:
        The MEX value.
    """
    # Convert the set to a list and sort it to ensure ordered iteration
    # This is robust because sets don't guarantee order.
    sorted_s = sorted(list(s))

    mex = 0
    for num in sorted_s:
        if num == mex:
            mex += 1
        elif num > mex:
            # If we encounter a number greater than mex, it means mex
            # was missing from the set, so we've found our MEX.
            return mex
    return mex  # If loop completes, mex is the next number in sequence


# We'll use lru_cache for memoization.
# The `maxsize=None` makes it an unbounded cache, storing all results.
@lru_cache(maxsize=None)
def calculate_grundy(hypergraph: Hypergraph) -> int:
    """
    Calculates the Grundy number (nim-value) for a given hypergraph state.
    Uses memoization to store already calculated Grundy numbers.

    Args:
        hypergraph: The current Hypergraph state.

    Returns:
        The Grundy number for the given hypergraph state.
    """
    # Base case: If the hypergraph has no possible moves (e.g., no vertices, edges, or faces)
    # its Grundy number is 0. This is the definition of a P-position (previous player wins).
    if not hypergraph.vertices:  # Assuming no vertices means no possible moves
        return 0

    # Collect Grundy numbers of all reachable next states
    reachable_grundy_numbers = set()

    # --- Consider all possible moves from the current hypergraph state ---
    # For Takeaway-Hypergraphs, moves involve removing a vertex.
    # When a vertex is removed, any edges or faces containing it are also removed.

    # Simulate removing each vertex one by one
    for vertex_to_remove in list(
        hypergraph.vertices
    ):  # Iterate over a copy as set changes during iteration
        next_hypergraph = hypergraph.copy()  # Create a copy to modify
        next_hypergraph.remove_vertex(
            vertex_to_remove
        )  # This method should cascade removal

        # Recursively calculate the Grundy number for the next state
        grundy_of_next_state = calculate_grundy(next_hypergraph)
        reachable_grundy_numbers.add(grundy_of_next_state)

    # Calculate the MEX of the reachable Grundy numbers
    return calculate_mex(reachable_grundy_numbers)


def build_game_tree(
    hypergraph: Hypergraph,
    max_depth: int = -1,
    current_depth: int = 0,
    _visited_states: set = None,
) -> dict:
    """
    Recursively constructs a dictionary representation of the game tree,
    including Grundy numbers for each state.

    Args:
        hypergraph: The current hypergraph state.
        max_depth: Maximum depth to build the tree (-1 for no limit).
        current_depth: Current recursion depth (for internal use).
        _visited_states: Set of visited hypergraph hashes to detect cycles
                         within the current path (for internal use, pass a copy!).

    Returns:
        A dictionary representing the current node in the game tree.
    """
    if _visited_states is None:
        _visited_states = set()

    # Create a unique, hashable representation of the current state
    current_hg_hash = hash(hypergraph)

    # 1. Depth Limit
    if max_depth != -1 and current_depth >= max_depth:
        return {
            "state": str(hypergraph),
            "grundy_number": calculate_grundy(
                hypergraph
            ),  # Still calculate Grundy even if truncated
            "children": [],
            "truncated": True,
        }

    # 2. Cycle Detection (prevents infinite recursion for cyclic games, and redundant branches)
    if current_hg_hash in _visited_states:
        return {
            "state": str(hypergraph),
            "grundy_number": calculate_grundy(
                hypergraph
            ),  # Get Grundy for the cycle state
            "children": [],
            "cycle_detected": True,
        }

    # Add current state to visited set for this path
    _visited_states.add(current_hg_hash)

    # 3. Base Case (Game End)
    if not hypergraph.vertices:  # If the hypergraph is empty
        return {"state": str(hypergraph), "grundy_number": 0, "children": []}

    # 4. Recursive Step (Normal State)
    grundy_number = calculate_grundy(hypergraph)
    children_nodes = []

    for vertex_to_remove in hypergraph.vertices:
        next_hypergraph = hypergraph.copy()
        next_hypergraph.remove_vertex(vertex_to_remove)

        # Pass a COPY of _visited_states to recursive calls for independent branches
        child_node = build_game_tree(
            next_hypergraph,
            max_depth=max_depth,
            current_depth=current_depth + 1,
            _visited_states=_visited_states.copy(),
        )
        children_nodes.append(child_node)

    # We could remove current state from visited set for path-independent checks
    # This is optional, but good practice for other types of tree traversal
    # _visited_states.remove(current_hg_hash) # Not needed here as we passed a copy

    return {
        "state": str(hypergraph),
        "grundy_number": grundy_number,
        "children": children_nodes,
    }


def print_game_tree(node: dict, indent: int = 0):
    """
    Prints a dictionary representation of a game tree to the console
    in a structured, indented format.

    Args:
        node: The dictionary representing the current node in the game tree.
        indent: The current indentation level.
    """
    prefix = "    " * indent
    state_str = node["state"]
    grundy_num = node["grundy_number"]

    status = ""
    if node.get("truncated"):
        status = " (TRUNCATED)"
    elif node.get("cycle_detected"):
        status = " (CYCLE DETECTED)"
    elif grundy_num == 0:
        status = " (P-position)"
    else:
        status = " (N-position)"

    print(f"{prefix}State: {state_str}, Grundy: {grundy_num}{status}")

    for child in node.get("children", []):
        print_game_tree(child, indent + 1)
