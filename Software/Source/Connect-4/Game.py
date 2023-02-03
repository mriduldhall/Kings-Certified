from Board import Board
from Validator import Validator
from random import choice


class Game:
    def __init__(self, rows=6, columns=7, empty=0, player_1=1, player_2=2):
        self.board = Board(rows, columns, empty, player_1, player_2, "R")

    def print_board(self):
        print('   |   '.join([str(column) for column in [col for col in range(self.board.number_of_columns)]]))
        print("".join(['-' for _ in range(self.board.number_of_columns * 7)]))
        print('\n'.join(['       '.join([str(cell) for cell in row]) for row in self.board.grid]))

    def make_player_move(self, player_number):
        """
        :param player_number: corresponds to numerical attribute of self.player[1, 2]_marker
        """
        max_column = self.board.number_of_columns - 1

        column = (input(f"Enter column (0 - {max_column}): "))
        marker = self.board.player_number_to_marker[player_number]

        while not Validator(column).type_validation(int) or (int(column) not in self.board.get_valid_moves()):
            print("Invalid move.")
            column = input(f"Enter column (0 - {max_column}): ")

        self.board.make_move(int(column), marker)

    def make_robot_move(self):
        column = choice(self.board.get_valid_moves())
        marker = self.board.player_number_to_marker["R"]
        self.board.make_move(column, marker)

    def play_game(self):
        is_player_game = input("Play against Robot or another Player: \n 1 for player \n 0 for robot\n")
        while not Validator(is_player_game).option_validator(["0", "1"]):
            is_player_game = input("Error. Please input 1 or 0. \n"
                                   "Play against Robot or another Player: \n"
                                   " 1 for player \n 0 for robot\n")

        print("")

        p1_first_play = input("Who plays first? \n 1 - I start first \n 0 - Opponent starts\n")
        while not Validator(p1_first_play).option_validator(["0", "1"]):
            p1_first_play = input("Error. Please input 1 or 0. \n"
                                  "Who plays first: \n"
                                  " 1 - I start first \n 0 - Opponent starts\n")

        print("")

        is_player_game = int(is_player_game)
        p1_first_play = int(p1_first_play)
        current_turn = p1_first_play

        while not self.board.check_victory() and (len(self.board.get_valid_moves()) > 0):
            self.print_board()
            print("")

            if current_turn == 1:
                print("Player 1 turn:")
                self.make_player_move(1)
                current_turn = 0

            elif current_turn == 0 and is_player_game:
                print("Player 2 turn:")
                self.make_player_move(2)
                current_turn = 1

            elif current_turn == 0 and not is_player_game:
                print("Robot turn:")
                self.make_robot_move()
                current_turn = 1

            else:
                print("Error")

        self.print_board()

        winner = not current_turn

        if not self.board.get_valid_moves() and not self.board.check_victory():
            print("Draw")
        elif winner:
            print("Player 1 wins")
        elif is_player_game:
            print("Player 2 wins")
        else:
            print("Robot wins")


if __name__ == '__main__':
    Game().play_game()
