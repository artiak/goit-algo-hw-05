"""
Provides HashTable realization and its API testing.
"""


class HashTable:
    """
    Provides HashTable realization.
    """

    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(self.size)]

    def hash_code(self, key) -> int:
        """
        Calculates hash code.
        """
        return hash(key) % self.size

    def put(self, key, value) -> bool:
        """
        Inserts the new Entry or replaces existent Value.
        """
        hash_code = self.hash_code(key)
        the_entry = [key, value]

        bucket: list = self.table[hash_code]

        if not bucket:
            bucket.append(the_entry)

            return True

        for entry in bucket:
            if entry[0] == key:
                entry[1] = value

                return True

        bucket.append(the_entry)

        return True

    def get(self, key) -> object:
        """
        Gets value by the key.
        """
        hash_code = self.hash_code(key)
        bucket: list = self.table[hash_code]

        if not bucket:
            return None

        for entry in bucket:
            if entry[0] == key:
                return entry[1]

        return None

    def delete(self, key) -> object:
        """
        Removes Entry by given Key.
        """
        hash_code = self.hash_code(key)
        bucket: list = self.table[hash_code]

        if not bucket:
            return None

        for entry in bucket:
            if entry[0] == key:
                bucket.remove(entry)

                return entry[1]

        return None


if __name__ == "__main__":
    # GIVEN:
    APPLE = "apple"
    ORANGE = "orange"
    BANANA = "banana"

    # WHEN:
    table = HashTable(5)
    table.put(APPLE, 10)
    table.put(ORANGE, 20)
    table.put(BANANA, 30)

    # THEN:
    assert table.get(APPLE) == 10
    assert table.get(ORANGE) == 20
    assert table.get(BANANA) == 30

    # AND:
    assert table.delete(ORANGE) == 20
    assert not table.get(ORANGE)
