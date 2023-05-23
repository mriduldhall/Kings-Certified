from Board import Board
from Minimax import Minimax
from random import choice


class Game:
    def __init__(self):
        self.board = Board()
        self.minimax = Minimax(self.board.grid, self.board.robot_marker, self.board.player_1_marker)
        
    def make_player_move(self, player_number):
        row = str(input(f"Enter row (0 - 2): "))
        column = str(input(f"Enter column (0 - 2): "))
        marker = self.board.player_number_to_marker[player_number]
        positions = ["0", "1", "2"]
        while row not in positions or column not in positions or (row, column) not in self.board.get_valid_moves():
            print("Invalid move.")
            row = (input(f"Enter row (0 - 2): "))
            column = (input(f"Enter column (0 - 2): "))
        move = (str(row), str(column))
        self.board.make_move(move, marker)
        self.minimax.follow_move(move)

    def make_robot_move(self, is_maximising):
        move = choice(self.minimax.next_best_move(is_maximising))[0]
        # print(f"Chosen move: {move}")
        self.board.make_move(move, self.board.robot_marker)
        self.minimax.follow_move(move)

    def play_game(self):
        is_player_game = input("Play against Robot or another Player: \n 1 for player \n 0 for robot\n")
        while is_player_game != "0" and is_player_game != "1":
            is_player_game = input("Error. Please input 1 or 0. \n"
                                   "Play against Robot or another Player: \n"
                                   " 1 for player \n 0 for robot\n")

        print() 

        p1_first_play = input("Who plays first? \n 1 - I start first \n 0 - Opponent starts\n")
        while p1_first_play != "0" and p1_first_play != "1":
            p1_first_play = input("Error. Please input 1 or 0. \n"
                                  "Who plays first: \n"
                                  " 1 - I start first \n 0 - Opponent starts\n")

        if p1_first_play == "0":
            is_maximising = True
        else:
            is_maximising = False

        print("")

        is_player_game = int(is_player_game)
        p1_first_play = int(p1_first_play)
        current_turn = p1_first_play
        while not self.board.check_victory()[0] and len(self.board.get_valid_moves()) > 0:
            self.board.print_board()
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
                self.make_robot_move(is_maximising)
                current_turn = 1

            else:
                print("Error")
        
        winner = not current_turn
        
        self.board.print_board()
        
        if not self.board.get_valid_moves() and not self.board.check_victory()[0]:
            print("Draw")
        elif winner:
            print("Player 1 wins")
        elif is_player_game:
            print("Player 2 wins")
        else:
            print("Robot wins")


if __name__ == "__main__":
    a = Game()
    a.play_game()
