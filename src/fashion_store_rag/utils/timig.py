import time


def timed_search(search_function, **kwargs):
    start = time.perf_counter()
    results = search_function(**kwargs)
    elapsed_ms = (time.perf_counter() - start) * 1000

    return results, elapsed_ms
