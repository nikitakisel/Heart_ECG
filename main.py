import cv2
import numpy as np
import rectangle
import curve_analysis

__all__ = []


def main():
    # picture = "img/default.jpg"
    # img = cv2.imread(picture, cv2.IMREAD_GRAYSCALE)

    # img = cv2.imread("img/default.jpg")
    img = cv2.imread('img/magic_CUT.jpg')
    # img = cv2.imread("img/without_shadow.jpg")
    img_height, img_width, img_channels = img.shape

    # median blur
    median = cv2.medianBlur(img, 5)

    # threshold on black
    lower = (0, 0, 0)
    upper = (45, 45, 45)
    # upper = (15, 15, 15)
    thresh = cv2.inRange(median, lower, upper)

    # apply morphology open and close
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    morph = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (29, 29))
    morph = cv2.morphologyEx(morph, cv2.MORPH_CLOSE, kernel)

    # filter contours on area
    contours = cv2.findContours(
        morph,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )
    contours = contours[0] if len(contours) == 2 else contours[1]
    result = img.copy()
    line1 = []
    line2 = []

    # find ecg lines
    for i in range(len(contours)):
        area = cv2.contourArea(contours[i])
        if area > 3000:
            contour = np.ndarray.tolist(contours[i])
            prom = []
            for item in contour:
                prom.append(item[0])

            mi = min([item[0] for item in prom])
            ma = max([item[0] for item in prom])

            start_line = []
            j = 0

            while prom[j][0] != mi:
                start_line.append(prom[j])
                j += 1

            start_line.append(prom[j])
            start_line.reverse()
            start = j

            while prom[j][0] != ma:
                j += 1

            end_line = prom[j:]
            end_line.reverse()

            line1 = start_line + end_line
            line2 = prom[start : j + 1]
            # cv2.drawContours(result, [contours[i]], -1, (0, 0, 255), 2)

    # show coordinates and scale
    print(f'Coordinates of line: {line1}')
    small_rectangle_length, axis_variants = rectangle.find_small_scale(
        'img/magic_CUT.jpg',
    )
    big_rectangle_length = 5 * small_rectangle_length
    print(f'Scale: 1 second is {big_rectangle_length} px')

    # find main axis
    point_axis = max(item[1] for item in line2)
    ind = 0
    while axis_variants[ind] < point_axis:
        ind += 1

    # show main axis
    real_axis = axis_variants[ind] - 1
    cv2.line(result, (0, real_axis), (img_width, real_axis), (255, 0, 0), 2)

    # show points of ecg line
    for item in line1:
        cv2.circle(
            result,
            (item[0], item[1]),
            radius=1,
            color=(255, 0, 0),
            thickness=-1,
        )

    # show minimums and maximums
    minimums, maximums = curve_analysis.find_extremes(line1)
    minimum_letters = ['Q', 'S', '']
    maximum_letters = ['P', 'R', 'T']

    for i in range(len(minimums)):
        x, y = minimums[i][0], minimums[i][1]
        cv2.circle(result, (x, y), radius=3, color=(0, 0, 255), thickness=-1)
        cv2.putText(
            result,
            minimum_letters[i % 3],
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2,
        )

    for i in range(len(maximums)):
        x, y = maximums[i][0], maximums[i][1]
        cv2.circle(result, (x, y), radius=3, color=(44, 211, 15), thickness=-1)
        cv2.putText(
            result,
            maximum_letters[i % 3],
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (44, 211, 15),
            2,
        )

    # show window
    cv2.namedWindow('Electric cardiogram of heart', cv2.WINDOW_NORMAL)
    cv2.imshow('Electric cardiogram of heart', result)

    if cv2.waitKey(0) & 0xFF == ord('q'):
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
