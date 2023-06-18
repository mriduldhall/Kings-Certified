from cv2 import imshow, imread, bilateralFilter, Canny, findContours, RETR_TREE, CHAIN_APPROX_SIMPLE, circle, \
    bitwise_and, arcLength, approxPolyDP, boundingRect, FONT_HERSHEY_SIMPLEX, putText, LINE_AA, line, \
    VideoCapture, waitKey, destroyAllWindows
from numpy import zeros_like, where, array, all, mean


class ComputerVision:
    def __init__(self, minimum_radius=20, maximum_radius=25, colour_threshold=100, video=True, development=False):
        self.bi_filter = None
        self.canny = None
        self.contours = None 
        self.hierarchies = None

        self.token_colours = {"Red": (10, 10, 230),
                              "Yellow": (10, 230, 230),
                              "Blue": (230, 10, 10)}
        
        self.rows = 6
        self.columns = 7
        
        self.empty_marker = 0
        self.player1_marker = 1
        self.player2_marker = 2
        self.robot_marker = "R"

        self.player1_colour = "Red"
        self.player2_colour = "Yellow"
        self.robot_colour = self.player2_colour
        
        self.min_rad = minimum_radius
        self.max_rad = maximum_radius
        self.colour_threshold = colour_threshold
        self.development = development
        self.video = video

    def refresh_attributes(self, capture):
        if self.video:
            is_true, frame = capture.read()
            imshow("Raw", frame)
        else:
            frame = imread(capture)
        self.bi_filter = bilateralFilter(frame, 15, 150, 150)
        canny = Canny(self.bi_filter, 125, 175)
        self.contours, self.hierarchies = findContours(canny, RETR_TREE, CHAIN_APPROX_SIMPLE)

    @staticmethod
    def get_grid_size(token_list):
        rightmost_circle_centre = token_list[0][0]
        leftmost_circle_centre = token_list[0][0]

        for i in range(len(token_list)):
            if token_list[i][0][0] > rightmost_circle_centre[0]:
                rightmost_circle_centre = token_list[i][0]
            elif token_list[i][0][0] < leftmost_circle_centre[0]:
                leftmost_circle_centre = token_list[i][0]

        grid_width_pixels = rightmost_circle_centre[0] - leftmost_circle_centre[0]

        highest_circle_centre = token_list[0][0]
        lowest_circle_centre = token_list[0][0]

        for i in range(len(token_list)):
            if token_list[i][0][1] < highest_circle_centre[1]:
                highest_circle_centre = token_list[i][0]
            elif token_list[i][0][1] > lowest_circle_centre[1]:
                lowest_circle_centre = token_list[i][0]

        grid_height_pixels = highest_circle_centre[1] - lowest_circle_centre[1]
        grid_size_pixels = (grid_width_pixels, grid_height_pixels)
        top_left_approx = (leftmost_circle_centre[0], highest_circle_centre[1])
        
        return grid_size_pixels, top_left_approx

    @staticmethod
    def round_token_grid(token_list, grid_dimensions, top_left_point):
        width, height = grid_dimensions
        width_divisor = width / (7 - 1)
        height_divisor = height / (6 - 1)
        rounded_tokens = []
        
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

    @staticmethod
    def remove_duplicate_items(tokens):
        unique_points = []
        for token in tokens:
            if token not in unique_points:
                unique_points.append(token)
        return unique_points

    def sort_rounded_tokens(self, rounded_tokens):
        blank_grid = [[(column, row) for column in range(self.columns)] for row in range(self.rows)]

        for column in range(len(blank_grid)):
            for row in range(len(blank_grid[0])):
                for token in rounded_tokens:
                    if (row, column) in token:
                        blank_grid[column][row] = token[0], token[1]

        return blank_grid

    @staticmethod
    def print_grid(grid):
        print()
        for columns in range(len(grid)):
            for rows in range(len(grid[0])):
                print(f"[{grid[columns][rows]}]", end="")
            print()

    def print_board(self, board):
        print()
        print('   |   '.join([str(column) for column in [col for col in range(self.columns)]]))
        print("".join(['-' for _ in range(self.columns * 7)]))
        print('\n'.join(['       '.join([str(cell) for cell in row]) for row in board]))
        print()

    def convert_to_game_grid(self, colour_grid):
        game_grid = [[None for column in range(self.columns)] for row in range(self.rows)]
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
        mask = zeros_like(self.bi_filter)

        circle(mask, circle_centre, radius, (255, 255, 255), -1)

        masked_img = bitwise_and(self.bi_filter, mask)
        pixels = masked_img[where(masked_img[:, :, 0] != 0)]

        min_colour = array([0, 0, 0])
        max_colour = array([0, 0, 0])

        excluded_pixels = (pixels >= min_colour) & (pixels <= max_colour)
        pixels = pixels[~all(excluded_pixels, axis=1)]

        mean_colour = mean(pixels, axis=0)

        return mean_colour

    def token_colour(self, average_colour):
        for token_colour in self.token_colours:
            colour_true = True
            for BGR in range(len("BGR")):
                if not (self.token_colours[token_colour][BGR] - self.colour_threshold <= average_colour[BGR] <=
                        self.token_colours[token_colour][BGR] + self.colour_threshold):
                    colour_true = False
            if colour_true:
                return token_colour

    def shape_detection(self):
        token_list = []
        for i, contour in enumerate(self.contours):
            if i == 0:
                continue

            epsilon = 0.01 * arcLength(contour, True)
            approx_polygon = approxPolyDP(contour, epsilon, True)
            x, y, w, h = boundingRect(approx_polygon)
            x_mid = int(x + w / 2)
            y_mid = int(y + h / 2)
            coords = (x_mid, y_mid)
            rad = int(w / 2)
            circle_threshold = 10

            if len(approx_polygon) > circle_threshold and self.min_rad < rad < self.max_rad:
                circle_colour = self.average_colour(coords, rad)
                single_token_colour = self.token_colour(circle_colour)
                token_list.append([coords, single_token_colour])
                
                if self.development:
                    font = FONT_HERSHEY_SIMPLEX
                    circle(self.bi_filter, coords, rad, (0, 255, 0), 2)
                    putText(self.bi_filter, single_token_colour, (x_mid - int(rad / 4), y_mid),
                            font, 0.5, (255, 255, 255), 1, LINE_AA)
                    
        return token_list

    def get_grid(self):
        token_list = self.shape_detection()
        print(token_list)
        grid_dims, top_left = self.get_grid_size(token_list)
        rounded_token_grid = self.round_token_grid(token_list, grid_dims, top_left)
        rounded_tokens = self.remove_duplicate_items(rounded_token_grid)
        sorted_tokens = self.sort_rounded_tokens(rounded_tokens)
        converted_grid = self.convert_to_game_grid(sorted_tokens)

        if self.development:
            draw_distance = 700
            x1, y1 = (self.bi_filter.shape[1] - 50, self.bi_filter.shape[0] - 50)
            x2, y2 = x1 - draw_distance, y1
            
            line(self.bi_filter, (x1, y1), (x2, y2), (0, 0, 255), thickness=2)
            imshow("Labeled, Filtered Feed", self.bi_filter)
            
        return converted_grid

    @staticmethod
    def get_move(previous_grid, current_grid):
        for row in range(len(previous_grid)):
            for column in range(len(previous_grid[row])):
                if previous_grid[row][column] != current_grid[row][column]:
                    return column

    def analyse_feed(self, previous_grid, capture):
        self.refresh_attributes(capture)
        current_grid = self.get_grid()
        if self.development:
            self.print_board(previous_grid)
            self.print_board(current_grid)
            print(previous_grid)
            print(current_grid)
        return self.get_move(previous_grid, current_grid)


if __name__ == "__main__":
    prev_grid = [[0, 0, 0, 0, 0, 0, 0], 
                 [0, 0, 0, 0, 0, 2, 0], 
                 [0, 2, 0, 2, 0, 1, 0], 
                 [2, 1, 1, 1, 2, 2, 1], 
                 [2, 1, 2, 2, 1, 1, 1], 
                 [1, 2, 1, 1, 2, 1, 2]
                 ]
    capture = VideoCapture(0)
    a = ComputerVision(20, 50, 120, True, True)
    print(a.analyse_feed(prev_grid, capture))

    if waitKey(0):
        destroyAllWindows()
