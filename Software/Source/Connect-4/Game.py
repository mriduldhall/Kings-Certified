from Board import Board
import random


class Game:
    def __init__(self, rows=6, columns=7, empty=0, player_1=1, player_2=2):
        self.board = Board(rows, columns, empty, player_1, player_2, "R")

    def input_validation(self, user_input, data_type):
        try:
            data_type(user_input)
            return True
        except ValueError:
            return False

    # Arya/Shenglun
    # Prints the board in its current status
    def print_board(self):
        print('   |   '.join([str(column) for column in [col for col in range(self.board.number_of_columns)]]))
        print("".join(['-' for i in range(self.board.number_of_columns*7)]))
        print('\n'.join(['       '.join([str(cell) for cell in row]) for row in self.board.grid]))

    # Shenglun
    # Allows a human player to make a move when given the player number who is about to make a move
    def make_player_move(self, player_number):
        """
        :param player_number: corresponds to numerical attribute of self.player[1, 2]_marker
        """
        max_column = self.board.number_of_columns - 1

        column = (input(f"Enter column (0 - {max_column}): "))  # Validator
        marker = self.board.player_number_to_marker[player_number]

        while not self.input_validation(column, int) or (int(column) not in self.board.get_valid_moves()):
            print("Invalid move.")
            column = input(f"Enter column (0 - {max_column}): ")

        self.board.make_move(int(column), marker)
        self.print_board()

    # Shenglun
    # Allows the robot to make a move
    def make_robot_move(self):
        column = random.choice(self.board.get_valid_moves())
        marker = self.board.player_number_to_marker["R"]
        self.board.make_move(column, marker)
        self.print_board()

    # Arya
    # Allows user to choose if they want PvP or PvR and then calls other methods as needed to make moves
    def play_game(self):
        pass
