import cv2
import numpy as np


def red(circle_img):
    circle_img = cv2.cvtColor(circle_img, cv2.COLOR_BGR2HSV)

    # lower boundary RED color range values; Hue (0 - 10)
    lower1 = np.array([0, 100, 20])
    upper1 = np.array([10, 255, 255])

    # upper boundary RED color range values; Hue (160 - 180)
    lower2 = np.array([160, 100, 20])
    upper2 = np.array([179, 255, 255])

    lower_mask = cv2.inRange(circle_img, lower1, upper1)
    upper_mask = cv2.inRange(circle_img, lower2, upper2)

    full_mask = lower_mask + upper_mask
    result = cv2.bitwise_and(circle_img, circle_img, mask=full_mask)
    blacks = np.count_nonzero(result[::] == np.array([0, 0, 0]))
    total = np.prod(result.shape)

    # black is less than 60%
    if blacks / total < 0.6:
        return True
    return False


def yellow(circle_img):
    circle_img = cv2.cvtColor(circle_img, cv2.COLOR_BGR2HSV)

    # lower boundary Yellow color range values; Hue (10 - 87)
    lower = np.array([10, 140, 129])
    upper = np.array([87, 255, 255])

    mask = cv2.inRange(circle_img, lower, upper)

    result = cv2.bitwise_and(circle_img, circle_img, mask=mask)
    blacks = np.count_nonzero(result[::] == np.array([0, 0, 0]))
    total = np.prod(result.shape)

    # black is less than 60%
    if blacks / total < 0.6:
        return True
    return False


def get_most_common_color(img, circle):
    """
    :param img: The original Image
    :param circle: The coordinates of the circles in format (x, y, r).
    :return: R for red, Y for yellow and X for other
    """
    x, y, r = circle
    circle_img = img[y - r:y + r, x - r:x + r]
    if red(circle_img):
        return 'R'
    elif yellow(circle_img):
        return 'Y'
    return 'X'


def get_grid(img, coordinates: np.ndarray):
    """
    :param img: The original Image
    :param coordinates: The coordinates of the circles in format (x, y, r).
    :return: Grid in the format used by BOARD
    """
    n_of_rows, n_of_columns = 6, 7
    # Sort by y-coordiantes
    y_sorted = coordinates[coordinates[:, 1].argsort()]
    # Divide into matrix for each row
    rows = y_sorted.reshape((n_of_rows, n_of_columns, 3))
    # Sort each row by x-coordinate
    rows = rows[:, rows[:, :, 0].argsort()][np.diag_indices(n_of_rows)]

    grid = []
    for row in range(n_of_rows):
        single_row = []
        for column in range(n_of_columns):
            player = get_most_common_color(img, rows[row, column])
            if player == 'R':
                single_row.append(1)
            elif player == 'Y':
                single_row.append(2)
            else:
                single_row.append(0)
        grid.append(single_row)

    return grid


def get_coordinates(img):
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # To Reduce noise
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Detect red and blue circles using HoughCircles image2
    # circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 1.5, 20, param1=50, param2=30, minRadius=15, maxRadius=20)

    # Detect red and blue circles using HoughCircles image4
    circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 1.5, 20, param1=50, param2=30, minRadius=40, maxRadius=45)

    # Detect red and blue circles using HoughCircles image6
    # circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 1.5, 20, param1=50, param2=30, minRadius=35, maxRadius=40)

    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        return circles
    return None


if __name__ == '__main__':
    # Read the input image -- It can be video later.
    img = cv2.imread('Test_Images/picture4.jpg')

    coordinates = get_coordinates(img.copy())
    if coordinates is None:
        print('Error Reading the grid!')
    elif coordinates.shape != (42, 3):
        print('Not All the Grid Read Successfully!!')
    else:
        grid = get_grid(img, coordinates)
        for row in grid:
            print(row)

    cv2.imshow('Original Image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
