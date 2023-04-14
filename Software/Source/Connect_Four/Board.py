from time import process_time

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
    a = Board(rows=6, columns=7, empty=0, player_1=1, player_2=2, robot='R')

    a.grid = [
        [0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 2, 1],
        [1, 1, 2, 1, 1, 2, 2],
        [2, 2, 1, 1, 2, 1, 1],
    ]

    a.grid = [
        [1, 0, 0, 0, 0, 0, 1],
        [2, 0, 2, 0, 1, 2, 0],
        [1, 2, 2, 2, 0, 0, 2],
        [0, 0, 2, 2, 2, 0, 1],
        [0, 0, 0, 2, 0, 0, 0],
        [1, 2, 0, 0, 0, 1, 1]
    ]

    a.grid = [
        [0, 0, 0, 1, 0, 0, 2],
        [0, 0, 0, 0, 0, 2, 0],
        [1, 1, 2, 2, 2, 1, 1],
        [0, 0, 0, 2, 1, 0, 1],
        [0, 2, 2, 2, 1, 1, 0],
        [2, 2, 0, 1, 2, 1, 1]
    ]

    print(a.check_victory())

    start_time = process_time()
    for i in range(1000000):
        a.check_victory()
    elapsed_time = process_time() - start_time
    print(elapsed_time)
