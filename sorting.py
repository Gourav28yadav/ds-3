import random
import time
import copy
import sys

# quick sort hits recursion limit on sorted arrays so increase it
sys.setrecursionlimit(25000)


# --- sorting algorithms ---

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    # add remaining
    while i < len(left):
        result.append(left[i])
        i += 1
    while j < len(right):
        result.append(right[j])
        j += 1
    return result


def quick_sort(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)
        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)
    return arr

def partition(arr, low, high):
    pivot = arr[high]  # last element as pivot
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


# --- timing function ---

def measure_time(sort_func, arr):
    arr_copy = copy.deepcopy(arr)
    start = time.time()
    if sort_func == quick_sort:
        sort_func(arr_copy, 0, len(arr_copy) - 1)
    else:
        arr_copy = sort_func(arr_copy)
    end = time.time()
    return arr_copy, (end - start) * 1000  # in ms


# --- dataset generation ---

def make_datasets(sizes):
    data = {}
    for s in sizes:
        random.seed(42)
        data[s] = {
            "random": [random.randint(1, 100000) for _ in range(s)],
            "sorted": list(range(1, s + 1)),
            "reverse": list(range(s, 0, -1))
        }
    return data


# --- main ---

if __name__ == "__main__":

    print("=" * 60)
    print("  Sorting Performance Analyzer")
    print("=" * 60)

    # correctness check first
    print("\n--- Correctness Check ---")
    test = [5, 2, 9, 1, 5, 6]
    expected = [1, 2, 5, 5, 6, 9]
    print(f"input: {test}")

    r1 = insertion_sort(test.copy())
    print(f"insertion sort: {r1}  {'PASS' if r1 == expected else 'FAIL'}")

    r2 = merge_sort(test.copy())
    print(f"merge sort:     {r2}  {'PASS' if r2 == expected else 'FAIL'}")

    r3 = test.copy()
    quick_sort(r3, 0, len(r3) - 1)
    print(f"quick sort:     {r3}  {'PASS' if r3 == expected else 'FAIL'}")

    # performance tests
    print("\n--- Performance Tests ---")
    sizes = [1000, 5000, 10000]
    datasets = make_datasets(sizes)
    types = ["random", "sorted", "reverse"]

    results = {}
    for s in sizes:
        for t in types:
            d = datasets[s][t]
            _, t1 = measure_time(insertion_sort, d)
            _, t2 = measure_time(merge_sort, d)
            _, t3 = measure_time(quick_sort, d)
            results[(s, t)] = (t1, t2, t3)

    # print table
    print(f"\n{'Size':<8}{'Type':<10}{'Insertion(ms)':>14}{'Merge(ms)':>12}{'Quick(ms)':>12}")
    print("-" * 56)
    for s in sizes:
        for t in types:
            ins, mer, qs = results[(s, t)]
            print(f"{s:<8}{t:<10}{ins:>14.2f}{mer:>12.2f}{qs:>12.2f}")
        print()

    # observations
    print("--- Observations ---")
    print("""
Random input:
  insertion sort is slow because of O(n^2), lots of shifting.
  merge sort and quick sort are fast, both O(n log n) on average.

Sorted input:
  insertion sort is very fast here (best case O(n), nothing to shift).
  merge sort stays same as always.
  quick sort becomes slow because last element pivot on sorted data
  gives worst case O(n^2) partitioning.

Reverse sorted:
  insertion sort worst case, every element shifted to beginning.
  merge sort still consistent.
  quick sort also slow, same pivot issue.

Stability:
  insertion sort - stable, in-place
  merge sort - stable, not in-place (uses extra O(n) space)
  quick sort - not stable, in-place
""")

    print("done.")
