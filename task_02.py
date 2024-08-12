"""
Provides binary search realization and testing.
"""


def binary_search(q: float, lst: list) -> tuple:
    """
    Searches for float in source list.
    """
    left_idx: int = 0
    right_idx: int = len(lst) - 1

    iter_count: int = 0

    while left_idx <= right_idx:
        iter_count += 1

        mid_idx: int = (left_idx + right_idx) // 2
        mid_val: float = lst[mid_idx]

        if q < mid_val:
            right_idx = mid_idx - 1
            continue

        if q > mid_val:
            left_idx = mid_idx + 1
            continue

        ceil_idx = mid_idx + 1

        if ceil_idx > len(lst) - 1:
            ceil_idx = - 1

        return (iter_count, lst[ceil_idx])

    return (iter_count, None)


### TESTING ###


SRC: list = [1.1, 2.2, 3.3, 4.4, 5.5]


def _should_handle_miss() -> None:
    # WHEN:
    res: tuple = binary_search(3.2, SRC)

    # THEN:
    assert len(res) == 2
    assert res[0] == 3
    assert res[1] is None


def _should_find_middle() -> None:
    # WHEN:
    res: tuple = binary_search(3.3, SRC)

    # THEN:
    assert len(res) == 2
    assert res[0] == 1
    assert res[1] == 4.4


def _should_find_last() -> None:
    # WHEN:
    res: tuple = binary_search(5.5, SRC)

    # THEN:
    assert len(res) == 2
    assert res[0] == 3
    assert res[1] == 5.5


if __name__ == "__main__":
    _should_handle_miss()
    _should_find_middle()
    _should_find_last()
