from Board import Board
from Validator import Validator
from Minimax import Minimax
from AudioManager import AudioManager
from random import randint


class Game:
    def __init__(self, rows=4, columns=5, empty=0, player_1=1, player_2=2, maximising_marker='R', minimising_marker=1):
        self.board = Board(rows, columns, empty, player_1, player_2, 'R')
        self.minimax = Minimax(maximising_marker, minimising_marker, [rows, columns, empty, player_1, player_2, "R"])
        self.is_maximising = True
        self.audio_manager = AudioManager()

    def print_board(self):
        print('   |   '.join([str(column) for column in [col for col in range(self.board.number_of_columns)]]))
        print("".join(['-' for _ in range(self.board.number_of_columns * 5)]))
        print('\n'.join(['       '.join(["\033[0;31m"+str(cell)+"\033[0m" if str(cell) == 'R' else "\033[0;32m"+str(cell)+"\033[0m" if str(cell) == '1' else str(cell) for cell in row]) for row in self.board.grid]))

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
        is_player_game = 0
        p1_first_play = 0

        current_turn = p1_first_play

        if p1_first_play == 0:
            print(self.minimax.storage_function.directory_name)
            self.minimax.storage_function.directory_name += "Player1"   # player 1 is robot player
        else:
            self.minimax.storage_function.directory_name += "Player2"

        self.minimax.files_line_count = self.minimax.storage_function.update_file_line_count()

        self.audio_manager.play_play_connect_three()
        self.audio_manager.play_galbiati_plays_red()

        while not self.board.check_victory()[0] and (len(self.board.get_valid_moves()) > 0):
            self.print_board()
            print("")

            if current_turn == 1:
                if randint(1, 100) < 35:
                    self.audio_manager.play_its_your_move()
                print("Player 1 turn:")
                self.make_player_move(1)
                current_turn = 0
                if randint(1, 100) < 20:
                    self.audio_manager.play_lol_really()

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
            self.audio_manager.play_tie()

        elif winner:
            print("Player 1 wins")
            self.audio_manager.play_galbiati_loses()

        else:
            print("Robot wins")
            self.audio_manager.play_galbiati_wins()
            self.audio_manager.play_loser()
            self.audio_manager.play_pathetic_humans()

    def play_game(self):
        play = "1"
        self.minimax.current_line = 1
        self.minimax.last_line = 0
        self.minimax.current_depth = 1
        self.audio_manager.play_hello_i_am_riccardino()

        while play == "1":
            self.board = Board(4, 5, 0, 1, 2, 'R')
            self.minimax = Minimax("R", 1, [4, 5, 0, 1, 2, "R"])
            self.game_interface()

            play = input("Play again: \n 1 for yes \n 0 for no\n")
            while play != "0" and play != "1":
                play = input("\nWould you like to play again?\n"
                             "1 yes\n"
                             "0 no \n")

        print("Thanks for playing!")


if __name__ == '__main__':
    game = Game()
    game.play_game()
