from Board import Board
from Minimax import Minimax
from socket import socket, AF_INET, SOCK_STREAM
from AudioManager import AudioManager
from random import randint

class Game:
    HOST = "127.0.0.1"
    PORT = 65431

    def __init__(self, rows=4, columns=5, empty=0, player_1=1, player_2=2, maximising_marker='R', minimising_marker=1):
        self.board = None
        self.minimax = None
        self.is_maximising = None
        self.current_turn = None
        self.server = None
        self.client = None
        self.setup_socket()
        self.audio_manager = AudioManager()
        self.reset(rows, columns, empty, player_1, player_2, maximising_marker, minimising_marker)

    def reset(self, rows, columns, empty, player_1, player_2, maximising_marker, minimising_marker):
        self.board = Board(rows, columns, empty, player_1, player_2, 'R')
        self.minimax = Minimax(maximising_marker, minimising_marker, [rows, columns, empty, player_1, player_2, "R"])
        self.is_maximising = True
        self.minimax.current_line = 1
        self.minimax.last_line = 0
        self.minimax.current_depth = 1
        self.audio_manager.gg_occurred = False

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
            message = self.client.recv(11).decode()
            message = message[4:]
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
        print("".join(['-' for _ in range(self.board.number_of_columns * 5)]))
        print('\n'.join(['       '.join(["\033[0;31m"+str(cell)+"\033[0m" if str(cell) == 'R' else "\033[0;32m"+str(cell)+"\033[0m" if str(cell) == '1' else str(cell) for cell in row]) for row in self.board.grid]))

    def make_player_move(self, player_number):
        column = None
        while column is None:
            message = self.receive_message()
            func = self.decode_message(message[0])
            column = func([message[1], message[2], message[3]])
        marker = self.board.player_number_to_marker[player_number]
        self.board.make_move(int(column), marker)
        self.minimax.follow_move(int(column))
        self.send_message("GAME" + str(column) + "YZ")

    def make_robot_move(self):
        column = self.minimax.next_best_move(self.is_maximising)
        marker = self.board.player_number_to_marker["R"]
        self.board.make_move(column, marker)
        self.minimax.follow_move(column)
        self.send_message("GAME" + str(column) + "YZ")

    def game_interface(self):
        message = self.receive_message()
        funct = self.decode_message(message[0])
        p1_first_play = funct([message[1], message[2], message[3]])

        p1_first_play = int(p1_first_play)
        self.current_turn = p1_first_play

        self.minimax.storage_function.directory_name += "Player1"

        self.minimax.files_line_count = self.minimax.storage_function.update_file_line_count()

        self.audio_manager.play_play_connect_three()
        self.audio_manager.play_galbiati_plays_red()

        while not self.board.check_victory()[0] and (len(self.board.get_valid_moves()) > 0):
            self.send_message("STAT" + str(self.current_turn) + "NZ")

            self.print_board()
            print("")

            if self.current_turn == 1:
                if randint(1, 100) < 35:
                    self.audio_manager.play_its_your_move()
                print("Player 1 turn:")
                self.make_player_move(1)
                self.current_turn = 0
                if randint(1, 100) < 20:
                    self.audio_manager.play_lol_really()

            elif self.current_turn == 0:
                print("Robot turn:")
                self.make_robot_move()
                self.current_turn = 1

            else:
                print("Error")

        self.print_board()

        winner = not self.current_turn
        self.send_message("STAT" + str(int(winner)) + "YZ")

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
        self.wait_for_client()
        self.audio_manager.play_hello_i_am_riccardino()

        while play == "1":
            self.game_interface()

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

            play = input("Play again: \n 1 for yes \n 0 for no\n")
            while play != "0" and play != "1":
                play = input("\nWould you like to play again?\n"
                             "1 yes\n"
                             "0 no \n")
            if play == "1":
                self.wait_for_client()

        print("Thanks for playing!")
        self.close_socket()
