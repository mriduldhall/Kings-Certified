from Board import Board
from copy import deepcopy


class Minimax:
    def __init__(self, initial_state, maximising_marker, minimising_marker, game_setup_arguments, is_maximising=True):
        self.initial_state = initial_state
        self.maximising_marker = maximising_marker
        self.minimising_marker = minimising_marker
        self.game_setup_arguments = game_setup_arguments
        self.is_maximising = is_maximising

    def minimax(self, state, is_maximising):
        if (score := self.evaluate(state)) is not None:
            return score
        return (max if self.is_maximising else min)(
            self.minimax(new_state, not is_maximising)
            for new_state in self.possible_new_states(state)
        )

    def best_move(self):
        pass

    def possible_new_states(self, state):
        """
        :param state: retrieves a state of the board
        :return: array of possible next board states (same number as columns)
        """

        player_marker = self.maximising_marker if self.is_maximising else self.minimising_marker

        current_board = Board(*self.game_setup_arguments, deepcopy(state))

        valid_next_states = current_board.get_valid_moves()
        possible_states = []

        for column in valid_next_states:
            current_board.make_move(column, player_marker)
            possible_states.append(current_board.grid)
            current_board.grid = deepcopy(state)

        return possible_states

    def evaluate(self, state):
        current_board = Board(*self.game_setup_arguments, state)
        player_marker = self.maximising_marker if self.is_maximising else self.minimising_marker
        if current_board.check_victory()[0]:
            if current_board.check_victory()[1] == player_marker:
                return 1
            else:
                return -1
        elif not current_board.check_victory()[0] and not current_board.get_valid_moves():
            return 0
        else:
            return None


if __name__ == '__main__':
    a = Board(rows=6, columns=7, empty=0, player_1=1, player_2=2, robot='R')
    a.grid = [
        [2, 2, 2, 1, 0, 0, 0],
        [1, 1, 1, 2, 1, 1, 2],
        [2, 2, 2, 1, 2, 2, 1],
        [1, 1, 1, 2, 2, 1, 1],
        [2, 2, 2, 1, 1, 1, 2],
        [1, 1, 1, 2, 1, 1, 1],
    ]
    print(a.check_victory())
    b = Minimax(a, 1, 2, [6, 7, 0, 1, 2, "R"])
    print(b.minimax(a.grid, True))
