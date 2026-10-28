# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

`trent` — convenient sequence/iterable/collection processing for Python (requires Python >= 3.13; environment currently runs 3.14.8), inspired by Clojure mapping and threading macros and the functional style of Common Lisp / Clojure.

- Provides lazy, fully typehinted collections/sequences: map, filter, take, concat, group, spans (`as_spans`), reduce, etc.
- Public entry points: `trent.seq` (aliases `coll`, `icoll`) plus functional convenience wrappers in `trent.interface` (e.g. `cmap`, `cfilter`, `pmap`, `cat`, `map_to_pair`).
- Async / parallel execution via `trent.concur` (thread pools, multiprocessing).
- Not intended for high-load or table-like data processing (pandas/polars/pyspark territory).

## Commands

Run tests (from repo root, using the local venv):

```bash
source .venv/bin/activate
python -m pytest                 # full suite
python -m pytest test/test_coll.py::test_mapping_1   # single test
python -m pytest test/           # by directory
```

Lint (config in `ruff.toml`):

```bash
ruff check .
ruff format .
```

Build distribution:

```bash
python -m build
```

Version bump (config in `.bumpversion.cfg`):

```bash
bumpversion <part>   # patch | minor | major
```

## Architecture

High-level module layout (source lives in `trent/`):

- `trent/collection_core.py` — `Collection[T]` base class: lazy sequence operations (`map`, `pmap`, async variants, `filter`, `take`, `concat`, `reduce`, …) plus abstract capabilities (`as_spans`, `rangify`, `group_by`, `map_to_pair`) that concrete implementations provide. Lazy by default; `persist()` forces materialization; `head` caches the first element (`empty` / `tail` derive from it).
- `trent/coll.py` — `CollectionImpl[T]`, concrete `Collection`; adds paired-sequence capabilities (`map_to_pair`, `group_by`, `as_spans`, `rangify`).
- `trent/paired_coll.py` — `PairedCollection[T1, T2]`: a `Collection` over tuple pairs; pair/group operations, spans, `to_dict`.
- `trent/interface.py` — standalone functional convenience functions over sequences: `seq`, `coll`, `icoll`, `cmap`, `cfilter`, `pmap`, `pmap_`, `cat`, `mapcat`, `catmap`, `pairmap`, `groupcoll`, `groupmap`, `map_to_pair`, `rangify`.
- `trent/concur.py` — CPU detection (`cpu_count`) and execution pools (`CPU_COUNT`, `TRENT_THREADPOOL`).
- `trent/coll_aux.py` — internal helpers: `DistinctFilter`, `Rangifier`, `PartCounter`, `PartByCounter`.
- `trent/nth.py` — element accessors: `first`, `second`, `third`, `nth`, plus strict variants `first_`, `second_`, `nth_` raising on missing values.
- `trent/func.py` — utilities: `identity`, `getter`, `gtr`, `gtr_`, `isnone`.
- `trent/exceptions.py` — `MissingValueException`, `EmptyCollectionException`.

Big picture flow: functional composition over lazy collections → `Collection` / `CollectionImpl` operation chain → `PairedCollection` for pair/group semantics → interface helpers for ergonomic function-call style.

## Testing & Current State

- Test suite in `test/` (pytest; `pyproject.toml` sets `pythonpath = ["trent"]`, `testpaths = ["test"]`). Currently 75 tests passing across 7 test files.
- In-flight work tracked in `PLAN.md` and `findings.md` (test-coverage improvement plan; branch `tests_improvements`).
- Supporting docs: `README.md`, `USER_GUIDE.md`, `SUMMARY.md`.

## Docs

- `README.md` — project pitch and non-goals.
- `USER_GUIDE.md` — usage and feature walkthrough.
- `SUMMARY.md` — architecture / API summary (stale — may lag source).
- `PLAN.md`, `findings.md` — test-improvement plan and audit findings.