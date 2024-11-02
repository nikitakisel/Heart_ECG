import cv2

import find_contours
import rectangle
import curve_analysis
import curve_calculation

__all__ = []


def main():
    picture = 'img/magic_CUT_new.jpg'
    show_picture = 'img/default_CUT_new.jpg'
    # img = cv2.imread(picture, cv2.IMREAD_GRAYSCALE)

    img = cv2.imread(picture)
    img_height, img_width, img_channels = img.shape
    result = cv2.imread(show_picture)

    upper_contour, _ = find_contours.find_contours(picture, 29)
    _, lower_contour = find_contours.find_contours(picture, 11)

    # show coordinates and scale
    print(f'Coordinates of line: {upper_contour}')
    small_rectangle_length, axis_variants = rectangle.find_small_scale(picture)
    real_scale = 25 * small_rectangle_length
    print(f'Scale: 1 second is {real_scale} px')

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
        cv2.circle(
            result,
            (item[0], item[1]),
            radius=1,
            color=(255, 0, 0),
            thickness=-1,
        )

    # find minimums and maximums
    # minimums, maximums = curve_analysis.find_extremes(upper_contour)

    # DANGEROUS PART!!!
    _, maximums = curve_analysis.find_extremes(upper_contour)
    potential_minimums, _ = curve_analysis.find_extremes(lower_contour)
    minimums = curve_analysis.find_neighbour_minimums(
        maximums,
        3,
        [1],
        potential_minimums,
    )

    # find establish points
    potential_establish_points = curve_analysis.find_establish_points(
        upper_contour,
        small_rectangle_length,
    )
    establish_points = curve_analysis.find_neighbour_minimums(
        maximums,
        3,
        [0, 2],
        potential_establish_points,
    ) + curve_analysis.find_neighbour_maximums(
        minimums,
        5,
        potential_establish_points,
    )
    establish_points.sort()

    # show a layout
    curve_calculation.draw_layout(
        result,
        maximums,
        establish_points,
        small_rectangle_length,
    )

    # draw establish points
    for item in establish_points:
        cv2.circle(
            result,
            (item[0], item[1]),
            radius=3,
            color=(0, 120, 255),
            thickness=-1,
        )

    # show minimums and maximums
    minimum_letters = ['Q', 'S']
    maximum_letters = ['P', 'R', 'T']

    for i in range(len(minimums)):
        x, y = minimums[i][0], minimums[i][1]
        cv2.circle(result, (x, y), radius=3, color=(0, 0, 255), thickness=-1)
        cv2.putText(
            result,
            minimum_letters[i % 2],
            (x - 20, y + 20) if i % 2 == 0 else (x + 5, y + 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 255),
            2,
        )

    for i in range(len(maximums)):
        x, y = maximums[i][0], maximums[i][1]
        cv2.circle(result, (x, y), radius=3, color=(44, 211, 15), thickness=-1)
        cv2.putText(
            result,
            maximum_letters[i % 3],
            (x - 10, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (44, 211, 15),
            2,
        )

    # print parameters calculation
    curve_calculation.print_parameters(maximums, establish_points, real_scale)

    # show window
    cv2.namedWindow('Electric cardiogram of heart', cv2.WINDOW_NORMAL)
    cv2.imshow('Electric cardiogram of heart', result)

    if cv2.waitKey(0) & 0xFF == ord('q'):
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
