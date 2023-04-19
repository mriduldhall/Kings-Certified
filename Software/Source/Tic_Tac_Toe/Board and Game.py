from random import choice


class TicTacToe:
    def __init__(self, init_board=None):
        self.empty_marker = "0"
        self.player_1_marker = "X"
        self.player_2_marker = "O"
        self.robot_marker = "R"
        self.player_number_to_marker = {
            1: self.player_1_marker,
            2: self.player_2_marker,
            "R": self.robot_marker
        }

        self.player_marker_to_number = {
            self.player_1_marker: 1,
            self.player_2_marker: 2,
            self.robot_marker: "R"
        }

        if not init_board:
            self.board = [[self.empty_marker for columns in range(3)] for rows in range(3)]
        else:
            self.board = init_board

    def print_board(self):
        print("")
        for row in range(len(self.board)):
            print(self.board[row])

    def get_valid_moves(self):
        available_spaces = []
        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                if self.board[row][column] == self.empty_marker:
                    available_spaces.append((str(row), str(column)))

        return available_spaces

    def make_move(self, place_coord, player_marker):
        row, column = place_coord
        self.board[int(row)][int(column)] = player_marker

    def check_victory(self):
        # check rows
        for row in self.board:
            if row[0] == row[1] == row[2] != self.empty_marker:
                print("1")
                return True, self.player_marker_to_number[row[0]]

        # check columns
        for columns in range(len(self.board)):
            column = [self.board[0][columns], self.board[1][columns], self.board[2][columns]]
            if column[0] == column[1] == column[2] != self.empty_marker:
                print("2")
                return True, self.player_marker_to_number[column[0]]

        # check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != self.empty_marker:
            print("3")
            return True, self.player_marker_to_number[self.board[0][0]]

        if self.board[0][2] == self.board[1][1] == self.board[2][0] != self.empty_marker:
            print("4")
            return True, self.player_marker_to_number[self.board[0][2]]

        return False, None

    def make_player_move(self, player_number):
        column = str(input(f"Enter column (0 - 2): "))
        row = str(input(f"Enter row (0 - 2): "))

        marker = self.player_number_to_marker[player_number]
        positions = ["0", "1", "2"]
        print(self.get_valid_moves())
        while row not in positions or column not in positions or (row, column) not in self.get_valid_moves():
            print("Invalid move.")
            column = (input(f"Enter column (0 - 2): "))
            row = (input(f"Enter row (0 - 2): "))

        self.make_move((int(row), int(column)), marker)

    def make_robot_move(self):
        self.make_move(choice(self.get_valid_moves()), "R")

    def play_game(self):
        is_player_game = input("Play against Robot or another Player: \n 1 for player \n 0 for robot\n")
        while is_player_game != "0" and is_player_game != "1":
            is_player_game = input("Error. Please input 1 or 0. \n"
                                   "Play against Robot or another Player: \n"
                                   " 1 for player \n 0 for robot\n")

        print("")

        p1_first_play = input("Who plays first? \n 1 - I start first \n 0 - Opponent starts\n")
        while p1_first_play != "0" and p1_first_play != "1":
            p1_first_play = input("Error. Please input 1 or 0. \n"
                                  "Who plays first: \n"
                                  " 1 - I start first \n 0 - Opponent starts\n")

        print("")

        is_player_game = int(is_player_game)
        p1_first_play = int(p1_first_play)
        current_turn = p1_first_play
        while not self.check_victory()[0] and len(self.get_valid_moves()) > 0:
            self.print_board()
            print("")

            if current_turn == 1:
                print("Player 1 turn: ")
                self.make_player_move(1)
                current_turn = 0

            elif current_turn == 0 and is_player_game:
                print("Player 2 turn: ")
                self.make_player_move(2)
                current_turn = 1

            elif current_turn == 0 and not is_player_game:
                print("Robot turn: ")
                self.make_robot_move()
                current_turn = 1

            else:
                print("Error")

        winner = not current_turn

        if not self.get_valid_moves() and not self.check_victory()[0]:
            print("Draw")
        elif winner:
            print("Player 1 wins")
        elif is_player_game:
            print("Player 2 wins")
        else:
            print("Robot wins")


if __name__ == "__main__":
    a = TicTacToe()

    # a.board = [
    #     ["O", 0, "O"],
    #     ["X", "X", 0],
    #     ["O", 0, "X"]
    # ]

    a.print_board()
    print(a.get_valid_moves())
    print(a.check_victory())
    a.play_game()
