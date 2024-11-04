import cv2

__all__ = []


def find_small_scale(image_path):
    # Read the input image
    input_image = image_path

    # Convert image to grayscale
    grayscale_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)

    # Convert to binary image
    _, binary_image = cv2.threshold(
        grayscale_image,
        150,
        255,
        cv2.THRESH_BINARY,
    )

    # Find all the contours
    all_contours, hierarchy = cv2.findContours(
        binary_image,
        cv2.RETR_LIST,
        cv2.CHAIN_APPROX_SIMPLE,
    )

    # Find mode
    variants = []
    axis_variants = []

    # Loop through individual contours
    for contour in all_contours:
        # Approximate contour to a polygon
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)

        # Calculate aspect ratio and bounding box
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            axis_variants.append(y)

            if w == h:
                variants.append(h)

    axis_variants = list(set(axis_variants))
    axis_variants.sort()

    return max(set(variants), key=variants.count), axis_variants
