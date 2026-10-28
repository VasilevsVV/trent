# trent — Project Summary

## Overview

`trent` is a Python library (v0.5.4) for **convenient sequence/iterable/collection processing**, inspired by **Clojure mapping and threading macros** and the functional programming style of Common Lisp / Clojure.

- **Python ≥ 3.13** only
- ~2 100 lines of Python across 10 source files
- Dependencies: `funcy`, `psutil`

---

## Goals

- Functional-style sequence processing with **full Python 12 typing** (unlike built-in `map`/`filter`)
- Lazy evaluation where possible
- Built-in **async** and **parallel** mapping
- Clojure-style `->` / `->>` / `as->` threading convenience (via `interface.py` functions)
- Prototyping-friendly, readable, type-hinted code

## Non-goals

- High-performance / high-load sequence processing
- Table-like data processing (use pandas / polars / PySpark instead)

---

## Architecture

```
trent/
├── __init__.py        # Public API surface (exports everything)
├── collection_core.py # Abstract base: Collection[T]
├── coll.py            # CollectionImpl — concrete Collection
├── paired_coll.py     # PairedCollection[T1, T2] — for key-value / tuple sequences
├── interface.py       # Standalone convenience functions (seq, cmap, cfilter, pmap, …)
├── concur.py          # Async / parallel execution pool (psutil + concurrent.futures)
├── coll_aux.py        # Internal helpers: DistinctFilter, Rangifier, PartCounter, PartByCounter
├── nth.py             # first, second, third, nth (+ raising variants: first_, second_, nth_)
├── func.py            # identity, getter/gtr/gtr_, isnone
└── exceptions.py      # MissingValueException, EmptyCollectionException
```

### Core types

| Class | Parametrisation | Purpose |
|---|---|---|
| `Collection[T]` | `Collection` (abstract base) | Lazy, typed sequence (implements `Iterable[T]`) |
| `CollectionImpl[T]` | `Collection[T]` | Concrete implementation; also produces `PairedCollection` |
| `PairedCollection[T1, T2]` | `Collection[Tuple[T1, T2]]` | Key–value / tuple sequences (e.g. grouped results) |

All collection classes are **lazy** by default (iterators passed through). A `persist()` call forces materialisation so the collection can be iterated multiple times.

---

## Public API

### Entry points / constructors

| Function | Returns | Notes |
|---|---|---|
| `seq(iterable)` | `Collection` | Wraps any iterable; dicts → items |
| `coll(iterable)`, `icoll(iterable)` | `Collection` | Aliases for `seq` |

### Mapping & filtering

