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
