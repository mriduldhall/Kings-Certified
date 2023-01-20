from Board import Board
import random


class Game:
    def __init__(self, rows=6, columns=7, empty=0, player_1=1, player_2=2):
        self.board = Board(rows, columns, empty, player_1, player_2, "R")

    def input_validation(self, user_input, data_type):
        """
        :param user_input: the value to be checked
        :param data_type: the data type to compare the checked value with
        :return: true or false if the value have the corresponding data type
        """
        try:
            data_type(user_input)
            return True
        except ValueError:
            return False

    # Arya/Shenglun
    # Prints the board in its current status
    def print_board(self):
        print('   |   '.join([str(column) for column in [col for col in range(self.board.number_of_columns)]]))
        print("".join(['-' for _ in range(self.board.number_of_columns * 7)]))
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

    # Shenglun
    # Allows the robot to make a move
    def make_robot_move(self):
        column = random.choice(self.board.get_valid_moves())
        marker = self.board.player_number_to_marker["R"]
        self.board.make_move(column, marker)

    # Arya
    # Allows user to choose if they want PvP or PvR and then calls other methods as needed to make moves
    def play_game(self):
        """
        is_player_game  - binary value for if game is between robot and player or player and player
        p1_first_play   - binary value for if the first go is player 1 or not player 1
        current_turn    - binary value for if the next player is player 1 or not player 1
                          if it is not player 1 then is_player_game is used to determine the next turn
        winner          - binary value for the last players turn
                          if not player 1 then is_player_game is used to determine winner
        """
        is_player_game = input("Play against Robot or another Player: \n 1 for player \n 0 for robot\n")
        # input validation
        while not (str(is_player_game) == "0" or str(is_player_game) == "1"):
            is_player_game = input("Error. Please input 1 or 0. \n"
                                   "Play against Robot or another Player: \n"
                                   " 1 for player \n 0 for robot\n")

        p1_first_play = input("Who plays first? \n 1 - I start first \n 0 - Opponent starts\n")
        # input validation
        while not (str(p1_first_play) == "0" or str(p1_first_play) == "1"):
            p1_first_play = input("Error. Please input 1 or 0. \n"
                                  "Who plays first: \n"
                                  " 1 - I start first \n 0 - Opponent starts\n")

        is_player_game = int(is_player_game)
        p1_first_play = int(p1_first_play)
        current_turn = p1_first_play

        # looping through the turns
        while not int(input("Has someone won yet? 1/0")):
            """not Board.check_victory(victory)"""
            self.print_board()

            if current_turn == 1:
                print("Player 1 turn:")
                self.make_player_move(1)
                self.print_board()
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

        winner = not current_turn
        if winner:
            print("Player 1 wins")
        elif is_player_game:
            print("Player 2 wins")
        else:
            print("Robot wins")


current_game = Game(6, 7, " ", 1, 2)
Game.play_game(current_game)
