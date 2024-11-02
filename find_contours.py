import cv2
import numpy as np

__all__ = []


def find_contours(picture, kernel_limit):
    img = cv2.imread(picture)

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
    kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT,
        (kernel_limit, kernel_limit),
    )
    morph = cv2.morphologyEx(morph, cv2.MORPH_CLOSE, kernel)

    # filter contours on area
    contours = cv2.findContours(
        morph,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )
    contours = contours[0] if len(contours) == 2 else contours[1]

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

    # cv2.namedWindow('Electric cardiogram of heart', cv2.WINDOW_NORMAL)
    # cv2.imshow('Electric cardiogram of heart', result)

    # if cv2.waitKey(0) & 0xFF == ord('q'):
    #     cv2.destroyAllWindows()

    return line1, line2
