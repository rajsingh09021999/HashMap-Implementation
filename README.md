# HashMap-Implementation
---

#### Overview

This project involves implementing two versions of a HashMap data structure for **CS261 Data Structures**, Fall 2024. The assignment is divided into two parts:

1. **Chaining-based HashMap**: Uses a dynamic array and singly linked lists for collision resolution.
2. **Open Addressing-based HashMap**: Uses a dynamic array with quadratic probing for collision resolution.

The assignment tests your ability to create and manipulate hash tables while adhering to specific constraints and optimizing for performance.

---

#### Files Included

- **`hash_map_sc.py`**: Skeleton code for the chaining-based HashMap.
- **`hash_map_oa.py`**: Skeleton code for the open addressing HashMap.
- **`a6_include.py`**: Contains the `DynamicArray`, `LinkedList`, and utility classes.
- **README.md**: This file.

---

#### Objectives

1. Implement the following methods for both HashMap versions:
   - `put()`
   - `resize_table()`
   - `table_load()`
   - `empty_buckets()`
   - `get()`
   - `contains_key()`
   - `remove()`
   - `get_keys_and_values()`
   - `clear()`

2. Implement additional methods:
   - **Chaining-based HashMap**: `find_mode()`
   - **Open Addressing-based HashMap**: `__iter__()` and `__next__()`

3. Ensure **O(1)** average time complexity for operations in an optimized hash map.

---

#### Instructions

1. **General Rules**:
   - Use Python 3 and submit on Gradescope before the deadline.
   - Adhere to the skeleton code structure. Do not modify pre-written method signatures or variable names.
   - Avoid direct recursion unless explicitly allowed (`put()` and `resize_table()`).
   - Add meaningful docstrings and comments to your code for clarity.

2. **Restrictions**:
   - Do not use built-in Python data structures or their methods.
   - Do not access private variables or dunder methods of `DynamicArray` and `LinkedList`.

3. **Testing**:
   - Write custom test cases using Python’s `unittest` framework.
   - Test with the two provided hash functions.

4. **Performance Expectations**:
   - Ensure the `find_mode()` method has a time complexity of **O(N)**.

---

#### Usage

1. **Chaining-based HashMap**:
   - Implement chaining using singly linked lists.
   - Resize the table when the load factor reaches or exceeds **1.0**.

2. **Open Addressing-based HashMap**:
   - Use quadratic probing for collision resolution.
   - Resize the table when the load factor reaches or exceeds **0.5**.

---

#### Examples

Refer to the **assignment document** for detailed examples and expected output for each method. Test cases are provided for functions like `put()`, `get()`, and `resize_table()` to help validate your implementation.

---

#### Evaluation Criteria

1. Correctness of implementation.
2. Adherence to coding standards and provided skeleton code.
3. Passing Gradescope and custom test cases.
4. Efficiency of `find_mode()` and other key methods.

---
