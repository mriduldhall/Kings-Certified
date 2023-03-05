import cv2 as cv
import numpy as np
from time import sleep


class ComputerVision:
    def __init__(self):
        self.isTrue = None
        self.frame = None
        self.bi_filter = None
        self.blank = None
        self.canny = None
        self.contours, self.hierarchies = None, None

        self.token_list = []
        self.token_colours = {"Red": (10, 10, 230),
                              "Yellow": (10, 230, 230),
                              "Blue": (230, 10, 10)}
        self.GRID_SIZE = (7, 6)

        self.empty_marker = 0
        self.player1_marker = 1
        self.player2_marker = 2
        self.robot_marker = "R"

        self.player1_colour = "Red"
        self.player2_colour = "Yellow"
        self.robot_colour = self.player2_colour

    def refresh_attributes(self, capture):
        # self.isTrue, self.frame = capture.read()
        self.frame = cv.imread('Test_Images/picture2.jpg')
        self.blank = np.zeros((self.frame.shape[1], self.frame.shape[0]), dtype='uint8')
        self.bi_filter = cv.bilateralFilter(self.frame, 15, 150, 150)
        self.canny = cv.Canny(self.bi_filter, 125, 175)
        self.contours, self.hierarchies = cv.findContours(self.canny, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        self.token_list = []

    def get_grid_size(self):
        rightmost_circle_centre = self.token_list[0][0]
        leftmost_circle_centre = self.token_list[0][0]

        for i in range(len(self.token_list)):
            # rightmost
            if self.token_list[i][0][0] > rightmost_circle_centre[0]:
                rightmost_circle_centre = self.token_list[i][0]
            elif self.token_list[i][0][0] < leftmost_circle_centre[0]:
                leftmost_circle_centre = self.token_list[i][0]

        grid_width_pixels = rightmost_circle_centre[0] - leftmost_circle_centre[0]

        # print(f"Rightmost: {rightmost_circle_centre}")
        # print(f"leftmost: {leftmost_circle_centre}")
        # print(f"Grid width: {grid_width_pixels}")
        # print()

        highest_circle_centre = self.token_list[0][0]
        lowest_circle_centre = self.token_list[0][0]

        for i in range(len(self.token_list)):
            # rightmost
            if self.token_list[i][0][1] < highest_circle_centre[1]:
                highest_circle_centre = self.token_list[i][0]
            elif self.token_list[i][0][1] > lowest_circle_centre[1]:
                lowest_circle_centre = self.token_list[i][0]

        grid_height_pixels = highest_circle_centre[1] - lowest_circle_centre[1]

        grid_size_pixels = (grid_width_pixels, grid_height_pixels)
        top_left_approx = (leftmost_circle_centre[0], highest_circle_centre[1])

        # print(f"Highest: {highest_circle_centre}")
        # print(f"Lowest: {leftmost_circle_centre}")
        # print(f"Grid height: {grid_height_pixels}")
        # print(f"Grid size {grid_size_pixels}")

        return grid_size_pixels, top_left_approx

    def round_token_grid(self, grid_dimensions, top_left_point):
        width, height = grid_dimensions
        width_divisor = width / (7 - 1)
        height_divisor = height / (6 - 1)
        rounded_tokens = []
        # Round pixels to a 7x6 grid
        offset = top_left_point
        for point in range(len(self.token_list)):
            offset_x = self.token_list[point][0][0] - offset[0]
            offset_y = self.token_list[point][0][1] - offset[1]
            rounded_x = offset_x / width_divisor
            rounded_y = offset_y / height_divisor
            rounded_centre = (round(rounded_x), round(rounded_y) * -1)

            point_colour = self.token_list[point][1]

            rounded_tokens.append([rounded_centre, point_colour])
        return rounded_tokens

    def remove_duplicate_items(self, tokens):
        unique_points = []
        for token in tokens:
            if token not in unique_points:
                unique_points.append(token)
        return unique_points

    def sort_rounded_tokens(self, rounded_tokens):
        blank_grid = [[(column, row) for column in range(self.GRID_SIZE[0])] for row in range(self.GRID_SIZE[1])]

        for column in range(len(blank_grid)):
            for row in range(len(blank_grid[0])):
                for token in rounded_tokens:
                    if (row, column) in token:
                        blank_grid[column][row] = token[0], token[1]

        return blank_grid

    def print_grid(self, grid):
        print()
        for columns in range(len(grid)):
            for rows in range(len(grid[0])):
                print(f"[{grid[columns][rows]}]", end="")
            print()

    def convert_to_game_grid(self, colour_grid):
        game_grid = [[None for column in range(self.GRID_SIZE[0])] for row in range(self.GRID_SIZE[1])]

        for column in range(len(game_grid)):
            for row in range(len(game_grid[0])):
                if colour_grid[column][row][1] == self.player1_colour:
                    game_grid[column][row] = self.player1_marker

                elif colour_grid[column][row][1] == self.player2_colour:
                    game_grid[column][row] = self.player2_marker

                elif colour_grid[column][row][1] == self.robot_colour:
                    game_grid[column][row] = self.robot_marker

                else:
                    game_grid[column][row] = self.empty_marker

        return game_grid

    def average_colour(self, circle_centre, radius):
        mask = np.zeros_like(self.bi_filter)

        cv.circle(mask, circle_centre, radius, (255, 255, 255), -1)

        masked_img = cv.bitwise_and(self.bi_filter, mask)
        pixels = masked_img[np.where(masked_img[:, :, 0] != 0)]

        min_colour = np.array([0, 0, 0])
        max_colour = np.array([0, 0, 0])

        excluded_pixels = (pixels >= min_colour) & (pixels <= max_colour)
        pixels = pixels[~np.all(excluded_pixels, axis=1)]

        mean_colour = np.mean(pixels, axis=0)

        # print(f"Average colour: {mean_colour}")
        return mean_colour

    def token_colour(self, average_colour):
        colour_threshold = 100

        for token_colour in self.token_colours:
            colour_true = True
            for BGR in range(len("BGR")):
                if not (self.token_colours[token_colour][BGR] - colour_threshold <= average_colour[BGR] <=
                        self.token_colours[token_colour][BGR] + colour_threshold):
                    colour_true = False
            if colour_true:
                return token_colour

    def rescale_frame(self, frame, scale=0.2):
        width = int(frame.shape[1] * scale)
        height = int(frame.shape[0] * scale)
        dimensions = (width, height)
        return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

    # this function is unnecessary as all filtering is done on assignment in refresh_attributes()
    def image_filtering(self, frame):
        bi_filter = cv.bilateralFilter(frame, 15, 150, 150)
        self.blank = np.zeros((frame.shape[1], frame.shape[0]), dtype='uint8')

        # canny edge detection
        canny = cv.Canny(bi_filter, 125, 175)
        contours, hierarchies = cv.findContours(canny, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        # cv.drawContours(blank, contours, -1, (255, 255, 255), 1)

    def shape_detection(self):
        for i, contour in enumerate(self.contours):
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

            min_rad = 10
            max_rad = 20

            cv.drawContours(self.blank, self.contours, 0, (0, 0, 255), 1)

            if len(approx_polygon) > circle_threshold and min_rad < rad < max_rad:
                cv.circle(self.bi_filter, coords, rad, circle_colour, 2)
                # cv.rectangle(bi_filter, (x, y), (x+w, y+h), rectangle_colour, 2)

                # bound_area = bi_filter[y:y+h, x:x+w]
                # circle_colour = np.mean(bound_area, axis=(0, 1))
                # print(str(circle_colour))
                circle_colour = self.average_colour(coords, rad)

                single_token_colour = self.token_colour(circle_colour)
                font = cv.FONT_HERSHEY_SIMPLEX
                cv.putText(self.bi_filter, single_token_colour, (coords[0] - int(rad / 4), coords[1]), font, 0.5,
                           (255, 255, 255), 1, cv.LINE_AA)

                self.token_list.append([coords, single_token_colour])

    def count_tokens_in_grid(self, grid):
        print(grid)
        print(f"Token No.: {len(grid)}")
        yellow_counter = 0
        red_counter = 0

        for i in range(len(grid)):
            if grid[i][1] == "Red":
                red_counter += 1
            elif grid[i][1] == "Yellow":
                yellow_counter += 1
        print(f"Red: {red_counter}\nYellow: {yellow_counter}")

    def main(self, capture):
        self.refresh_attributes(capture)
        self.shape_detection()

        draw_distance = 700
        x1, y1 = (self.bi_filter.shape[1] - 50, self.bi_filter.shape[0] - 50)
        x2, y2 = x1 - draw_distance, y1

        cv.line(self.bi_filter, (x1, y1), (x2, y2), (0, 0, 255), thickness=2)
        cv.imshow("Labeled, Filtered Feed", self.bi_filter)

        # self.print_grid(self.token_list)

        grid_dims, top_left = self.get_grid_size()
        rounded_tokens = self.remove_duplicate_items(self.round_token_grid(grid_dims, top_left))
        sorted_tokens = self.sort_rounded_tokens(rounded_tokens)

        # print("Rounded, unsorted grid:")
        # self.print_grid(rounded_tokens)

        # print("Rounded and Sorted")
        # self.print_grid(sorted_tokens)

        converted_grid = self.convert_to_game_grid(sorted_tokens)
        # print(converted_grid)

        return converted_grid


if __name__ == "__main__":
    capture = cv.VideoCapture(0)
    a = ComputerVision()
    board_prev = []
    board_current = [1]
    while board_prev != board_current:
        board_current = a.main(capture)
        a.print_grid(board_current)
        sleep(0.2)
        # board_prev = a.main(capture)
        if cv.waitKey(0):
            break
