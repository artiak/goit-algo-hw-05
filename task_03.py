"""
Compares time complexity of Knuth-Morris-Pratt,
Boyer-Moore, and Rabin-Karp searching algorithms.

Example of relusts for bigger article_2.txt:
Knuth-Morris-Pratt (present) search for '18398' chars takes '13' ms
Knuth-Morris-Pratt (absent) search for '18398' chars takes '11' ms
Boyer-Moore (present) search for '18398' chars takes '4' ms
Boyer-Moore (absent) search for '18398' chars takes '5' ms
Rabin-Karp (present) search for '18398' chars takes '33' ms
Rabin-Karp (absent) search for '18398' chars takes '32' ms

Boyer-Moore is the most effective searching algorithm for borth
present and absent search results.
"""
import timeit


def _lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps


def _kmp_search(text: str, pattern: str) -> int:
    q_len = len(pattern)
    src_len = len(text)

    lps = _lps(pattern)

    i = j = 0

    while i < src_len:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == q_len:
            return i - j

    return -1


def _shift_table(pattern):
    table = {}
    length = len(pattern)

    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1

    table.setdefault(pattern[-1], length)

    return table


def _bm_search(text, pattern):
    shift_table = _shift_table(pattern)
    i = 0

    while i <= len(text) - len(pattern):
        j = len(pattern) - 1

        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1

        if j < 0:
            return i

        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    return -1


def _poly_hash(s, base=256, modulus=101):
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value


def _rk_search(text, pattern):
    text_len = len(text)
    pattern_len = len(pattern)

    base = 256
    modulus = 101

    substring_hash = _poly_hash(pattern, base, modulus)
    current_slice_hash = _poly_hash(
        text[:pattern_len], base, modulus)

    h_multiplier = pow(base, pattern_len - 1) % modulus

    for i in range(text_len - pattern_len + 1):
        if substring_hash == current_slice_hash:
            if text[i:i+pattern_len] == pattern:
                return i

        if i < text_len - pattern_len:
            current_slice_hash = (current_slice_hash -
                                  ord(text[i]) * h_multiplier) % modulus
            current_slice_hash = (
                current_slice_hash * base + ord(text[i + pattern_len])) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus

    return -1


### TESTING ###


def _read(path):
    with open(path, encoding="utf-8") as file:
        return file.read()


def _measure(name: str, src: str, q: str, func: callable) -> None:
    seconds = timeit.timeit(lambda: func(src, q), number=10)
    millis = int(seconds * 1000)
    print(f"{name} search for '{len(src)}' chars takes '{millis}' ms")


ARTICLE_1_NAME: str = "article_1.txt"
ARTICLE_2_NAME: str = "article_2.txt"

KMP_NAME: str = "Knuth-Morris-Pratt"
BM_NAME: str = "Boyer-Moore"
RK_NAME: str = "Rabin-Karp"

PRESENT_SUFFIX: str = " (present)"
ABSENT_SUFFIX: str = " (absent)"

DISTANCE_PATTERN: str = "Distance"
SUPPRESSED_PATTERN: str = "suppressed"


def _measure_knuth_morris_pratt_search():
    _measure(KMP_NAME + PRESENT_SUFFIX, _read(ARTICLE_1_NAME),
             DISTANCE_PATTERN, _kmp_search)
    _measure(KMP_NAME + PRESENT_SUFFIX, _read(ARTICLE_2_NAME),
             SUPPRESSED_PATTERN, _kmp_search)

    _measure(KMP_NAME + ABSENT_SUFFIX, _read(ARTICLE_1_NAME),
             SUPPRESSED_PATTERN, _kmp_search)
    _measure(KMP_NAME + ABSENT_SUFFIX, _read(ARTICLE_2_NAME),
             DISTANCE_PATTERN, _kmp_search)


def _measure_boyer_moore_search():
    _measure(BM_NAME + PRESENT_SUFFIX, _read(ARTICLE_1_NAME),
             DISTANCE_PATTERN, _bm_search)
    _measure(BM_NAME + PRESENT_SUFFIX, _read(ARTICLE_2_NAME),
             SUPPRESSED_PATTERN, _bm_search)

    _measure(BM_NAME + ABSENT_SUFFIX, _read(ARTICLE_1_NAME),
             SUPPRESSED_PATTERN, _bm_search)
    _measure(BM_NAME + ABSENT_SUFFIX, _read(ARTICLE_2_NAME),
             DISTANCE_PATTERN, _bm_search)


def _measure_rabin_karp_search():
    _measure(RK_NAME + PRESENT_SUFFIX, _read(ARTICLE_1_NAME),
             DISTANCE_PATTERN, _rk_search)
    _measure(RK_NAME + PRESENT_SUFFIX, _read(ARTICLE_2_NAME),
             SUPPRESSED_PATTERN, _rk_search)

    _measure(RK_NAME + ABSENT_SUFFIX, _read(ARTICLE_1_NAME),
             SUPPRESSED_PATTERN, _rk_search)
    _measure(RK_NAME + ABSENT_SUFFIX, _read(ARTICLE_2_NAME),
             DISTANCE_PATTERN, _rk_search)


if __name__ == "__main__":
    _measure_knuth_morris_pratt_search()
    _measure_boyer_moore_search()
    _measure_rabin_karp_search()
