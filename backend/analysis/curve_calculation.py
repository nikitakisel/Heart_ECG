import cv2

__all__ = []


def draw_lower_layout(img, x1, x2, y, layout_length, text):
    cv2.line(img, (x1, y), (x1, y + layout_length), (0, 0, 0), 1)
    cv2.line(img, (x2, y), (x2, y + layout_length), (0, 0, 0), 1)
    cv2.line(
        img,
        (x1, y + layout_length),
        (x2, y + layout_length),
        (0, 120, 255),
        2,
    )

    cv2.line(
        img,
        (x1, y + layout_length),
        (x1 + 5, y + layout_length + 3),
        (0, 0, 0),
        2,
    )
    cv2.line(
        img,
        (x1, y + layout_length),
        (x1 + 5, y + layout_length - 3),
        (0, 0, 0),
        2,
    )
    cv2.line(
        img,
        (x1 + 5, y + layout_length - 3),
        (x1 + 5, y + layout_length + 3),
        (0, 0, 0),
        2,
    )

    cv2.line(
        img,
        (x2 - 5, y + layout_length - 3),
        (x2, y + layout_length),
        (0, 0, 0),
        2,
    )
    cv2.line(
        img,
        (x2 - 5, y + layout_length + 3),
        (x2, y + layout_length),
        (0, 0, 0),
        2,
    )
    cv2.line(
        img,
        (x2 - 5, y + layout_length - 3),
        (x2 - 5, y + layout_length + 3),
        (0, 0, 0),
        2,
    )

    cv2.putText(
        img,
        text,
        ((x1 + x2) // 2 - 10, y + layout_length + 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.35,
        (255, 0, 0),
        1,
    )


def draw_upper_layout(img, x1, x2, y, layout_length, text):
    cv2.line(img, (x1, y), (x1, y - layout_length), (0, 0, 0), 1)
    cv2.line(img, (x2, y), (x2, y - layout_length), (0, 0, 0), 1)
    cv2.line(
        img,
        (x1, y - layout_length),
        (x2, y - layout_length),
        (0, 120, 255),
        2,
    )

    cv2.line(
        img,
        (x1, y - layout_length),
        (x1 + 5, y - layout_length + 3),
        (0, 0, 0),
        2,
    )
    cv2.line(
        img,
        (x1, y - layout_length),
        (x1 + 5, y - layout_length - 3),
        (0, 0, 0),
        2,
    )
    cv2.line(
        img,
        (x1 + 5, y - layout_length - 3),
        (x1 + 5, y - layout_length + 3),
        (0, 0, 0),
        2,
    )

    cv2.line(
        img,
        (x2 - 5, y - layout_length - 3),
        (x2, y - layout_length),
        (0, 0, 0),
        2,
    )
    cv2.line(
        img,
        (x2 - 5, y - layout_length + 3),
        (x2, y - layout_length),
        (0, 0, 0),
        2,
    )
    cv2.line(
        img,
        (x2 - 5, y - layout_length - 3),
        (x2 - 5, y - layout_length + 3),
        (0, 0, 0),
        2,
    )

    cv2.putText(
        img,
        text,
        ((x1 + x2) // 2 - 10, y - layout_length - 5),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.35,
        (255, 0, 0),
        1,
    )


def draw_layout(img, maximums, establish_points, small_rectangle_length):
    for i in range(len(establish_points) // 6):
        draw_lower_layout(
            img,
            establish_points[6 * i][0],
            establish_points[6 * i + 2][0],
            establish_points[6 * i][1],
            small_rectangle_length * 3,
            'Int PQ',
        )
        draw_lower_layout(
            img,
            establish_points[6 * i + 2][0],
            establish_points[6 * i + 3][0],
            establish_points[6 * i + 2][1],
            small_rectangle_length * 5,
            'QRS',
        )
        draw_lower_layout(
            img,
            establish_points[6 * i + 2][0],
            establish_points[6 * i + 5][0],
            establish_points[6 * i + 2][1],
            small_rectangle_length * 8,
            'Int QT',
        )

        draw_upper_layout(
            img,
            establish_points[6 * i + 1][0],
            establish_points[6 * i + 2][0],
            establish_points[6 * i + 1][1],
            small_rectangle_length * 3,
            'Seg PQ',
        )
        draw_upper_layout(
            img,
            establish_points[6 * i + 3][0],
            establish_points[6 * i + 4][0],
            establish_points[6 * i + 3][1],
            small_rectangle_length * 3,
            'Seg ST',
        )

    r_maximums = [maximums[i] for i in range(len(maximums)) if i % 3 == 1]
    for i in range(1, len(r_maximums)):
        draw_upper_layout(
            img,
            r_maximums[i - 1][0],
            r_maximums[i][0],
            r_maximums[i][1],
            (i + 1) * 20,
            f'Interval R{i}R{i + 1}',
        )


def print_parameters(maximums, establish_points, scale):
    for i in range(len(establish_points) // 6):
        print(f'Fragment {i + 1}:')
        segment_pq = round(
            (establish_points[6 * i + 2][0] - establish_points[6 * i + 1][0])
            / scale,
            3,
        )
        print(f'Segment PQ: {segment_pq} seconds')
        segment_st = round(
            (establish_points[6 * i + 4][0] - establish_points[6 * i + 3][0])
            / scale,
            3,
        )
        print(f'Segment ST: {segment_st} seconds')
        interval_pq = round(
            (establish_points[6 * i + 2][0] - establish_points[6 * i][0])
            / scale,
            3,
        )
        print(f'Interval PQ: {interval_pq} seconds')
        qrs = round(
            (establish_points[6 * i + 3][0] - establish_points[6 * i + 2][0])
            / scale,
            3,
        )
        print(f'QRS: {qrs} seconds')
        interval_qt = round(
            (establish_points[6 * i + 5][0] - establish_points[6 * i + 2][0])
            / scale,
            3,
        )
        print(f'Interval QT: {interval_qt} seconds\n')

    r_maximums = [maximums[i] for i in range(len(maximums)) if i % 3 == 1]
    print('Intervals RR:')
    for i in range(1, len(r_maximums)):
        print(
            f'R{i+1} - R{i} = '
            f'{round((r_maximums[i][0] - r_maximums[i - 1][0]) / scale, 3)}'
            f' seconds',
        )
