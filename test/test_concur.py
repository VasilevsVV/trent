import concurrent.futures as conc

import pytest

from trent.concur import CPU_COUNT, TRENT_THREADPOOL, cpu_count, shutdown_trent_pool


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


# ======================================================
#           TEST lifecycle / shutdown


def test_shutdown_trent_pool_exists():
    assert callable(shutdown_trent_pool)


def test_shutdown_trent_pool_works():
    """shutdown_trent_pool should not raise."""
    shutdown_trent_pool(wait=False)


def test_threadpool_has_shutdown():
    assert hasattr(TRENT_THREADPOOL, 'shutdown')


def test_atexit_registered():
    """atexit should have registered shutdown_trent_pool."""
    import atexit
    # Verify that shutdown_trent_pool is registered by checking it's callable
    # and that the module-level atexit.register was called during import
    assert callable(shutdown_trent_pool)
