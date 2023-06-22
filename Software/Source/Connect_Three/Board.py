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

    def get_valid_moves(self):
        columns_available = []
        for column in range(self.number_of_columns):
            if self.grid[0][column] == self.empty_marker:
                columns_available.append(column)
        return columns_available

    def make_move(self, column_number, player_marker):
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
        coordinates = [[2, 0], [2, 1], [2, 2], [2, 3], [2, 4], [0, 2], [1, 2], [2, 2], [3, 2]]

        for coordinate in coordinates:
            row = coordinate[0]
            col = coordinate[1]
            mid_col = 2
            end_col = self.number_of_columns - 1
            mid_row = 2
            end_row = self.number_of_rows - 1

            if self.grid[row][col] != self.empty_marker:
                marker = self.player_number_to_marker[self.grid[row][col]]

                # check horizontal
                if end_col >= col >= mid_col:
                    if self.grid[row][col] == self.grid[row][col - 1] == self.grid[row][col - 2]:
                        return True, marker
                if end_col - 1 >= col >= mid_col - 1:
                    if self.grid[row][col - 1] == self.grid[row][col] == self.grid[row][col + 1]:
                        return True, marker
                if mid_col >= col >= 0:
                    if self.grid[row][col + 2] == self.grid[row][col + 1] == self.grid[row][col]:
                        return True, marker

                # check vertical
                if end_row >= row >= mid_row:
                    if self.grid[row][col] == self.grid[row - 1][col] == self.grid[row - 2][col]:
                        return True, marker
                if end_row - 1 >= row >= mid_row - 1:
                    if self.grid[row - 1][col] == self.grid[row][col] == self.grid[row + 1][col]:
                        return True, marker
                if mid_row - 1 >= row >= 0:
                    if self.grid[row + 2][col] == self.grid[row + 1][col] == self.grid[row][col]:
                        return True, marker

                # check diagonal negative
                if mid_col >= col >= 0 and mid_row > row >= 0:
                    if self.grid[row + 2][col + 2] == self.grid[row + 1][col + 2] == self.grid[row][col]:
                        return True, marker
                if end_col - 1 >= col >= mid_col - 1 and end_row - 1 >= row >= mid_row - 1:
                    if self.grid[row + 1][col + 1] == self.grid[row][col] == self.grid[row - 1][col - 1]:
                        return True, marker
                if end_col >= col >= mid_col and end_row >= row >= mid_row:
                    if self.grid[row - 2][col - 2] == self.grid[row - 1][col - 1] == self.grid[row][col]:
                        return True, marker

                # check diagonal positive
                if mid_col >= col >= 0 and end_row >= row >= mid_row:
                    if self.grid[row - 2][col + 2] == self.grid[row - 1][col + 1] == self.grid[row][col]:
                        return True, marker
                if end_col - 1 >= col >= mid_col - 1 and end_row - 1 >= row >= mid_row - 1:
                    if self.grid[row - 1][col + 1] == self.grid[row][col] == self.grid[row + 1][col - 1]:
                        return True, marker
                if end_col >= col >= mid_col and mid_row > row >= 0:
                    if self.grid[row + 2][col - 2] == self.grid[row + 1][col - 1] == self.grid[row][col]:
                        return True, marker

        return False, None
