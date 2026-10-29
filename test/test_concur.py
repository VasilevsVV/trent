import concurrent.futures as conc

import pytest

from trent.concur import CPU_COUNT, TRENT_THREADPOOL, cpu_count


# ======================================================
#           TEST cpu_count


def test_cpu_count_returns_int():
    result = cpu_count()
    assert isinstance(result, int)


def test_cpu_count_positive():
    result = cpu_count()
    assert result > 0


def test_cpu_count_reasonable():
    result = cpu_count()
    assert result <= 1000  # sanity check


# ======================================================
#           TEST CPU_COUNT


def test_cpu_count_is_int():
    assert isinstance(CPU_COUNT, int)


def test_cpu_count_positive():
    assert CPU_COUNT > 0


# ======================================================
#           TEST TRENT_THREADPOOL


def test_threadpool_is_executor():
    assert isinstance(TRENT_THREADPOOL, conc.ThreadPoolExecutor)


def test_threadpool_submits_task():
    future = TRENT_THREADPOOL.submit(lambda: 42)
    assert future.result() == 42


def test_threadpool_map():
    results = list(TRENT_THREADPOOL.map(lambda x: x * 2, [1, 2, 3]))
    assert results == [2, 4, 6]
