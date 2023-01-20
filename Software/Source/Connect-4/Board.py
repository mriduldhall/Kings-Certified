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
        self.grid = [
            [
                self.empty_marker for _ in range(self.number_of_columns)
            ] for _ in range(self.number_of_rows)
        ]

    # Haroon
    # Returns a list of all valid columns where moves can be made
    def get_valid_moves(self):
        """
        :return: columns_available: list with the index of columns where move is available.
        """
        columns_available = []
        for column in range(self.number_of_columns):
            if self.grid[0][column] == self.empty_marker:
                columns_available.append(column)
        return columns_available

    # Haroon
    # Makes a move when given column and player number
    def make_move(self, column_number, player_marker):
        """
        :param column_number: (computer) index of the column you want to make move in
        :param player_marker: the player mark you want to put in that column
        :return: True: if the move made successfully; else: False
        """
        assert column_number in self.get_valid_moves(), 'Move Request Should Be Valid!'

        grid_row_size = self.number_of_rows - 1  # Computer based indexing
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

        # for debugging purposes to make sure move was made correctly
        assert made_move, f'error while making the move in {column_number} column for {player_marker}'

        return made_move

    # Mridul
    # Checks if game is over and returns player number if won or False if game is still ongoing
    def check_victory(self):
        pass