| Function | Signature | Notes |
|---|---|---|
| `cmap(f, seq)` | `Collection[S]` | Lazy map |
| `cfilter(pred, seq)` | `Collection[T]` | Lazy filter |
| `pmap(f, seq)` | `Collection[S]` | Parallel (multiprocessing `Pool`) |
| `pmap_(f, seq, threads)` | `Collection[S]` | Parallel with explicit thread count |
| `catmap(f, seq)` | `Collection[S] | `cat().map(f)` |

### Concatenation & flattening

| Function | Signature | Notes |
|---|---|---|
| `cat(seq)` | `Collection` | Flatten nested iterables |
| `mapcat(f, seq)` | `Collection` | Map then flatten |
| `pairmap(f, seq)` | `Collection` | Map over `(a, b)` pairs |
| `groupmap(f, seq)` | `Collection` | Group-by with transform |
| `groupcoll(seq)` | `Collection` | Ungroup (reverse of groupmap) |

### Pairs & key extraction

| Function | Signature | Notes |
|---|---|---|
| `map_to_pair(seq, f_key [, f_val])` | `PairedCollection` | Map element → `(key, value)` |
| `rangify(seq)` | `PairedCollection` | **Deprecated** → use `as_spans()` |

### Element accessors

| Function | Raises on empty? |
|---|---|
| `first(coll)`, `second(coll)`, `third(coll)` | No (returns `None`) |
| `first_(coll)`, `second_(coll)`, `nth_(coll, n)` | Yes (`MissingValueException`) |

### Utility functions

| Function | Returns |
|---|---|
| `identity(x)` | `x` |
| `getter(key, default)` / `gtr(key, default)` | Callable that pulls a dict key |
| `gtr_(key, type)` | Callable that pulls a dict key, raises on missing |
| `isnone(val)` | `TypeIs[None]` |

---

## Collection methods (selected)

### Mapping & transformation

| Method | Returns | Notes |
|---|---|---|
| `.map(f)` | `Collection[S]` | Lazy |
| `.pmap(f)` | `Collection[S]` | Multiprocessing Pool |
| `.pmap_(f, threads)` | `Collection[S]` | Pool with explicit thread count |
| `.async_map(f)` | `Collection[S]` | Thread pool (I/O-bound) |
| `.async_map_(f, threads)` | `Collection[S]` | Thread pool with explicit count |
| `.mapcat(f)` | `Collection` | Map → flatten |
| `.cat()` | `Collection` | Flatten (identity map) |
| `.catmap(f)` | `Collection` | Flatten → map |
| `.pairmap(f)` | `Collection` | Map over `(a, b)` pairs |
| `.apply(f)` | `Collection[T]` | Side-effect map (same type) |

### Filtering

| Method | Returns | Notes |
|---|---|---|
| `.filter(pred)` | `Self` | Lazy |
| `.remove(pred)` | `Self` | Complement of filter |
| `.remove_none(*types)` | `Collection` | Remove `None` values |
| `.distinct()` / `.unique()` | `Self` | Remove duplicates (not lazy) |
| `.distinct_by(f)` | `Self` | Distinct by key |

### Take / slice

| Method | Returns | Notes |
|---|---|---|
| `.take(n)` | `Self` | First n elements |
| `.takewhile(pred)` | `Self` | While predicate holds |
| `.head` | `T` | First element (non-destructive) |
| `.tail()` | `Self` | All but first |

### Partitioning

| Method | Returns | Notes |
|---|---|---|
| `.partition(n)` | `Collection[list]` | Fixed-size chunks |
| `.partition_by(pred)` | `Collection[list]` | Split on predicate change |
| `.partmap(f)` | `Collection[list]` | Map over partitions |
| `.async_partmap(f [, threads])` | `Collection[list]` | Async over partitions |
| `.async_partmap_(f, threads)` | `Collection[list]` | Async over partitions, explicit threads |

### Grouping

| Method | Returns | Notes |
|---|---|---|
| `.group_by(f [, val_fn])` | `PairedCollection` | Group by key (eager) |
| `.groupmap(f)` | `Collection` | Ungroup / expand groups |
| `.group_by_to_dict(f [, val_fn])` | `dict` | Returns plain dict |

### Pairs & spans

| Method | Returns | Notes |
|---|---|---|
| `.as_spans(fail_if_single=False)` | `PairedCollection` | Adjacent pairs (sliding window 2) |
| `.rangify()` | `PairedCollection` | **Deprecated** → `.as_spans()` |

### Reduction & collection

| Method | Returns | Notes |
|---|---|---|
| `.reduce(f [, initial])` | `T` / `S` | Fold / reduce |
| `.to_list()` | `list` | Materialise |
| `.to_set()` | `set` | Materialise |
| `.collect(f)` | `S` | Materialise + transform |

### In-place mutation

| Method | Returns | Notes |
|---|---|---|
| `.extend_(iterable)` | `Self` | Chain-extend |
| `.append_(val)` | `Self` | Append single |
| `.cons_(val)` | `Self` | Prepend single |

### Other

| Method | Returns | Notes |
|---|---|---|
| `.concat(*iterables)` | `Self` | New collection with appended iterables |
| `.extend(iterable)` | `Self` | Alias for `.concat` |
| `.conj(*vals)` | `Self` | Concat single values |
| `.append(val)` | `Self` | Append single value |
| `.cons(val)` | `Self` | Prepend single value |
| `.__add__(iter)` | `Self` | Supports `coll + iterable` |
| `.persist()` | `Self` | Materialise for repeated iteration |
| `.empty` | `bool` | Is collection empty? |
| `.head` | `T` | First element (cached) |

---

## Async / Parallel

| Module / Object | Details |
|---|---|
| `concur.py` | `CPU_COUNT` (from `psutil` or `multiprocessing`), `TRENT_THREADPOOL` (global `ThreadPoolExecutor(CPU_COUNT * 2)`) |
| `async_map` | Uses `TRENT_THREADPOOL` (global, shared) |
| `async_map_` | Uses `concurrent.futures.ThreadPoolExecutor` (local, per-call) |
| `pmap` / `pmap_` | Uses `multiprocessing.Pool` (process-based, CPU-bound) |
| `async_foreach` | New in v0.5.4 — runs `asyncio`-based foreach over threads |

---

## Internal helpers (`coll_aux.py`)

| Class | Purpose |
|---|---|
| `DistinctFilter` | Callable that tracks seen values; returns `True` only on first encounter |
| `Rangifier` | Sliding-window pair generator for `as_spans()` |
| `PartCounter` | Fixed-size partition counter (for `.partition()`) |
| `PartByCounter` | Predicate-based partition counter (for `.partition_by()`) |

---

## Exceptions

| Exception | When |
|---|---|
| `EmptyCollectionException` | Empty `.head`, `.tail`, empty `.as_spans(fail_if_single=True)` |
| `MissingValueException` | `first_()`, `second_()`, `nth_()` on empty / short sequence |

---

## Testing

8 test files in `test/`:

| File | Covers |
|---|---|
| `test_coll.py` | Core `Collection` operations |
| `test_coll_async.py` | Async mapping |
| `test_coll_paired.py` | `PairedCollection` |
| `test_coll_transform.py` | Transformations |
| `test_combined_pipeline.py` | Chained operations |
| `test_paired_coll.py` | `PairedCollection` (duplicate coverage?) |
| `test_interfcae.py` | Interface functions (note: typo in filename) |

---

## Recent commits (chronological, newest first)

| Commit | Message |
|---|---|
| `9124159` | Bump version: 0.5.3 → 0.5.4 |
| `3ffced8` | Added async_foreach |
| `39f9b79` | Bump version: 0.5.2 → 0.5.3 |
| `7dce552` | Reworked typing and typehinting |
| `c1f5552` | Updated pyproject |
| `e415bdc` | Bump version: 0.5.1 → 0.5.2 |
| `14a743b` | Fixed more typing issues |
| `770e915` | Bump version: 0.5.0 → 0.5.1 |
| `4c41587` | Small fix for typing |
| `933639a` | Fixed init |
| `4300e18` | Bump version: 0.4.8 → 0.5.0 |
| `781ca9f` | Updated dependencies |
| `aa6a983` | Reworked "as_spans()" again. Fixed tests |
| `c240379` | Deprecated method `rangify()`. Renamed to `as_spans()` |
| `3b9d728` | Updated interface `rangify` |
| `439c2a1` | Added more tests |
| `8cb43ff` | Code cleanup |
| `84ca789` | Some fixes for `tail()` |
| `ca77efa` | Reworked `rangify()` method |
| `59d122a` | Added `paired_seq`. Added more tests |

---

## Known issues / quirks

1. **Typo in test filename**: `test_interfcae.py` (should be `test_interface.py`)
2. **Duplicate test coverage**: `test_coll_paired.py` and `test_paired_coll.py` both test `PairedCollection`
3. **Global state**: `TRENT_THREADPOOL` is a module-level global — not cleaned up; can cause issues in tests
4. **Eager operations**: `.group_by()`, `.distinct()`, `.head` all materialise portions of the collection
5. **Python 3.13+ only**: Uses `Self` type, `TypeIs`, and other newer typing features
6. **`rangify()` deprecated**: Renamed to `as_spans()`, but old name kept as alias
7. **Spelling in README**: "Supprot", "vesrsion", "asyncronously", "usefull", "maintanable" — several typos
8. **`__no_value` duplicated**: Both `collection_core.py` and `nth.py` define their own sentinel class

---

## How to run

```bash
# Install
pip install -e .

# Run tests
pytest test/ -v

# Type check (pyright)
pyright trent/
```
