from Board import Board
from Validator import Validator
from Minimax import Minimax


class Game:
    def __init__(self, rows=4, columns=5, empty=0, player_1=1, player_2=2, maximising_marker='R', minimising_marker=1):
        self.board = Board(rows, columns, empty, player_1, player_2, 'R')
        self.minimax = Minimax(maximising_marker, minimising_marker, [rows, columns, empty, player_1, player_2, "R"])
        self.is_maximising = True

    def print_board(self):
        print('   |   '.join([str(column) for column in [col for col in range(self.board.number_of_columns)]]))
        print("".join(['-' for _ in range(self.board.number_of_columns * 5)]))
        print('\n'.join(['       '.join([str(cell) for cell in row]) for row in self.board.grid]))

    def make_player_move(self, player_number):
        max_column = self.board.number_of_columns - 1
        column = (input(f"Enter column (0 - {max_column}): "))
        marker = self.board.player_number_to_marker[player_number]
        while not Validator(column).type_validation(int) or (int(column) not in self.board.get_valid_moves()):
            print("Invalid move.")
            column = input(f"Enter column (0 - {max_column}): ")
        self.board.make_move(int(column), marker)
        self.minimax.follow_move(int(column))

    def make_robot_move(self):
        column = self.minimax.next_best_move(self.is_maximising)
        marker = self.board.player_number_to_marker["R"]
        self.board.make_move(column, marker)
        self.minimax.follow_move(column)

    def game_interface(self):
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

        if p1_first_play == 0:
            print(self.minimax.storage_function.directory_name)
            self.minimax.storage_function.directory_name += "Player1"   # player 1 is robot player
        else:
            self.minimax.storage_function.directory_name += "Player2"

        self.minimax.files_line_count = self.minimax.storage_function.update_file_line_count()

        while not self.board.check_victory()[0] and (len(self.board.get_valid_moves()) > 0):
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

        if not self.board.get_valid_moves() and not self.board.check_victory()[0]:
            print("Draw")
        elif winner:
            print("Player 1 wins")
        elif is_player_game:
            print("Player 2 wins")
        else:
            print("Robot wins")

    def play_game(self):
        play = "1"
        self.minimax.current_line = 1
        self.minimax.last_line = 0
        self.minimax.current_depth = 1

        while play == "1":
            self.board.grid = [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]

            # self.board.grid = [
            #         [1, 0, 0, 0, 0],
            #         ["R", 0, 0, 0, 0],
            #         [1, 0, 0, 0, 0],
            #         ["R", 0, 0, 0, 0]
            # ]
            print("Grid: ", self.board.grid)
            self.game_interface()

            play = input("Play again: \n 1 for yes \n 0 for no\n")
            while play != "0" and play != "1":
                play = input("\nWould you like to play again?\n"
                             "1 yes\n"
                             "0 no \n")

        print("Thanks for playing!")


if __name__ == '__main__':
    while True:
        game = Game()
        # print("Grid: ", game.board.grid)
    #     game.board.grid = [
    #     [0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0]
    # ]
    #     game.board.grid = [
    #     [0, 0, 0, 0, 0],
    #     [1, 0, 0, "R", 1],
    #     ["R", 1, "R", 1, "R"],
    #     [1, 1, "R", 1, "R"]
    # ]
        game.play_game()
        # game.minimax.current_node = game.minimax.tree
