import cv2
import numpy as np
from time import time


class Connect4Detector:
    def __init__(self, img_path, min_radius=40, max_radius=45, n_of_rows=6, n_of_column=7):
        self.img = cv2.imread(img_path)
        self.n_of_rows = n_of_rows
        self.n_of_columns = n_of_column
        self.min_radius = min_radius
        self.max_radius = max_radius
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
        # self.lower_yellow = np.array([10, 107, 129])
        # self.upper_yellow = np.array([87, 255, 255])

        # YELLOW pic5
        self.lower_yellow = np.array([10, 206, 139])
        self.upper_yellow = np.array([25, 255, 255])

    def _improve_image(self):
        temp_img = cv2.GaussianBlur(self.img, (5, 5), 0)
        hsv = cv2.cvtColor(temp_img, cv2.COLOR_BGR2HSV)

        lower_range = np.array([110, 50, 50])
        upper_range = np.array([130, 255, 255])

        # Image 3
        lower_range = np.array([67, 72, 88])
        upper_range = np.array([133, 255, 255])

        # Image 5
        # lower_range = np.array([60,87,98])
        # upper_range = np.array([120,228,255])

        mask = cv2.inRange(hsv, lower_range, upper_range)
        canny = cv2.Canny(mask, 10, 100)
        return canny

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
        return blacks / total < 0.9

    def _is_yellow(self, circle_img):
        """
        Returns True if the circle is mostly YELLOW else False.
        """
        circle_img = cv2.cvtColor(circle_img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(circle_img, self.lower_yellow, self.upper_yellow)
        result = cv2.bitwise_and(circle_img, circle_img, mask=mask)
        blacks = np.count_nonzero(result[::] == np.array([0, 0, 0]))
        total = np.prod(result.shape)
        return blacks / total < 0.9

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
        # gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        # blur = cv2.GaussianBlur(gray, (5, 5), 0)
        mask = self._improve_image()
        circles = cv2.HoughCircles(
            mask,
            cv2.HOUGH_GRADIENT,
            1.5,
            20,
            param1=50,
            param2=30,
            minRadius=self.min_radius,
            maxRadius=self.max_radius,
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
        elif coordinates.shape != (42, 3):
            print('Not All the Grid Read Successfully!!')
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
    start = time()
    img_path_4 = 'Test_Images/picture5.jpg'
    img4 = Connect4Detector(img_path_4, min_radius=10, max_radius=25)
    grid = img4.detect()
    # print(grid)
    for row in grid:
        print(row)
    print(time()-start)
    # # To show the image for testing purposes!
    cv2.imshow(img_path_4, cv2.imread(img_path_4))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # img_path_2 = 'Test_Images/picture2.jpg'
    # img2 = Connect4Detector(img_path_2, radius=15)
    # grid = img2.detect()
    # print(grid)
    # for row in grid:
    #     print(row)
    # # To show the image for testing purposes!
    # cv2.imshow(img_path_2, cv2.imread(img_path_2))
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # start = time()
    # img_path_6 = 'Test_Images/picture6.jpg'
    # img6 = Connect4Detector(img_path_6, radius=35)
    # grid = img6.detect()
    # print(grid)
    # end = time()
    # print(end-start)
    # for row in grid:
    #     print(row)
    # # To show the image for testing purposes!
    # cv2.imshow(img_path_2, cv2.imread(img_path_2))
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()



    # print("")
    #
    # img4.img = cv2.imread('Test_Images/picture5.jpg')
    # img4.radius = 35
    # grid = img4.detect()
    # for row in grid:
    #     print(row)
    # cv2.imshow('Test_Images/picture2.jpg', cv2.imread('Test_Images/picture5.jpg'))
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

