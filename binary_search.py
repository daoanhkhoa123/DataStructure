def binary_search(l, n):
    """
    Args:
        l (list of float)
        n (float): to find

    Returns:
        int: index
        None when not found
    """
    first = 0
    last = len(l) - 1

    while last >= first:
        mid = (first+last)//2

        if l[mid] == n:
            return mid
        else:
            if n > l[mid]:
                first = mid + 1

            else:
                last = mid - 1

    return None
