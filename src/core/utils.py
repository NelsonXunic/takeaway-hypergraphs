from functools import lru_cache
from hypergraph import Hypergraph


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
