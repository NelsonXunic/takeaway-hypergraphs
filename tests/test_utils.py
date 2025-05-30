from src.core.utils import calculate_mex


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
