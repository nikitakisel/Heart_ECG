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


def find_establish_points(array, min_distance):
    deltas = [0] + [array[i][1] - array[i+1][1] for i in range(len(array) - 1)]
    establish_points = []

    for i in range(1, len(deltas)):
        if deltas[i] == 0 and array[i][0] - array[i - 1][0] > min_distance / 2:
            establish_points.append(array[i - 1])
            establish_points.append(array[i])

    return establish_points


def find_neighbour_minimums(maximums, category_count, current_categories, potential_neighbour_minimums):
    category_maximums = [maximums[i] for i in range(len(maximums)) if i % category_count in current_categories]
    neighbour_minimums = []
    ind = 0

    for i in range(1, len(potential_neighbour_minimums)):
        if potential_neighbour_minimums[i][0] > category_maximums[ind][0] and \
                potential_neighbour_minimums[i][1] != category_maximums[ind][1]:

            k = 1
            while potential_neighbour_minimums[i - k][1] == category_maximums[ind][1]:
                k += 1

            neighbour_minimums.append(potential_neighbour_minimums[i - k])
            neighbour_minimums.append(potential_neighbour_minimums[i])
            ind += 1

            if ind == len(category_maximums):
                break

    return neighbour_minimums
