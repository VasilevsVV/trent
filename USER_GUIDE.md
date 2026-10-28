# trent — User Guide

Convenient sequence/iterable/collection processing for Python, inspired by Clojure mapping and threading macros.

**Requires Python 3.13+**

---

## Table of Contents

1. [Installation](#installation)
2. [Getting Started](#getting-started)
3. [Core Concepts](#core-concepts)
4. [Mapping & Transforming](#mapping--transforming)
5. [Filtering](#filtering)
6. [Concatenation & Flattening](#concatenation--flattening)
7. [Partitioning](#partitioning)
8. [Grouping](#grouping)
9. [Paired Collections](#paired-collections)
10. [Parallel & Async Operations](#parallel--async-operations)
11. [Element Access](#element-access)
12. [Reduction & Collection](#reduction--collection)
13. [In-Place Mutation](#in-place-mutation)
14. [Utility Functions](#utility-functions)
15. [Exceptions](#exceptions)

---

## Installation

```bash
pip install trent
```

---

## Getting Started

Import the library and create a collection:

```python
from trent import seq, cmap, cfilter, first, first_

# Create a collection from any iterable
numbers = seq([1, 2, 3, 4, 5])

# Map: transform each element
doubled = cmap(lambda x: x * 2, numbers)
print(doubled.to_list())  # [2, 4, 6, 8, 10]

# Filter: keep elements matching a predicate
evens = cfilter(lambda x: x % 2 == 0, numbers)
print(evens.to_list())  # [2, 4]

# Get the first element
print(first(numbers))  # 1
print(first_(numbers))  # 1 (raises if empty)
```

---

## Core Concepts

### Collection vs PairedCollection

`trent` provides two main collection types:

- **`Collection[T]`** — a lazy, typed sequence of elements of type `T`
- **`PairedCollection[T1, T2]`** — a sequence of key-value tuples `(T1, T2)`, useful for grouped data

```python
from trent import seq, pairmap

# Regular collection
words = seq(["apple", "banana", "cherry"])

# Paired collection: map elements to (key, value) pairs
lengths = words.map_to_pair(len)  # [(5, 'apple'), (6, 'banana'), (6, 'cherry')]
print(lengths.to_list())

# Convert back to a dict
word_lengths = lengths.to_dict()
print(word_lengths)  # {5: 'apple', 6: 'banana'}
```

### Laziness

Collections are **lazy** by default — operations chain without evaluating until you materialise:

```python
from trent import seq

numbers = seq(range(10))
squared = numbers.map(lambda x: x ** 2)  # Not evaluated yet
print(squared.to_list())  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```

Use `.persist()` to force materialisation so the collection can be iterated multiple times.

---

## Mapping & Transforming

### `cmap` — Lazy Map

```python
from trent import seq, cmap

words = seq(["hello", "world", "python"])
upper = cmap(str.upper, words)
print(upper.to_list())  # ['HELLO', 'WORLD', 'PYTHON']
```

### `apply` — Side-Effect Map

Apply a function to each element without transforming the values. Useful for logging, updating, or calling methods.

```python
from trent import seq

logs = seq([
    {"level": "ERROR", "msg": "Connection failed"},
    {"level": "INFO", "msg": "User logged in"},
])

# Log each entry without changing the data
logs.apply(lambda log: print(f"[{log['level']}]: {log['msg']}"))
```

### `mapcat` — Map Then Flatten

```python
from trent import seq, mapcat

words = seq(["apple", "banana", "cherry"])
letters = mapcat(lambda w: list(w), words)
print(letters.to_list())  # ['a', 'p', 'p', 'l', 'e', 'b', 'a', 'n', 'a', 'n', 'a', 'c', 'h', 'e', 'r', 'r', 'y']
```

### `pairmap` — Map Over Pairs

```python
from trent import seq, pairmap

pairs = seq([(1, "apple"), (2, "banana"), (3, "cherry")])
result = pairmap(lambda k, v: f"{k}:{v.upper()}", pairs)
print(result.to_list())  # ['1:APPLE', '2:BANANA', '3:CHERRY']
```

---

## Filtering

### `cfilter` — Filter by Predicate

```python
from trent import seq, cfilter

numbers = seq(range(1, 11))
odds = cfilter(lambda x: x % 2 != 0, numbers)
print(odds.to_list())  # [1, 3, 5, 7, 9]
```

### `remove` — Negated Filter

```python
from trent import seq, cfilter

words = seq(["apple", "banana", "cherry", "kiwi"])
short = cfilter(lambda w: len(w) < 5, words)
print(short.to_list())  # ['kiwi']
```

### `remove_none` — Remove `None` Values

```python
from trent import seq, cfilter

values = seq([1, None, 3, None, 5])
clean = values.remove_none()
print(clean.to_list())  # [1, 3, 5]
```

### `distinct` / `distinct_by` — Deduplicate

```python
from trent import seq

words = seq(["apple", "banana", "apple", "cherry", "banana"])
unique = words.distinct()
print(unique.to_list())  # ['apple', 'banana', 'cherry']

# Distinct by a key
records = seq([
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
    {"id": 1, "name": "Alice (dup)"},
])
deduped = records.distinct_by(lambda r: r["id"])
print(deduped.to_list())  # [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}]
```

---

## Concatenation & Flattening

### `cat` — Flatten Nested Iterables

```python
from trent import seq, cat

nested = seq([[1, 2], [3, 4], [5, 6]])
flat = cat(nested)
print(flat.to_list())  # [1, 2, 3, 4, 5, 6]
```

### `mapcat` — Map and Flatten

```python
from trent import seq, mapcat

words = seq(["hello", "world"])
# Map each word to its characters, then flatten
chars = mapcat(lambda w: list(w), words)
print(chars.to_list())  # ['h', 'e', 'l', 'l', 'o', 'w', 'o', 'r', 'l', 'd']
```

### `catmap` — Flatten Then Map

```python
from trent import seq, catmap

nested = seq([[1, 2], [3, 4], [5, 6]])
result = catmap(lambda x: x * 10, nested)
print(result.to_list())  # [10, 20, 30, 40, 50, 60]
```

---

## Partitioning

### `partition` — Fixed-Size Chunks

```python
from trent import seq

numbers = seq(range(10))
chunks = numbers.partition(3)
print(chunks.to_list())  # [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
```

### `partition_by` — Split on Predicate Change

```python
from trent import seq

numbers = seq([1, 2, 3, 4, 5, 6, 7, 8, 9])
# Split whenever we hit an even number
chunks = numbers.partition_by(lambda n: n % 2 == 0)
print(chunks.to_list())
# [[1, 2], [3, 4], [5, 6], [7, 8], [9]]
```

### `partmap` — Map Over Partitions

```python
from trent import seq

numbers = seq(range(10))
# Partition into chunks of 3, then sum each chunk
sums = numbers.partition(3).partmap(sum)
print(sums.to_list())  # [3, 12, 21, 9]
```

---

## Grouping

### `group_by` — Group Elements by Key

```python
from trent import seq

# Group words by length
words = seq(["apple", "banana", "kiwi", "cherry", "date"])
grouped = words.group_by(len)
print(grouped.to_list())
# [(5, ['apple']), (6, ['banana', 'cherry']), (4, ['kiwi', 'date'])]

# Group with custom value function
logs = seq([
    {"env": "prod", "msg": "Error A"},
    {"env": "test", "msg": "Debug B"},
    {"env": "prod", "msg": "Error C"},
])
grouped_logs = logs.group_by(lambda x: x["env"], val_fn=lambda x: x["msg"])
print(grouped_logs.to_list())
# [('prod', ['Error A', 'Error C']), ('test', ['Debug B'])]
```

### `groupmap` — Ungroup (Reverse of Grouping)

```python
from trent import seq

pairs = seq([(1, 'a'), (1, 'b'), (2, 'c')])
# Expand grouped pairs back into individual elements
flattened = pairs.groupmap()
print(flattened.to_list())  # [(1, 'a'), (1, 'b'), (2, 'c')]
```

---

## Paired Collections

### Creating Paired Collections

```python
from trent import seq, map_to_pair

words = seq(["apple", "banana", "cherry"])
# Map to (length, word) pairs
lengths = map_to_pair(words, len)
print(lengths.to_list())  # [(5, 'apple'), (6, 'banana'), (6, 'cherry')]

# With both key and value functions
indexed = map_to_pair(words, lambda w: f"id_{w}", lambda w: len(w))
print(indexed.to_list())  # [('id_apple', 5), ('id_banana', 6), ('id_cherry', 6)]
```

### `to_dict` — Convert to Dictionary

```python
from trent import seq, map_to_pair

words = seq(["apple", "banana", "cherry"])
lengths = map_to_pair(words, len).to_dict()
print(lengths)  # {5: 'apple', 6: 'banana'}
```

### `pairmap` on PairedCollections

```python
from trent import seq, map_to_pair, pairmap

words = seq(["apple", "banana", "cherry"])
pairs = map_to_pair(words, len)

# Transform both elements of each pair
result = pairmap(lambda k, v: f"{v.upper()} ({k})", pairs)
print(result.to_list())  # ['APPLE (5)', 'BANANA (6)', 'CHERRY (6)']
```

### `as_spans` — Adjacent Pairs (Sliding Window)

```python
from trent import seq

numbers = seq([1, 2, 3, 4, 5])
spans = numbers.as_spans()
print(spans.to_list())  # [(1, 2), (2, 3), (3, 4), (4, 5)]

# Useful for comparing adjacent elements
diffs = numbers.as_spans().pairmap(lambda a, b: b - a)
print(diffs.to_list())  # [(1, 1), (1, 1), (1, 1), (1, 1)]
```

---

## Parallel & Async Operations

### `pmap` — Parallel Map (CPU-Bound)

Uses `multiprocessing.Pool` for CPU-intensive tasks:

```python
from trent import seq, pmap

def expensive_computation(n):
    return sum(i * i for i in range(n))

numbers = seq(range(20))
results = pmap(expensive_computation, numbers)
print(results.to_list())
```

### `pmap_` — Parallel Map with Thread Control

```python
from trent import seq, pmap_

numbers = seq(range(20))
results = pmap_(expensive_computation, numbers, threads=4)
```

### `.async_map` — Async Map (I/O-Bound)

Uses a global thread pool for I/O-bound tasks (network calls, file I/O, etc.):

```python
import asyncio
from trent import seq

async def fetch_data(url):
    # Simulate network call
    await asyncio.sleep(0.1)
    return f"data_from_{url}"

urls = seq(["http://api.example.com/a", "http://api.example.com/b"])
results = urls.async_map(fetch_data)
print(results.to_list())
```

### `.async_map_` — Async Map with Thread Control

```python
from trent import seq

urls = seq(["http://api.example.com/a", "http://api.example.com/b"])
results = urls.async_map_(fetch_data, threads=8)
```

### `async_foreach` — Concurrent Side Effects

```python
from trent import seq
import asyncio

urls = seq(["http://api1.com", "http://api2.com", "http://api3.com"])

async def download(url):
    # Simulate download
    await asyncio.sleep(0.1)
    print(f"Downloaded: {url}")

urls.async_foreach(download, threads=4)
```

---

## Element Access

### `first`, `second`, `third` — Safe Access

Return `None` if the element doesn't exist:

```python
from trent import first, second, third

numbers = seq([10, 20, 30, 40])
print(first(numbers))   # 10
print(second(numbers))  # 20
print(third(numbers))   # 30
print(second(seq([])))  # None
```

### `first_`, `second_`, `nth_` — Strict Access

Raise `MissingValueException` if the element doesn't exist:

```python
from trent import first_, second_, nth_

numbers = seq([10, 20, 30])
print(first_(numbers))   # 10
print(second_(numbers))  # 20
print(nth_(numbers, 2))  # 30

# Raises MissingValueException:
# first_(seq([]))
```

---

## Reduction & Collection

### `.reduce` — Fold / Accumulate

```python
from trent import seq

numbers = seq([1, 2, 3, 4, 5])

# Sum
total = numbers.reduce(lambda acc, x: acc + x)
print(total)  # 15

# With initial value
product = numbers.reduce(lambda acc, x: acc * x, initial=1)
print(product)  # 120

# Custom accumulator
words = seq(["hello", "world", "python"])
concat = words.reduce(lambda acc, w: f"{acc} {w}")
print(concat)  # 'hello world python'
```

### `to_list`, `to_set` — Materialise

```python
from trent import seq

numbers = seq(range(5))
lst = numbers.to_list()
print(lst)  # [0, 1, 2, 3, 4]

s = numbers.to_set()
print(s)  # {0, 1, 2, 3, 4}
```

### `.collect` — Materialise and Transform

```python
from trent import seq

numbers = seq([1, 2, 3, 4, 5])
result = numbers.collect(lambda lst: sum(lst) / len(lst))
print(result)  # 3.0 (average)
```

---

## In-Place Mutation

### `extend_`, `append_`, `cons_` — Mutate the Collection

```python
from trent import seq

numbers = seq([1, 2, 3])

# Extend with another iterable
numbers.extend_([4, 5])
print(numbers.to_list())  # [1, 2, 3, 4, 5]

# Append a single value
numbers.append_(6)
print(numbers.to_list())  # [1, 2, 3, 4, 5, 6]

# Prepend a single value
numbers.cons_(0)
print(numbers.to_list())  # [0, 1, 2, 3, 4, 5, 6]
```

### `concat`, `conj`, `cons` — New Collection with Added Elements

```python
from trent import seq

numbers = seq([1, 2, 3])

# New collection with appended elements
extended = numbers.concat([4, 5])
print(extended.to_list())  # [1, 2, 3, 4, 5]

# Join single values
joined = numbers.conj(4, 5, 6)
print(joined.to_list())  # [1, 2, 3, 4, 5, 6]

# Prepend
prepended = numbers.cons(0)
print(prepended.to_list())  # [0, 1, 2, 3]
```

### `__add__` — Concatenation with `+`

```python
from trent import seq

a = seq([1, 2, 3])
b = a + [4, 5]
print(b.to_list())  # [1, 2, 3, 4, 5]
```

---

## Utility Functions

### `identity` — Return the Same Value

```python
from trent import identity

# Useful as a default function
numbers = seq([1, 2, 3])
result = numbers.map(identity)
print(result.to_list())  # [1, 2, 3]
```

### `getter` / `gtr` — Extract Dict Keys

```python
from trent import seq, cmap, getter, gtr

users = seq([
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25},
])

# Get all names
names = cmap(getter("name"), users)
print(names.to_list())  # ['Alice', 'Bob']

# With default value
ages = cmap(gtr("age", 0), users)
print(ages.to_list())  # [30, 25]
```

### `gtr_` — Strict Dict Key Getter

```python
from trent import seq, cmap, gtr_

users = seq([
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": None},
])

# Strict getter — raises Exception if key is absent
age_getter = gtr_("age", int)
names = cmap(lambda u: f"{u['name']}: {age_getter(u)}", users)
print(names.to_list())  # ['Alice: 30', 'Bob: None']

# Raises Exception: "Missing value by key: missing_key, from map: {'name': 'Bob', 'age': None}"
# gtr_("missing_key", int)({"name": "Bob"})
```

### `isnone` — Check for `None`

```python
from trent import seq, isnone

values = seq([1, None, 3, None, 5])
clean = values.remove(isnone)
print(clean.to_list())  # [1, 3, 5]
```

---

## Take & Slice

### `.take` — First N Elements

```python
from trent import seq

numbers = seq(range(10))
first_five = numbers.take(5)
print(first_five.to_list())  # [0, 1, 2, 3, 4]
```

### `.takewhile` — While Predicate Holds

```python
from trent import seq

numbers = seq(range(10))
# Take while numbers are less than 5
small = numbers.takewhile(lambda x: x < 5)
print(small.to_list())  # [0, 1, 2, 3, 4]
```

### `head` / `tail` — First Element / Rest

```python
from trent import seq

numbers = seq([1, 2, 3, 4, 5])

# Get the first element (non-destructive)
print(numbers.head)  # 1

# Get all elements except the first
rest = numbers.tail()
print(rest.to_list())  # [2, 3, 4, 5]
```

---

## Exceptions

### `EmptyCollectionException`

Raised when accessing elements of an empty collection:

```python
from trent import seq, first_, EmptyCollectionException

try:
    first_(seq([]))
except EmptyCollectionException as e:
    print(e)  # "Collection is empty! Can't take head of empty collection"
```

### `MissingValueException`

Raised when accessing an element that doesn't exist:

```python
from trent import seq, first_, MissingValueException

try:
    first_(seq([]))
except MissingValueException as e:
    print(e)  # "Missing first for value: []"
```

---

## Real-World Examples

### Example 1: Processing API Responses

```python
from trent import seq, cmap, cfilter, first

responses = seq([
    {"status": 200, "data": "success"},
    {"status": 500, "data": "error"},
    {"status": 200, "data": "ok"},
    {"status": 404, "data": "not found"},
])

# Get all successful responses
success = cfilter(lambda r: r["status"] == 200, responses)
messages = cmap(lambda r: r["data"], success)
print(messages.to_list())  # ['success', 'ok']

# Get the first successful response
first_success = first(cfilter(lambda r: r["status"] == 200, responses))
print(first_success["data"])  # 'success'
```

### Example 2: Log Analysis

```python
from trent import seq, cfilter, cmap

logs = seq([
    {"level": "ERROR", "service": "auth", "msg": "Login failed"},
    {"level": "INFO", "service": "auth", "msg": "Login success"},
    {"level": "ERROR", "service": "api", "msg": "Timeout"},
    {"level": "ERROR", "service": "auth", "msg": "Token expired"},
    {"level": "INFO", "service": "api", "msg": "Request OK"},
])

# Group errors by service
errors = cfilter(lambda l: l["level"] == "ERROR", logs)
grouped = errors.group_by(lambda l: l["service"], val_fn=lambda l: l["msg"])
print(grouped.to_list())
# [('auth', ['Login failed', 'Token expired']), ('api', ['Timeout'])]

# Count errors per service
counts = errors.group_by(lambda l: l["service"]).map(
    lambda svc, msgs: (svc, len(msgs))
)
print(counts.to_list())
# [('auth', 2), ('api', 1)]
```

### Example 3: Data Pipeline

```python
from trent import seq, cmap, cfilter, cat, mapcat

# Raw data
raw = seq([
    {"category": "electronics", "items": ["phone", "laptop"]},
    {"category": "clothing", "items": ["shirt", "pants"]},
    {"category": "electronics", "items": ["tablet", "charger"]},
])

# Flatten all items across categories
all_items = mapcat(lambda r: r["items"], raw)
print(all_items.to_list())
# ['phone', 'laptop', 'shirt', 'pants', 'tablet', 'charger']

# Group items by category
grouped = raw.group_by(lambda r: r["category"], val_fn=lambda r: r["items"])
print(grouped.to_dict())
# {'electronics': ['phone', 'laptop', 'tablet', 'charger'], 'clothing': ['shirt', 'pants']}
```

### Example 4: Parallel Processing

```python
from trent import seq, pmap
import hashlib

files = seq(["file1.txt", "file2.txt", "file3.txt"])

def compute_hash(filename):
    # Simulate CPU-intensive hashing
    with open(filename, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

hashes = pmap(compute_hash, files)
print(hashes.to_list())
```

---

## Quick Reference

| Category | Functions |
|---|---|
| **Create** | `seq()`, `coll()`, `icoll()` |
| **Map** | `cmap()`, `pmap()`, `pmap_()`, `pairmap()`, `.map()`, `.apply()` |
| **Filter** | `cfilter()`, `.filter()`, `.remove()`, `.remove_none()` |
| **Flatten** | `cat()`, `.cat()`, `.mapcat()`, `.catmap()` |
| **Partition** | `.partition()`, `.partition_by()`, `.partmap()` |
| **Group** | `.group_by()`, `.groupmap()`, `groupmap()`, `groupcoll()` |
| **Access** | `first()`, `second()`, `third()`, `.head`, `.tail()` |
| **Reduce** | `.reduce()`, `.collect()` |
| **Take** | `.take()`, `.takewhile()` |
| **Collect** | `.to_list()`, `.to_set()` |
| **Mutate** | `.extend_()`, `.append_()`, `.cons_()`, `.concat()`, `.conj()` |
| **Parallel** | `pmap()`, `pmap_()`, `.pmap()`, `.pmap_()` |
| **Async** | `.async_map()`, `.async_map_()`, `.async_foreach()`, `.async_partmap()`, `.async_partmap_()` |
| **Pairs** | `.as_spans()`, `.pairmap()`, `map_to_pair()`, `.to_dict()` |
