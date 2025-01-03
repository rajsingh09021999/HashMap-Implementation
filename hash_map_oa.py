# Name: Rajveer Singh
# OSU Email: singrajv@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: December 5, 2024,
# Description: In this assignment, I will complete a version of the HashMap class that uses
#              open addressing with quadratic probing for collision resolution where the
#              key-value pairs will be stored directly in a DynamicArray. I will do this by
#              implementing methods such as put(), resize_table(), table_load(), get(), and others,
#              along with iterator methods __iter__() and __next__().

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates or inserts a key/value pair into the hash map.
        If the key is already in the hash map, replace its value.
        If the key is not in the hash map, add a new entry.
        """

        # If adding a new key would cause the load factor to be >= 0.5,
        # we must first resize the table to double its current capacity.
        if self.table_load() >= 0.5:
            self.resize_table(self.get_capacity() * 2)

        # Compute the initial index using the hash function
        index = self._hash_function(key) % self.get_capacity()
        first_tombstone_index = -1

        probe = 0
        # Attempt to find a slot or the key itself, up to 'capacity' attempts
        while probe < self.get_capacity():
            current_index = (index + probe * probe) % self.get_capacity()
            entry = self._buckets.get_at_index(current_index)

            if entry is None:
                # Found an empty slot; if we found a tombstone earlier, reuse it
                if first_tombstone_index != -1:
                    self._buckets.set_at_index(first_tombstone_index, HashEntry(key, value))
                else:
                    self._buckets.set_at_index(current_index, HashEntry(key, value))
                self._size += 1
                return

            elif entry.is_tombstone:
                # Record the first tombstone we encounter, if we haven't already
                if first_tombstone_index == -1:
                    first_tombstone_index = current_index
                # Keep searching in case the key is further down

            elif entry.key == key:
                # Key found; update its value
                entry.value = value
                return

            # Move on to the next quadratic probe
            probe += 1

        # Under normal conditions (with proper resizing) we should never exhaust all probes.
        # If we do, it indicates the table is overly full or there's a logic error.

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the underlying table. All active key/value pairs
        must be put into the new table, meaning all non-tombstone hash table links
        must be rehashed.
        """

        # If new_capacity is less than the current number of elements in the hash map, we do nothing.
        if new_capacity < self.get_size():
            return

        # Otherwise, we find the next prime number greater than or equal to new_capacity and
        # use that as the new capacity.
        new_capacity = self._next_prime(new_capacity)

        # Save the old buckets and capacity for later
        old_buckets = self._buckets
        old_capacity = self.get_capacity()

        # Create a new DynamicArray with the updated capacity
        self._buckets = DynamicArray()
        count = 0
        while count < new_capacity:
            self._buckets.append(None)
            count += 1

        # Update our capacity and reset the size
        self._capacity = new_capacity
        self._size = 0

        # Rehash all non-tombstone entries
        index = 0
        while index < old_capacity:
            entry = old_buckets.get_at_index(index)
            if entry is not None and not entry.is_tombstone:
                # We re-insert all non-tombstone entries from the old table into the new table by calling `put()`.
                self.put(entry.key, entry.value)
            index += 1

    def table_load(self) -> float:
        """
        Returns the current load factor of the hash table,
        """
        return self.get_size() / self.get_capacity()  # load factor is size / capacity

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.
        """
        empty_count = 0
        index = 0
        # Iterate through all buckets using a while loop
        while index < self.get_capacity():
            # In open addressing, an empty bucket is one that is None.
            # Buckets with tombstones are not empty because they still
            # contain a HashEntry object (just marked as deleted).
            if self._buckets.get_at_index(index) is None:
                empty_count += 1
            index += 1
        return empty_count

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key.
        If the key is not in the hash map, returns None.
        """
        # We hash the key and reduce it modulo self._capacity to get a starting index
        index = self._hash_function(key) % self._capacity
        probe = 0

        while probe < self._capacity:
            # We use (index + probe*probe) % self._capacity to find the next index
            # if the current one is occupied by a non-matching key or is a tombstone
            current_index = (index + probe * probe) % self._capacity
            entry = self._buckets.get_at_index(current_index)

            if entry is None:
                # This indicates that empty bucket is found
                # since we encountered no matching key by now,
                # the key is not in the table.
                return None
            elif not entry.is_tombstone and entry.key == key:
                # If we find a matching key that is not a tombstone, we return its value.
                return entry.value

            # The variable probe increments by 1 each time we fail to find the key
            probe += 1

        # If we've probed all slots without finding the key, then we return None
        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map, otherwise returns False.
        """
        # If get() returns a non-None value, the key is present.
        # If get() returns None, the key does not exist in the map.
        return self.get(key) is not None

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map.
        If the key is not in the hash map, this method does nothing.
        """
        index = self._hash_function(key) % self.get_capacity()
        probe = 0

        # We use quadratic probing to search key
        while probe < self.get_capacity():
            current_index = (index + probe * probe) % self.get_capacity()
            entry = self._buckets.get_at_index(current_index)

            # When we encounter an empty bucket, we simply return nothing
            if entry is None:
                return

            # If we find an active entry with the matching key
            if not entry.is_tombstone and entry.key == key:
                # we effectively remove the key without breaking the probing sequence for other keys
                # that might be further down the line
                entry.is_tombstone = True
                self._size -= 1
                return

            probe += 1

        # Simply return if the key doesn't exist in the table
        return

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple (key, value)
        for each active key/value pair stored in the hash map.
        """
        new_dynamic_array = DynamicArray()
        index = 0

        # We loop through all buckets in the hash table
        while index < self.get_capacity():
            entry = self._buckets.get_at_index(index)
            # Only append if we have an active (non-tombstone) entry
            if entry is not None and not entry.is_tombstone:
                new_dynamic_array.append((entry.key, entry.value))
            index += 1

        return new_dynamic_array

    def clear(self) -> None:
        """
        Clears the contents of the hash map without changing the underlying capacity.
        """
        # Set every bucket back to None
        index = 0
        while index < self.get_capacity():
            self._buckets.set_at_index(index, None)
            index += 1

        # Reset the size since we now have no active entries
        self._size = 0

    def __iter__(self):
        """
        Returns the iterator for the hash map.
        """
        self._index = 0 # We set an internal index to 0 which advances after each call to __next_
        return self

    def __next__(self):
        """
        Returns the next non-tombstone HashEntry in the hash map.
        """
        # The iteration process starts when __iter__() which has self._index = 0
        while self._index < self.get_capacity():
            entry = self._buckets.get_at_index(self._index)
            self._index += 1  # we continue to increment self._index and look at the following bucket
            # We check if the entry is an active entry (bucket is not None and does not contain a tombstone)
            if entry is not None and not entry.is_tombstone:
                # Return the active entry
                return entry

        # Once we’ve checked all buckets in the hash map without finding any more active entries,
        # StopIteration is raised.
        raise StopIteration


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
