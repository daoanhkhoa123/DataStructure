def RotatedList(lst):
    l = 0
    h = len(lst) - 1

    while h >= l:
        m = (l+h) // 2

        if lst[m + 1] < lst[m] and lst[m] < lst[m - 1]:
            return m + 1

        elif lst[m] < lst[0]:
            h = m - 1

        else:
            l = m + 1

    return -1


lst = [4, 3, 5, 9, 8, 7, 2]
print(RotatedList(lst))
