from Board import Board
from copy import deepcopy


class Minimax:
    def __init__(self, maximising_marker, minimising_marker, game_setup_arguments, is_maximising=True):
        self.maximising_marker = maximising_marker
        self.minimising_marker = minimising_marker
        self.game_setup_arguments = game_setup_arguments
        self.is_maximising = is_maximising

    def minimax(self, state, is_maximising):
        if (score := self.evaluate(state[0], is_maximising)) is not None:
            return score, state[1]
        return (max if self.is_maximising else min)(
            self.minimax(state_info, not is_maximising)
            for state_info in self.possible_new_states(state[0], not is_maximising)
        )

    def best_move(self):
        pass

    def possible_new_states(self, state, is_maximising):
        """
        :param is_maximising: determines if the current turn is maximising player (bool)
        :param state: retrieves a state of the board
        :return: array of possible next board states (same number as columns)
        """

        player_marker = self.maximising_marker if is_maximising else self.minimising_marker

        current_board = Board(*self.game_setup_arguments, deepcopy(state))

        valid_next_states = current_board.get_valid_moves()
        possible_states = []

        for column in valid_next_states:
            current_board.make_move(column, player_marker)
            possible_states.append([current_board.grid, column])
            current_board.grid = deepcopy(state)

        return possible_states

    def evaluate(self, state, is_maximising):
        current_board = Board(*self.game_setup_arguments, state)
        player_marker = self.maximising_marker if is_maximising else self.minimising_marker
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
    # a.grid = [
    #     [2, 2, 2, 1, 0, 0, 0],
    #     [1, 1, 1, 2, 1, 1, 2],
    #     [2, 2, 2, 1, 2, 2, 1],
    #     [1, 1, 1, 2, 2, 1, 1],
    #     [2, 2, 2, 1, 1, 1, 2],
    #     [1, 1, 1, 2, 1, 1, 1],
    # ]
    # a.grid = [
    #     [0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 2, 1, 1],
    #     [1, 2, 1, 2, 1, 2, 2],
    #     [2, 2, 1, 2, 1, 2, 1],
    #     [1, 1, 2, 1, 1, 2, 2],
    #     [1, 2, 1, 2, 2, 1, 1],
    # ]
    a.grid = [
        [2, 0, 0, 0, 0, 1, 1],
        [2, 2, 2, 1, 2, 1, 1],
        [1, 2, 1, 2, 1, 2, 2],
        [2, 2, 1, 2, 1, 2, 1],
        [1, 1, 2, 1, 1, 2, 2],
        [1, 2, 1, 2, 2, 1, 1],
    ]
    # a.grid = [
    #     [0, 0, 0, 0, 0, 0, 1],
    #     [0, 2, 0, 0, 2, 1, 1],
    #     [1, 2, 1, 2, 1, 2, 2],
    #     [2, 2, 1, 2, 1, 2, 1],
    #     [1, 1, 2, 1, 1, 2, 2],
    #     [1, 2, 1, 2, 2, 1, 1],
    # ]
    # a.grid = [
    #     [0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0],
    #     [1, 2, 1, 2, 1, 2, 2],
    #     [2, 2, 1, 2, 1, 2, 1],
    #     [1, 1, 2, 1, 1, 2, 2],
    #     [1, 2, 1, 2, 2, 1, 1],
    # ]
    b = Minimax(1, 2, [6, 7, 0, 1, 2, "R"])
    print(b.minimax([a.grid, None], True))
