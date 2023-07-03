from Board import Board
from Minimax import Minimax
from Validator import Validator
from AudioManager import AudioManager
from random import choice
from socket import socket, AF_INET, SOCK_STREAM


class Game:
    HOST = "127.0.0.1"
    PORT = 65431

    def __init__(self, rows=6, columns=7, empty=0, player_1=1, player_2=2, maximising_marker=2, minimising_marker=1):
        self.board = None
        self.minimax = None
        self.server = None
        self.client = None
        self.current_turn = None
        self.setup_socket()
        self.audio_manager = AudioManager()
        self.reset(rows, columns, empty, player_1, player_2, maximising_marker, minimising_marker)

    def reset(self, rows, columns, empty, player_1, player_2, maximising_marker, minimising_marker):
        self.board = Board(rows, columns, empty, player_1, player_2, 'R')
        self.minimax = Minimax(maximising_marker, minimising_marker, [rows, columns, empty, player_1, player_2, "R"])
        self.audio_manager.gg_occurred = False
        self.current_turn = None

    def setup_socket(self):
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.bind((self.HOST, self.PORT))
        print("Listening")

    def wait_for_client(self):
        self.server.listen()
        self.client, client_address = self.server.accept()
        print(client_address)

    def close_client(self):
        self.client.close()

    def close_socket(self):
        self.server.close()

    def send_message(self, message):
        self.client.sendall(message.encode())

    def receive_message(self):
        invalid_flag = True
        while invalid_flag:
            message = self.client.recv(7).decode()
            flag = message[:4]
            if flag != "COLM" or (flag == "COLM" and self.current_turn == 1):
                invalid_flag = False
            elif flag == "COLM":
                self.send_message("GAMEZNZ")
        character_one = message[4]
        if character_one == "Z":
            character_one = None
        character_two = message[5]
        if character_two == "Z":
            character_two = None
        character_three = message[6]
        if character_three == "Z":
            character_three = None
        return [flag, character_one, character_two, character_three]

    def execute_play(self, parameters):
        if int(parameters[0]) == 1:
            return True
        return False

    def execute_colm(self, parameters):
        column = int(parameters[0])
        valid_columns = self.board.get_valid_moves()
        if column in valid_columns:
            return column
        self.send_message("GAMEZNZ")
        return None

    def decode_message(self, message_code):
        message_codes = {
            "PLAY": self.execute_play,
            "COLM": self.execute_colm,
        }
        return message_codes.get(message_code)

    def print_board(self):
        print('   |   '.join([str(column) for column in [col for col in range(self.board.number_of_columns)]]))
        print("".join(['-' for _ in range(self.board.number_of_columns * 7)]))
        print('\n'.join(['       '.join(["\033[0;31m"+str(cell)+"\033[0m" if str(cell) == 'R' else "\033[0;32m"+str(cell)+"\033[0m" if str(cell) == '1' else str(cell) for cell in row]) for row in self.board.grid]))

    def make_player_move(self, player_number):
        """
        :param player_number: corresponds to numerical attribute of self.player[1, 2]_marker
        """
        column = None
        while column is None:
            message = self.receive_message()
            func = self.decode_message(message[0])
            column = func([message[1], message[2], message[3]])
        marker = self.board.player_number_to_marker[player_number]
        self.board.make_move(int(column), marker)
        self.send_message("GAME" + str(column) + "YZ")

    def make_robot_move(self):
        converted_board = self.minimax.convert_state(self.board.grid, self.board.robot_marker, 2)
        column, score = self.minimax.next_best_move(converted_board)
        print(score)
        if score < self.audio_manager.umm_threshold:
            self.audio_manager.play_umm()
        marker = self.board.player_number_to_marker["R"]
        self.board.make_move(column, marker)
        self.send_message("GAME" + str(column) + "YZ")

    def play_game(self):
        play_again = True

        self.wait_for_client()
        self.audio_manager.play_hello_i_am_handy()
        self.audio_manager.play_play_connect_four()
        while play_again:
            message = self.receive_message()
            funct = self.decode_message(message[0])
            p1_first_play = funct([message[1], message[2], message[3]])

            self.audio_manager.play_kennedy_plays_red()

            p1_first_play = int(p1_first_play)
            self.current_turn = p1_first_play
            self.audio_manager.play_ready()

            while not self.board.check_victory()[0] and (len(self.board.get_valid_moves()) > 0):
                self.send_message("STAT" + str(self.current_turn) + "NZ")

                self.print_board()
                print("")

                if self.current_turn == 1:
                    print("Player 1 turn:")
                    self.minimax.current_moves += 1
                    self.audio_manager.play_its_your_move()
                    self.make_player_move(1)
                    self.current_turn = 0

                elif self.current_turn == 0:
                    print("Robot turn:")
                    choice([self.audio_manager.play_hmm, self.audio_manager.play_hmm2])()
                    self.make_robot_move()
                    self.minimax.current_moves += 1
                    self.current_turn = 1

                else:
                    print("Error")

                if self.minimax.current_moves > (self.audio_manager.fraction_for_gg * 42) and \
                        not self.audio_manager.gg_occurred:
                    self.audio_manager.play_gg()

            self.print_board()

            winner = not self.current_turn
            self.audio_manager.play_game_over()
            self.send_message("STAT" + str(int(winner)) + "YZ")

            if not self.board.get_valid_moves() and not self.board.check_victory()[0]:
                print("Draw")
                self.audio_manager.play_tie()
            elif winner:
                self.audio_manager.play_well_played()
                print("Player 1 wins")
                self.audio_manager.play_kennedy_loses()
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
            self.close_client()

            self.audio_manager.play_rematch()
            play_again = input("Play again: \n 1 for yes \n 0 for no\n")
            while not Validator(play_again).option_validator(["0", "1"]):
                play_again = input("Error. Please input 1 or 0.\nPlay again: \n 1 for yes \n 0 for no\n")
            play_again = bool(int(play_again))
            if play_again:
                self.wait_for_client()

        self.close_socket()
