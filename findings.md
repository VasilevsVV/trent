# Findings — `trent` Test Coverage Audit

> Companion to [PLAN.md](PLAN.md). All findings below were discovered during the read-only audit of the codebase and test suite conducted while creating the test-improvement plan.

## Project context

- Package: `trent` v0.5.4 (branch `paired_coll_support`), lazy sequence/iterable/collection processing for Python ≥3.13, inspired by Clojure mapping/threading macros; deps: `funcy`, `psutil`.

## Current test state

- **7 test files, 75 tests** (`test/`), no `conftest.py`, no coverage tooling.
- `SUMMARY.md` is stale: claims 8 test files, flags duplicate coverage, lists known quirks.

## Coverage gaps — modules with essentially no direct tests

1. `trent/nth.py` — public accessors `first/second/third/nth/first_/second_/nth_` (+ overloads) had no direct tests; only used indirectly via local `first_`/`second_` helpers in `test_coll_paired.py`.
2. `trent/func.py` — `identity`, `getter`, `gtr`, `gtr_`, `isnone`: no tests.
3. `trent/exceptions.py` — `MissingValueException`: no tests; `EmptyCollectionException` only covered for `head`, messages never asserted.
4. `trent/concur.py` — `cpu_count`, `CPU_COUNT`, `TRENT_THREADPOOL`: no tests.
5. `trent/coll_aux.py` — `DistinctFilter`, `Rangifier`, `PartCounter`, `PartByCounter`: no direct unit tests.
6. `trent/__init__.py` — exports/aliases: no tests.
7. `trent/interface.py` — covered partially (`seq`, `cmap`, `cfilter`, `cat`, `mapcat`); missing: `seq(None)`, `seq(dict)`, `paired_seq`, `pmap`/`pmap_`, `catmap`, `pairmap`, `groupcoll`, `groupmap`, `map_to_pair`, `rangify`.

## Coverage gaps — `Collection` surface with no or incomplete tests

- `reduce` (all overloads/behaviors) — **no tests at all**.
- `to_set` — **no tests**.
- `distinct` — **no tests** (only `unique`, `distinct_by`).
- `tail` on empty → raises `EmptyCollectionException` — untested.
- Async paths — mostly untested: `async_map_` threads=1 fallback, defaults, empty inputs, `async_foreach` threads=1/default/error-propagation, `async_partmap_` threads=1.
- `as_spans(fail_if_single=True)` — untested (raise path); empty-collection behavior with `fail_if_single` untested.
- `pairmap` with >2 elements (extra values dropped) — untested.
- Laziness (no evaluation until collect) — untested.

## Test infrastructure gaps

1. Typo filename: `test_interfcae.py` → should be `test_interface.py`.
2. Duplicate PairedCollection coverage: `test_coll_paired.py` vs `test_paired_coll.py` → consolidate.
3. No `conftest.py` / shared fixtures.
4. No coverage tooling; decision: add `pytest-cov` reporting only, no hard gate.
5. `pyproject.toml [tool.pytest.ini_options] pythonpath = ["trent"]` — likely incorrect; tests may run against installed copy in `.venv` instead of working tree.
6. Global `TRENT_THREADPOOL` (module-level, never shut down) — isolation concerns for async tests.
7. No CI configuration found.

## Potential source issues to fix alongside new tests

1. `async_foreach`: `asyncio.gather(..., return_exceptions=True)` **swallows exceptions** from user functions.
2. `reduce`: `initial: Optional[S] = None` conflates "no initial" and "initial=None".
3. `gtr_`: raises generic `Exception` instead of `MissingValueException`.
4. `cpu_count`: `assert res` lets `AssertionError` escape instead of falling back.
5. `remove_none(*_types)`: type args ignored (marked `# type: ignore`).
6. `as_spans(fail_if_single=True)` on empty collection: returns empty instead of raising (inconsistency).
7. `__no_value` sentinel duplicated in `collection_core.py` and `nth.py`.
8. `TRENT_THREADPOOL` never shut down; `head` not thread-safe (lock created but unused).

## Open items

- Final prioritization of plan phases.
- CI workflow addition (none found).