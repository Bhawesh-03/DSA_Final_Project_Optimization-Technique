# src/freq_count.py
from collections import Counter

def freq_count_naive(data):
    """O(n^2)-like frequency count by calling list.count() for each unique item."""
    unique_items = list(set(data))
    result = []
    for x in unique_items:
        result.append((x, data.count(x)))  # list.count is O(n) each
    return result

def freq_count_counter(data):
    """O(n) average-case frequency count using collections.Counter."""
    return Counter(data)
