# Test Improvement Plan — `trent` (v0.5.4)

## Context

- User request: "Please go through my code base and all tests I have here, and make a plan for improving tests. See what may be missing. The goal - fully cover the code and any potentiall issues."
- Branch: `paired_coll_support` (vs `main`); package `trent` — lazy sequence/iterable/collection processing for Python (≥3.13), inspired by Clojure mapping/threading macros; deps: `funcy`, `psutil`.
- User scope decisions (answered via AskUserQuestion):
  1. Source defects surfaced by the audit should be **fixed alongside the new tests** (not tests-only / not pin-only).
  2. Coverage reporting via `pytest-cov` is desired, but **no hard coverage gate** should be enforced yet.

## Current state

- Source (`trent/`, ~10 modules, ~2.1k LOC):
  - `collection_core.py` (771), `coll.py` (129), `paired_coll.py` (105), `interface.py` (92), `concur.py` (25), `coll_aux.py` (53), `nth.py` (167), `func.py` (52), `exceptions.py` (14), `__init__.py` (58).
- Tests (`test/`, 7 files, **75 tests**):
  - `test_coll.py` (32) — mapping/async_map, filter/remove/remove_none/apply, mapcat/catmap, unique/distinct_by, take/takewhile, partition(s)/partmap, cat, persist, head/empty/tail.
  - `test_coll_async.py` (4) — async_partmap ×3, async_foreach ×1.
  - `test_coll_paired.py` (11) — group_by_to_dict ×3, group_by, as_spans ×3, pairmap ×3, groupmap.
  - `test_coll_transform.py` (13) — concat/append/extend/cons/add, collect/to_list.
  - `test_combined_pipeline.py` (3) — chained operations incl. reduce.
  - `test_interfcae.py` (5) — seq/cmap/cfilter/cat/mapcat (filename typo).
  - `test_paired_coll.py` (7) — PairedCollection map_to_pair/pairmap_to_pair/paired_seq/paired_append/conj/cons (duplicate coverage).
- Docs: `SUMMARY.md` is stale — claims "8 test files", flags duplicates, lists known quirks.

## Audit findings — coverage gaps

### A. Modules with essentially **no direct tests**
1. `trent/nth.py` — public accessors `first/second/third/nth/first_/second_/nth_` (+ overloads): only used indirectly (group_by/pairmap call local `first_`/`second_` helpers). Missing: nth semantics, defaults, `MissingValueException`, non-iterable error paths.
2. `trent/func.py` — `identity`, `getter`, `gtr`, `gtr_`, `isnone`: no tests.
3. `trent/exceptions.py` — `MissingValueException`: no tests; `EmptyCollectionException`: only `head` path covered, messages not asserted.
4. `trent/concur.py` — `cpu_count`, `CPU_COUNT`, `TRENT_THREADPOOL`: no tests.
5. `trent/coll_aux.py` — `DistinctFilter`, `Rangifier`, `PartCounter`, `PartByCounter`: no direct unit tests.
6. `trent/__init__.py` — exports/aliases: no tests.
7. `trent/interface.py` — `seq/cmap/cfilter/cat/mapcat` covered; missing: `seq(None)`, `seq(dict)`, `paired_seq`, `pmap/pmap_`, `catmap`, `pairmap`, `groupcoll`, `groupmap`, `map_to_pair`, `rangify`.

### B. `Collection` surface with no or incomplete tests
- `reduce` (all overloads/behaviors) — **no tests at all**.
- `to_set` — **no tests**.
- `distinct` — **no tests** (only `unique`, `distinct_by`).
- `tail` on empty → raises `EmptyCollectionException` — untested.
- async paths: `async_map_` threads=1 fallback, defaults, empty inputs, `async_foreach` threads=1/default/error-propagation, `async_partmap_` threads=1 — mostly untested.
- `as_spans(fail_if_single=True)` — untested (raise path).
- `as_spans` on empty with `fail_if_single` — behavior.
- `pairmap` with >2 elements (extra values dropped) — untested.
- `groupmap`/`groupcoll` via interface — untested.
- laziness (no evaluation until collect) — untested.
- persist / head caching / `__repr__` / abstract instantiation — partial.

### C. Test infrastructure gaps
1. Typo filename: `test_interfcae.py` → should be `test_interface.py`.
2. Duplicate PairedCollection coverage: `test_coll_paired.py` vs `test_paired_coll.py` → consolidate.
3. No `conftest.py` / shared fixtures (empty collection, sample data).
4. No coverage tooling; decision: add `pytest-cov` **reporting only, no hard gate**.
5. `pyproject.toml [tool.pytest.ini_options] pythonpath = ["trent"]` — likely incorrect; tests may run against the *installed* copy in `.venv` instead of the working tree → should be fixed to truly cover the source under development.
6. Global `TRENT_THREADPOOL` (module-level, never shut down) — isolation concerns for async tests.
7. No CI configuration found.

### D. Potential source issues to fix alongside new tests (per user decision: fix alongside new tests)
1. `async_foreach`: `asyncio.gather(..., return_exceptions=True)` **swallows exceptions** from user functions.
2. `reduce`: `initial: Optional[S] = None` conflates "no initial" and "initial=None".
3. `gtr_`: raises generic `Exception` instead of `MissingValueException` (inconsistent with `first_`/`second_`/`nth_`).
4. `cpu_count`: `assert res` lets `AssertionError` escape instead of falling back.
5. `remove_none(*_types)`: type args ignored (marked `# type: ignore`).
6. `as_spans(fail_if_single=True)` on empty collection: returns empty instead of raising (inconsistency).
7. `__no_value` sentinel duplicated in `collection_core.py` and `nth.py`.
8. `TRENT_THREADPOOL` never shut down; `head` not thread-safe (lock created but unused).

## Proposed plan (phases)

- **Phase 1 — Audit & gap mapping**: ✅ done (this document).
- **Phase 2 — Test infrastructure**: add `conftest.py` fixtures; rename typo file; consolidate duplicate PairedCollection tests; fix `pythonpath` in `pyproject.toml`; add `pytest-cov` + coverage reporting; keep no hard gate.
- **Phase 3 — Unit tests for uncovered modules**: `nth`, `func`, `exceptions`, `concur`, `coll_aux`, `__init__` exports, interface wrappers/gaps.
- **Phase 4 — Behavior tests for uncovered surface & edge cases**, **plus source fixes** to the defects in section D, each with regression tests.

## Critical files to modify

- `test/` — rename `test_interfcae.py` → `test_interface.py`; consolidate `test_paired_coll.py` into `test_coll_paired.py` (or vice versa); add new unit/behavior test files.
- `pyproject.toml` — `[tool.pytest.ini_options]` (`pythonpath`, add `pytest-cov`).
- `conftest.py` — new (fixtures).
- `trent/*` — only for the defect fixes in section D (with accompanying regression tests).

## Verification

- `pytest test/ -v`
- `pytest --cov=trent --cov-report=term-missing` (reporting only, no gate).
- Re-run full suite after source fixes.

## Open items for the user (post-plan)

- Final prioritization of phases (e.g., start with Phase 2 → Phase 3 → Phase 4 → Phase 5).
- CI workflow addition (currently none found).