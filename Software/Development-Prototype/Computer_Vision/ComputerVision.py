import cv2 as cv
from time import sleep
import numpy as np

token_colours = {"Red": (10, 10, 230), "Yellow": (10, 230, 230), "Blue": (230, 10, 10)}

# img = cv.imread("miku.png")
# cv.imshow("Miku", img)

capture = cv.VideoCapture(0)


# capture = cv.VideoCapture("Domino's App Feat Hatsune Miku (Original).mp4")

def rescale_frame(frame, scale=0.2):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)
    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)


def token_colour(average_colour):
    colour_threshold = 100

    for token_colour in token_colours:
        colour_true = True
        for BGR in range(len("BGR")):
            if not (token_colours[token_colour][BGR] - colour_threshold <= average_colour[BGR] <=
                    token_colours[token_colour][BGR] + colour_threshold):
                colour_true = False
        if colour_true:
            return token_colour


def average_colour(filtered_img, radius, circle_centre):
    mask = np.zeros_like(filtered_img)

    cv.circle(mask, circle_centre, radius, (255, 255, 255), -1)

    masked_img = cv.bitwise_and(filtered_img, mask)
    pixels = masked_img[np.where(masked_img[:, :, 0] != 0)]

    min_colour = np.array([0, 0, 0])
    max_colour = np.array([0, 0, 0])

    excluded_pixels = (pixels >= min_colour) & (pixels <= max_colour)
    pixels = pixels[~np.all(excluded_pixels, axis=1)]

    mean_colour = np.mean(pixels, axis=0)

    # print(f"Average colour: {mean_colour}")
    return mean_colour


def height_width_calc(token_list):
    pass


def grid_size(token_list):
    rightmost_circle_centre = token_list[0][0]
    leftmost_circle_centre = token_list[0][0]

    for i in range(len(token_list)):
        # rightmost
        if token_list[i][0][0] > rightmost_circle_centre[0]:
            rightmost_circle_centre = token_list[i][0]
        elif token_list[i][0][0] < leftmost_circle_centre[0]:
            leftmost_circle_centre = token_list[i][0]

    grid_width_pixels = rightmost_circle_centre[0] - leftmost_circle_centre[0]

    print(f"Rightmost: {rightmost_circle_centre}")
    print(f"leftmost: {leftmost_circle_centre}")
    print(f"Grid width: {grid_width_pixels}")
    print()

    highest_circle_centre = token_list[0][0]
    lowest_circle_centre = token_list[0][0]

    for i in range(len(token_list)):
        # rightmost
        if token_list[i][0][1] < highest_circle_centre[1]:
            highest_circle_centre = token_list[i][0]
        elif token_list[i][0][1] > lowest_circle_centre[1]:
            lowest_circle_centre = token_list[i][0]

    grid_height_pixels = highest_circle_centre[1] - lowest_circle_centre[1]

    grid_size_pixels = (grid_width_pixels, grid_height_pixels)
    top_left_approx = (leftmost_circle_centre[0], highest_circle_centre[1])

    print(f"Highest: {highest_circle_centre}")
    print(f"Lowest: {leftmost_circle_centre}")
    print(f"Grid height: {grid_height_pixels}")
    print(f"Grid size {grid_size_pixels}")

    return grid_size_pixels, top_left_approx


def round_tokens(token_list, grid_size_pixels, top_left_point):
    width, height = grid_size_pixels
    width_divisor = width / (7 - 1)
    height_divisor = height / (6 - 1)
    rounded_tokens = []
    # Round pixels to a 7x6 grid
    offset = top_left_point
    for point in range(len(token_list)):
        offset_x = token_list[point][0][0] - offset[0]
        offset_y = token_list[point][0][1] - offset[1]
        rounded_x = offset_x / width_divisor
        rounded_y = offset_y / height_divisor
        rounded_centre = (round(rounded_x), round(rounded_y) * -1)

        point_colour = token_list[point][1]

        rounded_tokens.append([rounded_centre, point_colour])
    return rounded_tokens


def remove_duplicates(rounded_tokens):
    unique_points = []
    for token in rounded_tokens:
        if token not in unique_points:
            unique_points.append(token)
    return unique_points


def sort_tokens(token_list):
    GRID_SIZE = (7, 6)
    blank_grid = [[(column, row) for column in range(GRID_SIZE[0])] for row in range(GRID_SIZE[1])]

    print_grid(blank_grid)

    for column in range(len(blank_grid)):
        for row in range(len(blank_grid[0])):
            for token in token_list:
                if (row, column) in token:
                    blank_grid[column][row] = token[0], token[1]
    return blank_grid


def print_grid(grid):
    print()
    for columns in range(len(grid)):
        for rows in range(len(grid[0])):
            print(f"[{grid[columns][rows]}]", end="")
        print()


