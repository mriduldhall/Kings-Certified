import time
# The file only contains the valid_move() and make_move() methods.


class Game:
    def __init__(self):
        self.row = 5
        self.column = 6
        # These can be changed later to more appropriate value
        self.empty_position = 0
        self.player1_marker = 1
        self.player2_marker = 2
        self.board = [[self.empty_position for _ in range(self.column)] for _ in range(self.row)]

    def valid_move(self):
        """
        :return: list with the index of columns where move is available.
        """
        num_of_columns = len(self.board[0])
        columns_available = []
        for column in range(num_of_columns):
            if self.board[0][column] == self.empty_position:
                columns_available.append(column)
        return columns_available

    # This algorithm starts from the top
    def make_move(self, column, marker):
        """
        :param column: (computer) index of the column you want to make move in
        :param marker: the player mark you want to put in that column
        :return: True: if the move made successfully; else: False
        """
        assert column in self.valid_move(), 'Move Request Should Be Valid!'
        move_made = False
        row = 1
        while not move_made:
            if self.board[row][column] != self.empty_position:
                self.board[row-1][column] = marker
                move_made = True
            elif row == len(self.board) - 1:
                self.board[row][column] = marker
                move_made = True
            row += 1

        # for debugging purposes to make sure move was made correctly
        assert move_made, f'error while making the move in {column} column for {marker}'

        return move_made

    # This algorithm starts from the middle and goes up and down.
    def make_move_v2(self, column, marker):
        """
        :param column: (computer) index of the column you want to make move in
        :param marker: the player mark you want to put in that column
        :return: True: if the move made successfully; else: False
        """
        assert column in self.valid_move(), 'Move Request Should Be Valid!'

        board_row_size = self.row - 1
        row = board_row_size // 2
        made_move, ascending = False, False
        while not made_move:
            if self.board[row][column] != self.empty_position:
                row -= 1
                ascending = True
            elif self.board[row][column] == self.empty_position and row < board_row_size and not ascending:
                row += 1
            else:
                self.board[row][column] = marker
                made_move = True

        # for debugging purposes to make sure move was made correctly
        assert made_move, f'error while making the move in {column} column for {marker}'

        return made_move


a = Game()
# Random Board state to check if the methods were working as intended.
a.board = [[0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0],
           ['X', 0, 0, 0, 0, 0],
           ['X', 0, 0, 0, 0, 'X'],
           ['X', 0, 0, 0, 0, 'X']]

# Tests for the algorithms
start1 = time.time()
a.make_move(1, a.player1_marker)
a.make_move(2, a.player1_marker)
a.make_move(3, a.player1_marker)

a.make_move(1, a.player1_marker)
a.make_move(2, a.player1_marker)
a.make_move(3, a.player1_marker)
end1 = time.time()

a.board = [[0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0],
           ['X', 0, 0, 0, 0, 0],
           ['X', 0, 0, 0, 0, 'X'],
           ['X', 0, 0, 0, 0, 'X']]

start2 = time.time()
a.make_move_v2(1, a.player1_marker)
a.make_move_v2(2, a.player1_marker)
a.make_move_v2(3, a.player1_marker)

a.make_move_v2(1, a.player1_marker)
a.make_move_v2(2, a.player1_marker)
a.make_move_v2(3, a.player1_marker)
end2 = time.time()

print(f'Algorithm 1: {end1-start1}')
print(f'Algorithm 2: {end2-start2}')


# Pretty print of the board in terminal for debugging purposes
print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in a.board]))



