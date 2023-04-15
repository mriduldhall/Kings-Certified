from Software.Source.Connect_Four.Validator import Validator
from time import process_time as time
from copy import deepcopy


class Board:
    def __init__(self, rows, columns, empty, player_1, player_2, robot, grid=None):
        self.number_of_rows = rows
        self.number_of_columns = columns
        self.empty_marker = empty
        self.player_1_marker = player_1
        self.player_2_marker = player_2
        self.robot_marker = robot
        self.player_number_to_marker = {
            1: self.player_1_marker,
            2: self.player_2_marker,
            "R": self.robot_marker,
        }
        if not grid:
            self.grid = [[self.empty_marker for _ in range(self.number_of_columns)] for _ in range(self.number_of_rows)]
        else:
            self.grid = grid

    def check_victory(self):
        """
        :return: True: if the game has been won; else: False
        """
        test = {
            "column": [1, 0],
            "row": [0, 1],
            "diagonal_1": [1, 1],
            "diagonal_2": [1, -1],
        }
        coordinates = []
        for column_index in range(3, self.number_of_columns, 4):
            for row_index in range(self.number_of_rows):
                if self.grid[row_index][column_index]:
                    coordinates.append([row_index, column_index])
        for column_index in range(self.number_of_columns):
            for row_index in range(3, self.number_of_rows, 4):
                if (self.grid[row_index][column_index]) and ([row_index, column_index] not in coordinates):
                    coordinates.append([row_index, column_index])
        for coordinate in coordinates:
            marker = self.grid[coordinate[0]][coordinate[1]]
            for pattern in test.values():
                positive = True
                connected = []
                for _ in range(2):
                    row_check = coordinate[0]
                    column_check = coordinate[1]
                    while (Validator(row_check).range_validator(0, self.number_of_rows, equal_to_start=True) and
                           Validator(column_check).range_validator(0, self.number_of_columns, equal_to_start=True)) and \
                            (self.grid[row_check][column_check] == marker):
                        if [row_check, column_check] not in connected:
                            connected.append([row_check, column_check])
                        if positive:
                            row_check += pattern[0]
                            column_check += pattern[1]
                        else:
                            row_check -= pattern[0]
                            column_check -= pattern[1]
                    positive = False
                if len(connected) >= 4:
                    return True, self.player_number_to_marker[marker]
        return False, None

    def check_victory_new(self):
        """
        :return: True: if the game has been won; else: False
        """
        coordinates = [[0, 3], [1, 3], [2, 3], [3, 3], [4, 3], [5, 3], [2, 0], [2, 1], [2, 2], [2, 4], [2, 5], [2, 6]]

        for coordinate in coordinates:
            row = coordinate[0]
            col = coordinate[1]
            if self.grid[row][col] != self.empty_marker:
                marker = self.player_number_to_marker[self.grid[row][col]]

                # check horizontal
                if col + 3 < self.number_of_columns:
                    if self.grid[row][col] == self.grid[row][col + 1] == self.grid[row][col + 2] == self.grid[row][col + 3]:
                        return True, marker
                if col + 2 < self.number_of_columns and col - 1 >= 0:
                    if self.grid[row][col - 1] == self.grid[row][col] == self.grid[row][col + 1] == self.grid[row][col + 2]:
                        return True, marker
                if col + 1 < self.number_of_columns and col - 2 >= 0:
                    if self.grid[row][col - 2] == self.grid[row][col - 1] == self.grid[row][col] == self.grid[row][col + 1]:
                        return True, marker
                if col - 3 >= 0:
                    if self.grid[row][col - 3] == self.grid[row][col - 2] == self.grid[row][col - 1] == self.grid[row][col]:
                        return True, marker

                # check vertical
                if row + 3 < self.number_of_rows:
                    if self.grid[row][col] == self.grid[row + 1][col] == self.grid[row + 2][col] == self.grid[row + 3][col]:
                        return True, marker
                if row + 2 < self.number_of_rows and row - 1 >= 0:
                    if self.grid[row - 1][col] == self.grid[row][col] == self.grid[row + 1][col] == self.grid[row + 2][col]:
                        return True, marker
                if row + 1 < self.number_of_rows and row - 2 >= 0:
                    if self.grid[row - 2][col] == self.grid[row - 1][col] == self.grid[row][col] == self.grid[row + 1][col]:
                        return True, marker
                if row - 3 >= 0:
                    if self.grid[row - 3][col] == self.grid[row - 2][col] == self.grid[row - 1][col] == self.grid[row][col]:
                        return True, marker

                # check diagonal negative
                if col + 3 < self.number_of_columns and row + 3 < self.number_of_rows:
                    if self.grid[row][col] == self.grid[row + 1][col + 1] == self.grid[row + 2][col + 2] == self.grid[row + 3][col + 3]:
                        return True, marker
                if col + 2 < self.number_of_columns and col - 1 >= 0 and row + 2 < self.number_of_rows and row - 1 >= 0:
                    if self.grid[row - 1][col - 1] == self.grid[row][col] == self.grid[row + 1][col + 1] == self.grid[row + 2][col + 2]:
                        return True, marker
                if col + 1 < self.number_of_columns and col - 2 >= 0 and row + 1 < self.number_of_rows and row - 2 >= 0:
                    if self.grid[row - 2][col - 2] == self.grid[row - 1][col - 1] == self.grid[row][col] == self.grid[row + 1][col + 1]:
                        return True, marker
                if col - 3 >= 0 and row - 3 >= 0:
                    if self.grid[row - 3][col - 3] == self.grid[row - 2][col - 2] == self.grid[row - 1][col - 1] == self.grid[row][col]:
                        return True, marker

                # check diagonal positive
                if col + 3 < self.number_of_columns and row - 3 >= 0:
                    if self.grid[row - 3][col + 3] == self.grid[row - 2][col + 2] == self.grid[row - 1][col + 1] == self.grid[row][col]:
                        return True, marker
                if col + 2 < self.number_of_columns and col - 1 >= 0 and row + 1 < self.number_of_rows and row - 2 >= 0:
                    if self.grid[row - 2][col + 2] == self.grid[row - 1][col + 1] == self.grid[row][col] == self.grid[row + 1][col - 1]:
                        return True, marker
                if col + 1 < self.number_of_columns and col - 2 >= 0 and row + 2 < self.number_of_rows and row - 1 >= 0:
                    if self.grid[row - 1][col + 1] == self.grid[row][col] == self.grid[row + 1][col - 1] == self.grid[row + 2][col - 2]:
                        return True, marker
                if col - 3 >= 0 and row + 3 < self.number_of_rows:
                    if self.grid[row][col] == self.grid[row + 1][col - 1] == self.grid[row + 2][col - 2] == self.grid[row + 3][col - 3]:
                        return True, marker

        return False, None


if __name__ == '__main__':
    repetitions = 100000
    # test_grid = [
    #     [0, 0, 0, 1, 0, 0, 0],
    #     [0, 0, 0, 1, 0, 0, 0],
    #     [1, 1, 1, 1, 1, 1, 1],
    #     [1, 1, 1, 1, 1, 2, 1],
    #     [1, 1, 2, 1, 1, 2, 2],
    #     [2, 2, 1, 1, 2, 1, 1],
    # ]
    test_grid = [
        [0, 0, 0, 2, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [1, 2, 1, 2, 1, 2, 1],
        [0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 2, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
    ]

    a = Board(rows=6, columns=7, empty=0, player_1=1, player_2=2, robot='R')
    a.grid = deepcopy(test_grid)

    print("OLD:")
    start_time = time()
    for _ in range(repetitions):
        result = a.check_victory()
    end_time = time()
    print((end_time - start_time) / repetitions)

    print("NEW:")
    start_time = time()
    for _ in range(repetitions):
        result = a.check_victory_new()
    end_time = time()
    print((end_time - start_time) / repetitions)
