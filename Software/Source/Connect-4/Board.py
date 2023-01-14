class Board:
    def __init__(self, rows, columns, empty, player_1, player_2):
        self.number_of_rows = rows
        self.number_of_columns = columns
        self.empty_marker = empty
        self.player_1_marker = player_1
        self.player_2_marker = player_2
        self.player_number_to_marker = {
            "1": self.player_1_marker,
            "2": self.player_2_marker,
        }
        self.grid = [
            [
                self.empty_marker for _ in range(self.number_of_columns)
            ] for _ in range(self.number_of_rows)
        ]

    # Haroon
    # Returns a list of all valid columns where moves can be made
    def get_valid_moves(self):
        pass

    # Haroon
    # Makes a move when given column and player number
    def make_move(self, column_number, player_number):
        pass

    # Mridul
    # Checks if game is over and returns player number if won or False if game is still ongoing
    def check_victory(self):
        pass
