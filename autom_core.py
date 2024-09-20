# Core Py Funcs


def map(func, iterable):
    return [func(item) for item in iterable]


def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def sorted(iterable, key=None, reverse=False):
    # Convert iterable to a list
    list_to_sort = list(iterable)

    # Define a default key function if none is provided
    if key is None:
        key = lambda x: x

    # Bubble sort implementation
    n = len(list_to_sort)
    for i in range(n):
        for j in range(0, n - i - 1):
            if (key(list_to_sort[j]) > key(list_to_sort[j + 1])) ^ reverse:
                list_to_sort[j], list_to_sort[j + 1] = (
                    list_to_sort[j + 1],
                    list_to_sort[j],
                )
    return list_to_sort


def zip(*iterables):
    # Get the length of the shortest iterable
    min_length = min(len(iterable) for iterable in iterables)

    # Create a list of tuples
    return [tuple(iterable[i] for iterable in iterables) for i in range(min_length)]


def filter(func, iterable):
    return [item for item in iterable if func(item)]


def reversed(sequence):
    result = []
    for i in range(len(sequence) - 1, -1, -1):
        result.append(sequence[i])
    return result