def convert_to_game_grid(colour_grid):
    GRID_SIZE = (7, 6)

    empty_marker = 0
    player1_marker = 1
    player2_marker = 2
    robot_marker = "R"

    player1_colour = "Red"
    player2_colour = "Yellow"
    robot_colour = player2_colour

    game_grid = [[None for columns in range(GRID_SIZE[0])] for rows in range(GRID_SIZE[1])]

    for columns in range(len(game_grid)):
        for rows in range(len(game_grid[0])):
            if colour_grid[columns][rows][1] == player1_colour:
                game_grid[columns][rows] = player1_marker

            elif colour_grid[columns][rows][1] == player2_colour:
                game_grid[columns][rows] = player2_marker

            elif colour_grid[columns][rows][1] == robot_colour:
                game_grid[columns][rows] = robot_marker

            else:
                game_grid[columns][rows] = empty_marker

    return game_grid


count = 1
while count == 1:
    # isTrue, frame = capture.read()

    # frame = cv.imread("Maybe the thing\Test_Images\circles.png")
    frame = cv.imread("picture4.jpg")
    # frame = rescale_frame(frame, 0.4)

    bi_filter = cv.bilateralFilter(frame, 15, 150, 150)
    blank = np.zeros((frame.shape[1], frame.shape[0]), dtype='uint8')

    # canny edge detection
    canny = cv.Canny(bi_filter, 125, 175)
    contours, hierarchies = cv.findContours(canny, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    # cv.drawContours(blank, contours, -1, (255, 255, 255), 1)

    token_list = []

    for i, contour in enumerate(contours):
        if i == 0:
            continue

        epsilon = 0.01 * cv.arcLength(contour, True)
        approx_polygon = cv.approxPolyDP(contour, epsilon, True)
        x, y, w, h = cv.boundingRect(approx_polygon)
        x_mid = int(x + w / 2)
        y_mid = int(y + h / 2)
        coords = (x_mid, y_mid)
        circle_colour = (0, 255, 0)
        rectangle_colour = (255, 0, 0)
        rad = int(w / 2)

        circle_threshold = 10
        min_rad = 30
        max_rad = 100

        cv.drawContours(blank, contours, 0, (0, 0, 255), 1)

        if (len(approx_polygon) > circle_threshold) and min_rad < rad < max_rad:
            cv.circle(bi_filter, coords, rad, circle_colour, 2)
            # cv.rectangle(bi_filter, (x, y), (x+w, y+h), rectangle_colour, 2)

            # bound_area = bi_filter[y:y+h, x:x+w]
            # circle_colour = np.mean(bound_area, axis=(0, 1))
            # print(str(circle_colour))
            circle_colour = average_colour(bi_filter, rad, coords)
            single_token_colour = token_colour(circle_colour)
            font = cv.FONT_HERSHEY_SIMPLEX
            cv.putText(bi_filter, single_token_colour, (coords[0] - int(rad / 4), coords[1]), font, 0.5,
                       (255, 255, 255), 1, cv.LINE_AA)

            token_list.append([coords, single_token_colour])
            # token_list.append([coords, approx_colour(circle_colour)])

    draw_distance = 700
    x1, y1 = (bi_filter.shape[1] - 50, bi_filter.shape[0] - 50)
    x2, y2 = x1 - draw_distance, y1

    cv.line(bi_filter, (x1, y1), (x2, y2), (0, 0, 255), thickness=2)
    cv.imshow("Filtered Video", bi_filter)

    # cv.imshow("Canny Edges", canny)
    # cv.imshow("Masked Video", masked)

    print(token_list)
    print(f"Token No.: {len(token_list)}")
    yellow_counter = 0
    red_counter = 0

    for i in range(len(token_list)):
        if token_list[i][1] == "Red":
            red_counter += 1
        elif token_list[i][1] == "Yellow":
            yellow_counter += 1
    print(f"Red: {red_counter}\nYellow: {yellow_counter}")

    grid_dims, top_left = grid_size(token_list)
    rounded_tokens = remove_duplicates(round_tokens(token_list, grid_dims, top_left))

    print(f"Rounded token No.: {len(rounded_tokens)}")

    yellow_counter = 0
    red_counter = 0

    for i in range(len(rounded_tokens)):
        if rounded_tokens[i][1] == "Red":
            red_counter += 1
        elif rounded_tokens[i][1] == "Yellow":
            yellow_counter += 1
    print(f"Red: {red_counter}\nYellow: {yellow_counter}")

    for column in range(6):
        for row in range(7):
            print((f"[{rounded_tokens[column * 7 + row][0]}]"), end="")
        print("")

    sorted_tokens = sort_tokens(rounded_tokens)

    print_grid(sorted_tokens)
    print(convert_to_game_grid(sorted_tokens))
    sleep(0.2)
    if cv.waitKey(0) & 0xFF == ord("d"):
        break
    count = 0

# capture.release()
# cv.destroyAllWindows()
