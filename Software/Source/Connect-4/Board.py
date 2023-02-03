from Validator import Validator


class Board:
    def __init__(self, rows, columns, empty, player_1, player_2, robot):
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
        self.grid = [[self.empty_marker for _ in range(self.number_of_columns)] for _ in range(self.number_of_rows)]

    def get_valid_moves(self):
        """
        :return: columns_available: list with the index of columns where move is available.
        """
        columns_available = []
        for column in range(self.number_of_columns):
            if self.grid[0][column] == self.empty_marker:
                columns_available.append(column)
        return columns_available

    def make_move(self, column_number, player_marker):
        """
        :param column_number: (computer) index of the column you want to make move in
        :param player_marker: the player mark you want to put in that column
        :return: True: if the move made successfully; else: False
        """
        assert column_number in self.get_valid_moves(), 'Move Request Should Be Valid!'

        grid_row_size = self.number_of_rows - 1
        row = grid_row_size // 2
        made_move, ascending = False, False
        while not made_move:
            if self.grid[row][column_number] != self.empty_marker:
                row -= 1
                ascending = True
            elif self.grid[row][column_number] == self.empty_marker and row < grid_row_size and not ascending:
                row += 1
            else:
                self.grid[row][column_number] = player_marker
                made_move = True

        assert made_move, f'error while making the move in {column_number} column for {player_marker}'

        return made_move

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
                    return True
        return False
