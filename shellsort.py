# Sort an array a[0...n-1].
_GAPS = [701, 301, 132, 57, 23, 10, 4, 1]  # Ciura gap sequence


def shellsort(l: list):
    for gap in _GAPS:
        # Start with the largest gap and work down to a gap of 1
        # similar to insertion sort but instead of 1, gap is being used in each step
        for i in range(gap, len(l)):
            temp = l[i]  # save a[i] in temp and make a hole at position i

            # shift earlier gap-sorted elements up until the correct location for a[i] is found
            j = i
            while j >= gap and l[j-gap] > temp:
                l[j] = l[j-gap]
                j -= gap

            l[j] = temp  # put temp (the original a[i]) in its correct location


if __name__ == "__main__":
    l = [6, 2, 3, 4, 4, 8, 2, 2, 7, 1, 6, 5, 8456, 234]
    shellsort(l)
    print(*l)
