import cv2
import numpy as np


class Connect4Detector:
    def __init__(self, img_path, radius=40, n_of_rows=6, n_of_column=7):
        self.img = cv2.imread(img_path)
        self.n_of_rows = n_of_rows
        self.n_of_columns = n_of_column
        self.radius = radius
        self.players = {
            'R': 1,
            'Y': 2,
            'X': 0
        }
        # Colours Range in Hue
        # RED
        self.lower_red1 = np.array([0, 100, 20])
        self.upper_red1 = np.array([10, 255, 255])
        self.lower_red2 = np.array([160, 100, 20])
        self.upper_red2 = np.array([179, 255, 255])
        # YELLOW
        self.lower_yellow = np.array([10, 140, 129])
        self.upper_yellow = np.array([87, 255, 255])

    def _is_red(self, circle_img):
        """
        Returns True if the circle is mostly RED else False.
        """
        circle_img = cv2.cvtColor(circle_img, cv2.COLOR_BGR2HSV)
        lower_mask = cv2.inRange(circle_img, self.lower_red1, self.upper_red1)
        upper_mask = cv2.inRange(circle_img, self.lower_red2, self.upper_red2)
        full_mask = lower_mask + upper_mask
        result = cv2.bitwise_and(circle_img, circle_img, mask=full_mask)
        blacks = np.count_nonzero(result[::] == np.array([0, 0, 0]))
        total = np.prod(result.shape)
        return blacks / total < 0.6

    def _is_yellow(self, circle_img):
        """
        Returns True if the circle is mostly YELLOW else False.
        """
        circle_img = cv2.cvtColor(circle_img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(circle_img, self.lower_yellow, self.upper_yellow)
        result = cv2.bitwise_and(circle_img, circle_img, mask=mask)
        blacks = np.count_nonzero(result[::] == np.array([0, 0, 0]))
        total = np.prod(result.shape)
        return blacks / total < 0.6

    def _get_most_common_color(self, circle):
        """
        Takes an image and a circle and returns the most common color in the area where the circle is drawn.
        """
        x, y, r = circle
        circle_img = self.img[y - r: y + r, x - r: x + r]
        if self._is_red(circle_img):
            return "R"
        elif self._is_yellow(circle_img):
            return "Y"
        return "X"

    def _get_coordinates(self):
        """
        Detects circles in the given image and returns their coordinates.
        """
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        circles = cv2.HoughCircles(
            blur,
            cv2.HOUGH_GRADIENT,
            1.5,
            20,
            param1=50,
            param2=30,
            minRadius=self.radius,
            maxRadius=self.radius + 5,
        )
        if circles is not None:
            return np.round(circles[0, :]).astype("int")
        return None

    def detect(self):
        """
        Given an image path, detects the Connect 4 game and returns its state.
        """
        coordinates = self._get_coordinates()
        if coordinates is None:
            print("No circles detected.")
            return None
        y_sorted = coordinates[coordinates[:, 1].argsort()]
        rows = y_sorted.reshape((self.n_of_rows, self.n_of_columns, 3))
        rows = rows[:, rows[:, :, 0].argsort()][np.diag_indices(self.n_of_rows)]

        grid = []
        for row in range(self.n_of_rows):
            single_row = []
            for column in range(self.n_of_columns):
                player = self._get_most_common_color(rows[row, column])
                single_row.append(self.players[player])
            grid.append(single_row)

        return grid


if __name__ == '__main__':
    img_path = 'Images/Test_Images/picture4.jpg'
    img4 = Connect4Detector(img_path)
    grid = img4.detect()
    for row in grid:
        print(row)
    # To show the image for testing purposes!
    cv2.imshow(img_path, cv2.imread(img_path))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # img4.img = cv2.imread('Images/Test_Images/picture2.jpg')
    # img4.radius = 15
    # grid = img4.detect()
    # for row in grid:
    #     print(row)
    # cv2.imshow('Images/Test_Images/picture2.jpg', cv2.imread('Images/Test_Images/picture2.jpg'))
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

