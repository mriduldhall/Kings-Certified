from Board import Board
from Minimax import Minimax
from Validator import Validator
from AudioManager import AudioManager
from random import choice


class Game:
    def __init__(self, rows=6, columns=7, empty=0, player_1=1, player_2=2, maximising_marker=2, minimising_marker=1):
        self.board = None
        self.minimax = None
        self.audio_manager = AudioManager()
        self.reset(rows, columns, empty, player_1, player_2, maximising_marker, minimising_marker)

    def reset(self, rows, columns, empty, player_1, player_2, maximising_marker, minimising_marker):
        self.board = Board(rows, columns, empty, player_1, player_2, 'R')
        self.minimax = Minimax(maximising_marker, minimising_marker, [rows, columns, empty, player_1, player_2, "R"])
        self.audio_manager.gg_occurred = False

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
        converted_board = self.minimax.convert_state(self.board.grid, self.board.robot_marker, 2)
        column, score = self.minimax.next_best_move(converted_board)
        print(score)
        if score < self.audio_manager.umm_threshold:
            self.audio_manager.play_umm()
        marker = self.board.player_number_to_marker["R"]
        self.board.make_move(column, marker)

    def play_game(self):
        play_again = True

        self.audio_manager.play_play_connect_four()
        while play_again:

            self.audio_manager.play_instructions_question()
            instructions = input("Hear instructions: \n 1 for yes \n 0 for no\n")
            while not Validator(instructions).option_validator(["0", "1"]):
                instructions = input("Error. Please input 1 or 0.\nHear instructions: \n 1 for yes \n 0 for no\n")

            instructions = bool(int(instructions))
            if instructions:
                self.audio_manager.play_connect_four_explain_setup()
                self.audio_manager.play_connect_four_explain_tokens_setup()
                self.audio_manager.play_connect_four_explain_objective()
                self.audio_manager.play_connect_four_explain_play()
                self.audio_manager.play_connect_four_explain_winning()
                self.audio_manager.play_connect_four_explain_ending()

            print("")

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

            if is_player_game == "0":
                self.audio_manager.play_kennedy_plays_red()

            print("")

            is_player_game = int(is_player_game)
            p1_first_play = int(p1_first_play)
            current_turn = p1_first_play
            self.audio_manager.play_ready()

            while not self.board.check_victory()[0] and (len(self.board.get_valid_moves()) > 0):
                self.print_board()
                print("")

                if current_turn == 1:
                    print("Player 1 turn:")
                    if not is_player_game:
                        self.minimax.current_moves += 1
                        self.audio_manager.play_its_your_move()
                    self.make_player_move(1)
                    current_turn = 0

                elif current_turn == 0 and is_player_game:
                    print("Player 2 turn:")
                    self.make_player_move(2)
                    current_turn = 1

                elif current_turn == 0 and not is_player_game:
                    print("Robot turn:")
                    choice([self.audio_manager.play_hmm, self.audio_manager.play_hmm2])()
                    self.make_robot_move()
                    self.minimax.current_moves += 1
                    current_turn = 1

                else:
                    print("Error")

                if self.minimax.current_moves > (self.audio_manager.fraction_for_gg * 42) and \
                        not self.audio_manager.gg_occurred:
                    self.audio_manager.play_gg()

            self.print_board()

            winner = not current_turn
            self.audio_manager.play_game_over()

            if not self.board.get_valid_moves() and not self.board.check_victory()[0]:
                print("Draw")
                self.audio_manager.play_tie()
            elif winner:
                self.audio_manager.play_well_played()
                print("Player 1 wins")
                if not is_player_game:
                    self.audio_manager.play_kennedy_loses()
            elif is_player_game:
                print("Player 2 wins")
            else:
                choice([self.audio_manager.play_kennedy_wins, self.audio_manager.play_robot_overlord_kennedy])()
                print("Robot wins")
                self.audio_manager.play_loser()

            self.reset(
                self.board.number_of_rows,
                self.board.number_of_columns,
                self.board.empty_marker,
                self.board.player_1_marker,
                self.board.player_2_marker,
                self.minimax.maximising_marker,
                self.minimax.minimising_marker,
            )

            self.audio_manager.play_rematch()
            play_again = input("Play again: \n 1 for yes \n 0 for no\n")
            while not Validator(play_again).option_validator(["0", "1"]):
                play_again = input("Error. Please input 1 or 0.\nPlay again: \n 1 for yes \n 0 for no\n")
            play_again = bool(int(play_again))
