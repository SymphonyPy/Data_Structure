def get_next(p):
    next = [i for i in range(len(p))]
    next[0] = -1
    i = 0
    k = -1
    while i < len(p) - 1:
        if k == -1 or p[i] == p[k]:
            i += 1
            k += 1
            next[i] = k
        else:
            k = next[k]
    return next


def kmp(s, p):
    if len(p) == 0:
        return 0
    next = get_next(p)
    i = 0
    j = 0
    while i < len(s) and j < len(p):
        if j == -1 or s[i] == p[j]:
            i += 1
            j += 1
        else:
            j = next[j]
    if j == len(p):
        return i - len(p)
    else:
        return -1


def positions(string, pattern):
    poss = []
    pos = kmp(string, pattern)
    while pos != -1:
        string = string[:pos] + string[pos + len(pattern):]
        poss.append(pos)
        pos = kmp(string, pattern)
    return poss


def count(string, pattern):
    total = 0
    pos = kmp(string, pattern)
    while pos != -1:
        string = string[:pos] + string[pos + len(pattern):]
        total += 1
        pos = kmp(string, pattern)
    return total
