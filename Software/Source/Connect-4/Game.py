from Board import Board


class Game:
    def __init__(self, rows=6, columns=7, empty=0, player_1=1, player_2=2):
        self.board = Board(rows, columns, empty, player_1, player_2)

    # Arya/Shenglun
    # Prints the board in its current status
    def print_board(self):
        pass

    # Shenglun
    # Allows a human player to make a move when given the player number who is about to make a move
    def make_player_move(self, player_number):
        pass

    # Shenglun
    # Allows the robot to make a move
    def make_robot_move(self):
        pass

    # Arya
    # Allows user to choose if they want PvP or PvR and then calls other methods as needed to make moves
    def play_game(self):
        pass
