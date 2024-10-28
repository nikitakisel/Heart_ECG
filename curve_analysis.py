def find_extremes(array):
    deltas = [0] + [array[i][1] - array[i+1][1] for i in range(len(array) - 1)]
    start = 0
    while deltas[start] == 0:
        start += 1

    minimums = []
    maximums = []
    growth = True if deltas[start] > 0 else False

    for i in range(start + 1, len(deltas)):
        if deltas[i] > 0 and not growth:
            minimums.append(array[i - 1])
            growth = True
        elif deltas[i] < 0 and growth:
            maximums.append(array[i-1])
            growth = False

    return minimums, maximums
