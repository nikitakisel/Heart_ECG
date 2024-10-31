import math


def print_parameters(maximums, establish_points, scale):
    for i in range(len(establish_points) // 6):
        print(f"Fragment {i + 1}:")
        print(f"Segment PQ: {round((establish_points[6 * i + 2][0] - establish_points[6 * i + 1][0]) / scale, 3)} seconds")
        print(f"Segment ST: {round((establish_points[6 * i + 4][0] - establish_points[6 * i + 3][0]) / scale, 3)} seconds")
        print(f"Interval PQ: {round((establish_points[6 * i + 2][0] - establish_points[6 * i][0]) / scale, 3)} seconds")
        print(f"QRS: {round((establish_points[6 * i + 3][0] - establish_points[6 * i + 2][0]) / scale, 3)} seconds")
        print(f"Interval QT: {round((establish_points[6 * i + 5][0] - establish_points[6 * i + 2][0]) / scale, 3)} seconds")
        print("")

    r_maximums = [maximums[i] for i in range(len(maximums)) if i % 3 == 1]
    print("Intervals RR:")
    for i in range(1, len(r_maximums)):
        print(f"R{i+1} - R{i} = {round((r_maximums[i][0] - r_maximums[i - 1][0]) / scale, 3)} seconds")
