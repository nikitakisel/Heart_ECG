import cv2
import numpy as np
import math

import find_contours
import rectangle
import curve_analysis


def main():
    picture = "img/magic_CUT.jpg"
    # img = cv2.imread(picture, cv2.IMREAD_GRAYSCALE)

    img = cv2.imread(picture)
    img_height, img_width, img_channels = img.shape
    result = img.copy()

    upper_contour, _ = find_contours.find_contours("img/magic_CUT.jpg", 29)
    _, lower_contour = find_contours.find_contours("img/magic_CUT.jpg", 11)

    # show coordinates and scale
    print(f'Coordinates of line: {upper_contour}')
    small_rectangle_length, axis_variants = rectangle.find_small_scale(picture)
    big_rectangle_length = 5 * small_rectangle_length
    print(f'Scale: 1 second is {big_rectangle_length} px')

    # find main axis
    point_axis = max(item[1] for item in upper_contour)
    ind = 0
    while axis_variants[ind] < point_axis:
        ind += 1

    # show main axis
    real_axis = axis_variants[ind]
    cv2.line(result, (0, real_axis), (img_width, real_axis), (255, 0, 0), 2)

    # show points of ecg line
    for item in upper_contour:
        cv2.circle(result, (item[0], item[1]), radius=1, color=(255, 0, 0), thickness=-1)

    # find minimums and maximums
    minimums, maximums = curve_analysis.find_extremes(upper_contour)

    # DANGEROUS PART!!!
    _, maximums = curve_analysis.find_extremes(upper_contour)
    potential_minimums, _ = curve_analysis.find_extremes(lower_contour)
    minimums = []

    for i in range(1, len(maximums), 3):
        for minimum in potential_minimums:
            if abs(maximums[i][0] - minimum[0]) <= small_rectangle_length:
                minimums.append(minimum)

    # show minimums and maximums
    minimum_letters = ['Q', 'S']
    maximum_letters = ['P', 'R', 'T']

    for i in range(len(minimums)):
        x, y = minimums[i][0], minimums[i][1]
        cv2.circle(result, (x, y), radius=3, color=(0, 0, 255), thickness=-1)
        cv2.putText(result, minimum_letters[i % 2], (x - 20, y + 20) if i % 2 == 0 else (x + 5, y + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        # cv2.putText(result, minimum_letters[i % 3], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    for i in range(len(maximums)):
        x, y = maximums[i][0], maximums[i][1]
        cv2.circle(result, (x, y), radius=3, color=(44, 211, 15), thickness=-1)
        cv2.putText(result, maximum_letters[i % 3], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (44, 211, 15), 2)

    # show window
    cv2.namedWindow('Electric cardiogram of heart', cv2.WINDOW_NORMAL)
    cv2.imshow('Electric cardiogram of heart', result)

    if cv2.waitKey(0) & 0xFF == ord('q'):
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
