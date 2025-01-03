# Name: Rajveer Singh
# OSU Email: singrajv@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: December 5, 2024,
# Description: In this assignment, I will be completing a HashMap class by implementing methods
#              such as put(), resize_table(), table_load(), get(), and others while maintaining
#              an average-case performance of O(1) for all operations. To handle collisions,
#              I will use chaining, where key-value pairs are stored in nodes of a singly linked list.
#              The hash table itself will be stored in a DynamicArray.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        Updates or creates  key-value pair in the hash map depending on if key already exists.
        Resizes the hash table if the load factor is greater than or equal to 1.0.
        """

        # we need to check if hash table needs to resize
        if self.table_load() >= 1.0:
            self.resize_table(self.get_capacity() * 2)

        # We use the hash function to generate a hash value for the key,
        # then use the modulus operator with the table capacity
        # to make sure the index falls within the valid range of buckets.
        # All so we can retrieve a linked list at the computed index.
        linked_list = self._buckets[self._hash_function(key) % self.get_capacity()]

        # We use the contains() method of the LinkedList to check if the key already exists in the bucket
        if linked_list.contains(key):
            linked_list.contains(key).value = value  # If the key is found, we update its value
        else:  # Otherwise we insert a new node into the bucket and increase the size of the hash map
            linked_list.insert(key, value)
            self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the hash table to the specified new capacity.
        Rehashes all existing key-value pairs into the new table.
        If new_capacity < 1, does nothing.
        Ensures the new capacity is a prime number.
        """
        if new_capacity < 1:
            return

        # We make sure the new hash table capacity is the smallest prime number
        # that’s at least as large as the specified capacity
        new_capacity = self._next_prime(new_capacity)

        # We create a new DynamicArray to hold the resized table
        new_buckets = DynamicArray()
        i = 0
        while i < new_capacity:
            # Add an empty LinkedList for each bucket in the new table
            new_buckets.append(LinkedList())
            i += 1

        # Rehash all existing key-value pairs from the old table into the new table.
        i = 0
        while i < self.get_capacity():
            for node in self._buckets.get_at_index(i):
                # Recompute the new index for each key using the updated capacity.
                new_index = self._hash_function(node.key) % new_capacity
                new_buckets.get_at_index(new_index).insert(node.key, node.value)
            i += 1

        # Finally, we replace the old table with the new table
        self._buckets = new_buckets
        self._capacity = new_capacity

    def table_load(self) -> float:
        """
        Calculates and returns the load factor of the hash table.
        """
        return self.get_size() / self.get_capacity()  # load factor is size / capacity

    def empty_buckets(self) -> int:
        """
        Calculates and returns the number of empty LinkedLists in the hash table.
        """
        # We start track of how many buckets have no elements
        empty_buckets_count = 0
        index = 0

        # Go through each bucket in the hash table
        while index < self.get_capacity():
            # We ger the linked list at the current index
            current_bucket = self._buckets.get_at_index(index)
            # If this linked list has no elements, we increase the counter
            if current_bucket.length() == 0:
                empty_buckets_count += 1
            index += 1  # Move to the next bucket

        return empty_buckets_count

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key.
        If the key is not in the hash map, returns None.
        """
        # First, we calculate the index where the key should be located
        index = self._hash_function(key) % self.get_capacity()

        # We get the LinkedList at the computed index
        current_bucket = self._buckets.get_at_index(index)

        # Search the bucket for the key using its contains method
        if current_bucket.contains(key):
            # If we found the key, return its associated value
            return current_bucket.contains(key).value

        # If we didn't find the key, return None
        return None

    def contains_key(self, key: str) -> bool:
        """
        Checks if the given key exists in the hash map.
        Returns True if the key is found, otherwise False.
        """

        index = self._hash_function(key) % self.get_capacity()
        current_bucket = self._buckets.get_at_index(index)

        # Use the LinkedList's contains method to see if the key exists
        if current_bucket.contains(key):
            # If the key is found, we return True
            return True

        return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map.
        If the key is not in the hash map, does nothing.
        """

        index = self._hash_function(key) % self.get_capacity()
        current_bucket = self._buckets.get_at_index(index)

        # We remove the key from the bucket using the remove method of the LinkedList
        if current_bucket.remove(key):
            # after removing we decrease the size of the hash map
            self._size -= 1

        # If the key wasn't found, we just do nothing

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array containing all key-value pairs stored in the hash map.
        Each index of the array contains a tuple (key, value).
        """
        # We need to make a new dynamic array to store the key-value pairs
        key_value_pairs = DynamicArray()

        # We start with the first bucket and work our way through
        index = 0
        while index < self.get_capacity():
            # Get the bucket (a LinkedList) at the current index
            current_bucket = self._buckets.get_at_index(index)

            # Now, we loop through each node in the bucket
            for node in current_bucket:
                # And add the key and value as a tuple to our result array
                key_value_pairs.append((node.key, node.value))

            index += 1

        # Once we've gone through all the buckets, we return the array of pairs
        return key_value_pairs

    def clear(self) -> None:
        """
        Clears the contents of the hash map without changing the underlying hash table capacity.
        """
        # We need to reset the size to zero
        self._size = 0
        index = 0
        # We loop through each bucket
        while index < self.get_capacity():
            # And replace the linked list at the current index with a new empty LinkedList
            self._buckets.set_at_index(index, LinkedList())
            index += 1


def find_mode(arr: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Takes a DynamicArray and finds the mode along with their frequency.
    Returns a tuple containing a DynamicArray of the mode and the highest frequency count.
    """
    # We will use this HashMap to keep track of the frequency of each value
    frequency_tracker = HashMap()
    # We will keep track of the highest frequency we've encountered so far
    highest_frequency = 0

    index = 0
    # First pass: Build the frequency map and determine the highest frequency
    while index < arr.length():
        current_value = arr.get_at_index(index)
        # Get the current frequency of the value from the frequency tracker
        freq = frequency_tracker.get(current_value)
        if freq is None:
            # If it's the first time we've seen this value, we initialize its frequency to 1
            frequency_tracker.put(current_value, 1)
            freq = 1
        else:
            # If we've seen this value before, we increment its frequency
            freq += 1
            frequency_tracker.put(current_value, freq)

        # Update highest_frequency if the current frequency exceeds it
        if freq > highest_frequency:
            highest_frequency = freq
        # We don't need to collect modes in this pass
        index += 1

    # Second pass: Collect all values that have the highest frequency
    modes = DynamicArray()  # This will hold our modes
    key_value_pairs = frequency_tracker.get_keys_and_values()
    index = 0
    while index < key_value_pairs.length():
        key, value = key_value_pairs.get_at_index(index)
        if value == highest_frequency:
            # If the value's frequency matches the highest, we add it to modes
            modes.append(key)
        index += 1

    return modes, highest_frequency


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
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

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
    m = HashMap(53, hash_function_1)
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

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
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

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
